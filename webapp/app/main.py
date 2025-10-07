import os
import subprocess
import uuid
import base64
import json
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables BEFORE importing anything else
# Get the repo root and load .env from there
REPO_ROOT = Path(__file__).parent.parent.parent
load_dotenv(REPO_ROOT / ".env")

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import httpx

# Import n8n workflow builder service
from .n8n_service import (
    N8NService,
    GrokWorkflowBuilder,
    generate_workflow_from_prompt,
)
from .genius_enhancements import (
    WorkflowOptimizer,
    WorkflowTemplateManager,
    generate_genius_workflow,
)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(APP_ROOT, "..", ".."))
RUST_BIN = os.path.join(REPO_ROOT, "grok-chat-app", "target", "release", "grok-chat-app")

# In-memory sessions (ephemeral)
sessions: Dict[str, List[Dict[str, str]]] = {}

# Pricing per 1M tokens (USD) - configurable via environment
PRICING = {
    "grok-4-0709": {"input": 5.0, "output": 15.0},
    "grok-4-fast-reasoning": {"input": 3.0, "output": 6.0},
    "grok-4-fast-non-reasoning": {"input": 1.5, "output": 3.0},
    "grok-3": {"input": 1.0, "output": 2.0},
    "grok-3-mini": {"input": 0.2, "output": 0.4},
    "grok-code-fast-1": {"input": 0.2, "output": 1.5},  # Optimized for coding tasks
}

# Override from environment
for model in PRICING:
    key = model.upper().replace("-", "_")
    input_env = os.getenv(f"PRICE_{key}_INPUT_PER_MTOK")
    output_env = os.getenv(f"PRICE_{key}_OUTPUT_PER_MTOK")
    if input_env:
        PRICING[model]["input"] = float(input_env)
    if output_env:
        PRICING[model]["output"] = float(output_env)

AVAILABLE_MODELS = list(PRICING.keys())


class ChatPayload(BaseModel):
    session_id: Optional[str] = None
    message: str
    model: str = Field(default="grok-4-0709")
    system_prompt: Optional[str] = None
    max_tokens: int = Field(default=2048, ge=1, le=8192)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    context_window: int = Field(default=6, ge=0, le=50)
    mode: Optional[str] = Field(default="standard")
    expected_output_tokens: Optional[int] = Field(default=512, ge=1, le=8192)
    files: Optional[List[Dict[str, str]]] = None  # [{name, content}]
    web_search: Optional[bool] = False
    tools: Optional[List[Dict[str, Any]]] = None  # For agentic tasks
    codebase_context: Optional[str] = None  # For coding tasks


# Note: xAI does not currently support image generation
# Only chat completions with vision (image analysis) are supported


app = FastAPI(title="Grok Chat WebApp with n8n Workflow Builder")
app.mount("/static", StaticFiles(directory=os.path.join(APP_ROOT, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(APP_ROOT, "templates"))

# Initialize n8n service
n8n_service = N8NService()


def ensure_rust_binary() -> None:
    if not os.path.exists(RUST_BIN):
        raise FileNotFoundError(
            f"Rust binary not found at {RUST_BIN}. Build it with: cargo build --release --features terminal --manifest-path grok-chat-app/Cargo.toml"
        )


async def web_search_duckduckgo(query: str) -> Optional[str]:
    """Perform DuckDuckGo instant answer search."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.duckduckgo.com/",
                params={"q": query, "format": "json", "no_html": "1", "no_redirect": "1"},
                timeout=5.0,
            )
            response.raise_for_status()
            data = response.json()
            abstract = data.get("AbstractText") or ""
            if not abstract and isinstance(data.get("RelatedTopics"), list):
                for topic in data["RelatedTopics"]:
                    if isinstance(topic, dict) and topic.get("Text"):
                        abstract = topic["Text"]
                        break
            return abstract or None
    except Exception:
        return None


def estimate_tokens(text: str) -> int:
    """Simple heuristic: ~4 chars per token."""
    if not text:
        return 0
    return max(1, (len(text) + 3) // 4)


def build_system_prompt(
    base: Optional[str],
    history: List[Dict[str, str]],
    window: int,
    file_contents: str,
    web_result: Optional[str],
    mode: str,
) -> str:
    """Build comprehensive system prompt with all context."""
    prompt_parts = []
    
    # Base prompt
    base_prompt = base or "You are Grok, a helpful and maximally truthful AI built by xAI."
    
    # Mode adjustments
    if mode == "deep_research":
        base_prompt += "\n\nYou are in deep research mode. Provide comprehensive, detailed answers with multi-step reasoning. Cite sources and assumptions when possible."
    
    prompt_parts.append(base_prompt)
    
    # Web search results
    if web_result:
        prompt_parts.append(f"\n--- Web Search Results ---\n{web_result}\n--- End Web Search ---")
    
    # File contents
    if file_contents:
        prompt_parts.append(f"\n--- Attached Files ---\n{file_contents}\n--- End Attached Files ---")
    
    # Conversation history
    if window > 0 and history:
        prompt_parts.append("\n--- Recent Conversation History ---")
        recent = history[-window:]
        for msg in recent:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            prompt_parts.append(f"{role.capitalize()}: {content}")
        prompt_parts.append("--- End History ---")
    
    return "\n".join(prompt_parts)


def calculate_cost_estimate(
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
) -> Dict[str, Any]:
    """Calculate cost estimate based on token usage."""
    pricing = PRICING.get(model, PRICING["grok-4-0709"])
    input_cost = (prompt_tokens / 1_000_000.0) * pricing["input"]
    output_cost = (completion_tokens / 1_000_000.0) * pricing["output"]
    total_cost = input_cost + output_cost
    
    return {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens,
        "pricing": pricing,
        "cost": {
            "input_usd": round(input_cost, 6),
            "output_usd": round(output_cost, 6),
            "total_usd": round(total_cost, 6),
        },
    }


async def call_xai_chat_api(
    model: str,
    messages: List[Dict[str, Any]],
    max_tokens: int,
    temperature: float,
    api_key: str,
    tools: Optional[List[Dict[str, Any]]] = None,
    timeout_seconds: int = 120,  # Increased timeout for long-running tasks
) -> Dict[str, Any]:
    """Call xAI chat completions API directly (supports multimodal and tools)."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    body = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": False,
    }

    # Add tools if provided (for agentic tasks)
    if tools:
        body["tools"] = tools

    async with httpx.AsyncClient(timeout=timeout_seconds) as client:
        try:
            response = await client.post(
                "https://api.x.ai/v1/chat/completions",
                headers=headers,
                json=body,
            )
            response.raise_for_status()
            data = response.json()

            # Extract assistant message and tool calls
            choices = data.get("choices", [])
            if not choices:
                raise HTTPException(status_code=500, detail="No response from API")

            message = choices[0].get("message", {})
            content = message.get("content", "")

            # Handle tool calls for agentic tasks
            tool_calls = message.get("tool_calls", [])

            return {
                "content": content,
                "tool_calls": tool_calls,
                "usage": data.get("usage", {}),
            }

        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail=f"API request timeout ({timeout_seconds}s)")
        except httpx.HTTPStatusError as e:
            error_text = e.response.text
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"API Error: {error_text}"
            )


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "models": AVAILABLE_MODELS,
            "default_model": os.getenv("DEFAULT_MODEL", "grok-4-0709"),
            "default_temperature": 0.7,
            "default_max_tokens": 2048,
        },
    )


@app.get("/workflows", response_class=HTMLResponse)
async def workflow_builder_page(request: Request):
    """n8n Workflow Builder UI"""
    return templates.TemplateResponse(
        "workflow.html",
        {
            "request": request,
        },
    )


@app.post("/api/chat")
async def chat(payload: ChatPayload):
    """
    Main chat endpoint supporting:
    - Text chat with context history
    - File attachments (text and images)
    - Web search augmentation
    - Deep research mode
    - Cost estimation
    """
    ensure_rust_binary()
    
    # Get or create session
    session_id = payload.session_id or str(uuid.uuid4())
    history = sessions.setdefault(session_id, [])
    
    # Get API key
    api_key = os.environ.get("XAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="XAI_API_KEY not set in environment")
    
    # Adjust parameters based on mode
    effective_window = payload.context_window
    effective_temp = payload.temperature
    
    if payload.mode == "deep_research":
        effective_window = max(effective_window, 20)  # Larger context for research
        effective_temp = max(0.2, min(0.9, effective_temp))  # Moderate temperature
    
    # Process attached files
    file_contents = ""
    image_data_urls = []
    
    if payload.files:
        total_chars = 0
        for file_info in payload.files:
            name = file_info.get("name", "attachment")
            content = file_info.get("content", "")
            
            if not content:
                continue
            
            # Check if it's an image (data URL)
            if content.startswith("data:image/"):
                image_data_urls.append(content)
            else:
                # Text file - limit size
                snippet = content[:50_000]
                if total_chars + len(snippet) > 150_000:
                    break
                total_chars += len(snippet)
                file_contents += f"\n[File: {name}]\n{snippet}\n"
    
    # Web search augmentation
    web_result = None
    if payload.web_search:
        web_result = await web_search_duckduckgo(payload.message)
    
    # Build system prompt with all context
    system_prompt = build_system_prompt(
        payload.system_prompt,
        history,
        effective_window,
        file_contents,
        web_result,
        payload.mode or "standard",
    )
    
    # Add user message to history
    history.append({"role": "user", "content": payload.message})
    
    # Determine which inference path to use
    # For coding tasks or when tools are specified, use direct API for better control
    use_direct_api = image_data_urls or payload.tools or payload.codebase_context or payload.model == "grok-code-fast-1"

    assistant_response = ""
    tool_calls = []

    if use_direct_api:
        # Use xAI API directly for multimodal, tools, or coding tasks
        messages = []

        # System message
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        # User message
        if image_data_urls:
            # Multimodal message with text and images
            user_content = [{"type": "text", "text": payload.message}]
            for img_url in image_data_urls:
                user_content.append({
                    "type": "image_url",
                    "image_url": {"url": img_url}
                })
            messages.append({"role": "user", "content": user_content})
        else:
            # Text-only message
            messages.append({"role": "user", "content": payload.message})

        # Call API with support for tools and longer timeout
        api_response = await call_xai_chat_api(
            payload.model,
            messages,
            payload.max_tokens,
            effective_temp,
            api_key,
            tools=payload.tools,
            timeout_seconds=180,  # Longer timeout for complex tasks
        )

        assistant_response = api_response["content"]
        tool_calls = api_response.get("tool_calls", [])

    else:
        # Use Rust CLI for simple text-only (more efficient)
        cmd = [
            RUST_BIN,
            "-g", payload.message,
            "-m", payload.model,
            "-x", str(payload.max_tokens),
            "--temperature", str(effective_temp),
            "-y", system_prompt,
        ]

        env = os.environ.copy()

        try:
            result = subprocess.run(
                cmd,
                env=env,
                capture_output=True,
                text=True,
                timeout=120,  # Increased timeout
                cwd=REPO_ROOT,
            )

            if result.returncode != 0:
                error_detail = result.stderr.strip() or result.stdout.strip() or "Unknown error"
                raise HTTPException(status_code=500, detail=f"Inference error: {error_detail}")

            assistant_response = result.stdout.strip()

        except subprocess.TimeoutExpired:
            raise HTTPException(status_code=504, detail="Inference timeout (120s)")
    
    # Save assistant response to history
    history.append({"role": "assistant", "content": assistant_response})
    
    # Calculate cost estimate
    prompt_tokens = estimate_tokens(system_prompt) + estimate_tokens(payload.message)
    completion_tokens = payload.expected_output_tokens or 512
    
    estimate = calculate_cost_estimate(
        payload.model,
        prompt_tokens,
        completion_tokens,
    )
    
    return JSONResponse({
        "assistant": assistant_response,
        "session_id": session_id,
        "model": payload.model,
        "estimate": estimate,
        "mode": payload.mode or "standard",
        "tool_calls": tool_calls,
    })


# Image generation endpoint removed - xAI does not support this feature
# xAI only supports chat completions with vision (analyzing images, not generating them)


@app.get("/api/models")
async def list_models():
    """List available models with pricing information."""
    models_info = []
    for model in AVAILABLE_MODELS:
        models_info.append({
            "name": model,
            "pricing": PRICING[model],
        })
    
    return JSONResponse({
        "models": models_info,
        "count": len(models_info),
    })


@app.post("/api/estimate")
async def estimate_cost(payload: ChatPayload):
    """
    Estimate cost without making an inference call.
    Useful for live cost preview as user types.
    """
    # Build system prompt
    history = sessions.get(payload.session_id, [])
    
    file_contents = ""
    if payload.files:
        for file_info in payload.files:
            content = file_info.get("content", "")
            if not content.startswith("data:image/"):
                file_contents += content[:1000] + "\n"  # Just sample for estimate
    
    system_prompt = build_system_prompt(
        payload.system_prompt,
        history,
        payload.context_window,
        file_contents,
        None,  # Skip web search for estimate
        payload.mode or "standard",
    )
    
    prompt_tokens = estimate_tokens(system_prompt) + estimate_tokens(payload.message)
    completion_tokens = payload.expected_output_tokens or 512
    
    estimate = calculate_cost_estimate(
        payload.model,
        prompt_tokens,
        completion_tokens,
    )
    
    return JSONResponse(estimate)


# ============================================
# n8n Workflow Builder API Endpoints
# ============================================


class WorkflowGenerationRequest(BaseModel):
    """Request to generate an n8n workflow from natural language"""
    prompt: str = Field(..., description="Natural language description of the workflow")
    mode: str = Field(default="interpret", description="Generation mode: 'interpret' or 'exact'")
    node_sequence: Optional[str] = Field(None, description="Optional node sequence specification")
    node_details: Optional[str] = Field(None, description="Optional detailed requirements for specific nodes")
    auto_activate: bool = Field(default=False, description="Automatically activate the workflow after creation")
    session_id: Optional[str] = None


@app.get("/api/n8n/health")
async def n8n_health():
    """Check if n8n service is accessible"""
    is_healthy = await n8n_service.health_check()
    return JSONResponse({
        "healthy": is_healthy,
        "n8n_url": n8n_service.api_url,
        "webhook_url": n8n_service.webhook_url,
    })


@app.get("/api/n8n/workflows")
async def list_n8n_workflows():
    """List all n8n workflows"""
    try:
        workflows = await n8n_service.list_workflows()
        return JSONResponse({
            "workflows": workflows,
            "count": len(workflows),
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list workflows: {str(e)}")


@app.get("/api/n8n/workflows/{workflow_id}")
async def get_n8n_workflow(workflow_id: str):
    """Get a specific n8n workflow"""
    try:
        workflow = await n8n_service.get_workflow(workflow_id)
        return JSONResponse(workflow)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Workflow not found: {str(e)}")


@app.post("/api/n8n/workflows/generate/genius")
async def generate_genius_workflow_endpoint(request: WorkflowGenerationRequest):
    """
    Genius-level workflow generation with all advanced features:
    - Multi-stage AI processing
    - Template suggestions
    - Performance optimization  
    - Deep intent analysis
    - Intelligent connections
    """
    api_key = os.environ.get("XAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="XAI_API_KEY not set")
    
    if not await n8n_service.health_check():
        raise HTTPException(
            status_code=503,
            detail="n8n service is not accessible. Make sure it's running on " + n8n_service.api_url
        )
    
    try:
        result = await generate_genius_workflow(
            request.prompt,
            api_key,
            n8n_service,
            mode=request.mode,
            use_templates=True,
            optimize_performance=True
        )
        
        if request.auto_activate and result.get("workflow_id"):
            await n8n_service.activate_workflow(result["workflow_id"])
            result["activated"] = True
        
        return JSONResponse(result)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Genius workflow generation failed: {str(e)}"
        )

@app.post("/api/n8n/workflows/generate/advanced")
async def generate_advanced_workflow(request: WorkflowGenerationRequest):
    """
    Advanced workflow generation with multi-stage Grok AI processing.
    
    Features:
    - Input enhancement with Grok-3-mini (fast)
    - Intelligent connection building
    - Mode selection (interpret vs exact)
    - Node sequence control
    - Progress tracking
    """
    api_key = os.environ.get("XAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="XAI_API_KEY not set")
    
    # Check n8n health
    if not await n8n_service.health_check():
        raise HTTPException(
            status_code=503,
            detail="n8n service is not accessible. Make sure it's running on " + n8n_service.api_url
        )
    
    try:
        # Combine prompt with node details if provided
        full_prompt = request.prompt
        if request.node_details:
            full_prompt += f"\n\nSpecific Requirements:\n{request.node_details}"
        
        # Generate and deploy workflow with advanced options
        result = await generate_workflow_from_prompt(
            full_prompt,
            api_key,
            n8n_service,
            mode=request.mode,
            node_sequence=request.node_sequence,
        )
        
        workflow_id = result.get("workflow_id")
        
        # Optionally activate the workflow
        if request.auto_activate and workflow_id:
            await n8n_service.activate_workflow(workflow_id)
            result["activated"] = True
        
        # Store in session history if provided
        if request.session_id:
            history = sessions.setdefault(request.session_id, [])
            history.append({
                "role": "user",
                "content": f"[Advanced Workflow] {request.prompt} (Mode: {request.mode})"
            })
            history.append({
                "role": "assistant",
                "content": f"Created advanced workflow: {result['workflow_name']} with intelligent connections (ID: {workflow_id})"
            })
        
        return JSONResponse(result)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate advanced workflow: {str(e)}"
        )

@app.post("/api/n8n/workflows/generate")
async def generate_n8n_workflow(request: WorkflowGenerationRequest):
    """
    Generate a complete n8n workflow from natural language prompt.
    
    This endpoint uses the Grok API to:
    1. Analyze the workflow request
    2. Break it down into n8n nodes
    3. Configure connections and parameters
    4. Deploy to n8n
    
    Example prompts:
    - "Create a workflow that sends me a Slack message every day at 9 AM with weather data"
    - "Build a webhook that receives form submissions and saves them to Google Sheets"
    - "Make a workflow that monitors my Gmail for invoices and extracts data to Airtable"
    """
    api_key = os.environ.get("XAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="XAI_API_KEY not set")
    
    # Check n8n health
    if not await n8n_service.health_check():
        raise HTTPException(
            status_code=503,
            detail="n8n service is not accessible. Make sure it's running on " + n8n_service.api_url
        )
    
    try:
        # Generate and deploy workflow (basic mode for backwards compatibility)
        result = await generate_workflow_from_prompt(
            request.prompt,
            api_key,
            n8n_service,
            mode=request.mode,
            node_sequence=request.node_sequence,
        )
        
        workflow_id = result.get("workflow_id")
        
        # Optionally activate the workflow
        if request.auto_activate and workflow_id:
            await n8n_service.activate_workflow(workflow_id)
            result["activated"] = True
        
        # Store in session history if provided
        if request.session_id:
            history = sessions.setdefault(request.session_id, [])
            history.append({
                "role": "user",
                "content": f"[Workflow Request] {request.prompt}"
            })
            history.append({
                "role": "assistant",
                "content": f"Created workflow: {result['workflow_name']} (ID: {workflow_id})"
            })
        
        return JSONResponse(result)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate workflow: {str(e)}"
        )


@app.post("/api/n8n/workflows/{workflow_id}/activate")
async def activate_n8n_workflow(workflow_id: str):
    """Activate an n8n workflow"""
    try:
        result = await n8n_service.activate_workflow(workflow_id)
        return JSONResponse(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to activate workflow: {str(e)}")


@app.post("/api/n8n/workflows/{workflow_id}/execute")
async def execute_n8n_workflow(workflow_id: str, data: Optional[Dict[str, Any]] = None):
    """Manually execute an n8n workflow"""
    try:
        result = await n8n_service.execute_workflow(workflow_id, data)
        return JSONResponse(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to execute workflow: {str(e)}")


@app.delete("/api/n8n/workflows/{workflow_id}")
async def delete_n8n_workflow(workflow_id: str):
    """Delete an n8n workflow"""
    try:
        await n8n_service.delete_workflow(workflow_id)
        return JSONResponse({"success": True, "message": f"Workflow {workflow_id} deleted"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete workflow: {str(e)}")


@app.post("/api/chat/workflow")
async def chat_with_workflow_builder(payload: ChatPayload):
    """
    Enhanced chat endpoint that can understand workflow requests and automatically
    generate n8n workflows when the user is asking to create automation.
    
    This combines chat with workflow generation intelligence.
    """
    api_key = os.environ.get("XAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="XAI_API_KEY not set")
    
    # Get or create session
    session_id = payload.session_id or str(uuid.uuid4())
    history = sessions.setdefault(session_id, [])
    
    # First, use Grok to determine if this is a workflow creation request
    detection_prompt = f"""Analyze this message and determine if the user is requesting to create, build, or automate a workflow:

User message: "{payload.message}"

Respond with ONLY a JSON object:
{{
  "is_workflow_request": true/false,
  "confidence": 0.0-1.0,
  "extracted_intent": "brief description if true"
}}"""
    
    # Quick detection call
    async with httpx.AsyncClient(timeout=30.0) as client:
        detection_response = await client.post(
            "https://api.x.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "grok-4-fast-non-reasoning",
                "messages": [{"role": "user", "content": detection_prompt}],
                "temperature": 0.1,
                "max_tokens": 256,
            },
        )
        detection_data = detection_response.json()
        detection_content = detection_data["choices"][0]["message"]["content"]
        
        # Parse detection
        try:
            if "```json" in detection_content:
                detection_content = detection_content.split("```json")[1].split("```")[0].strip()
            elif "```" in detection_content:
                detection_content = detection_content.split("```")[1].split("```")[0].strip()
            
            detection = json.loads(detection_content)
        except:
            detection = {"is_workflow_request": False, "confidence": 0.0}
    
    # If high confidence workflow request, generate it
    if detection.get("is_workflow_request") and detection.get("confidence", 0) > 0.7:
        if await n8n_service.health_check():
            try:
                # Generate the workflow
                result = await generate_workflow_from_prompt(
                    payload.message,
                    api_key,
                    n8n_service,
                )
                
                workflow_id = result.get("workflow_id")
                workflow_name = result.get("workflow_name")
                
                # Build response
                response_text = f"""✅ I've created your n8n workflow!

**Workflow Name:** {workflow_name}
**Workflow ID:** {workflow_id}

The workflow has been deployed to your n8n instance. You can:
- View it at: {n8n_service.webhook_url}/workflow/{workflow_id}
- Activate it using the activate button
- Test it manually

Would you like me to activate it now or make any modifications?"""
                
                history.append({"role": "user", "content": payload.message})
                history.append({"role": "assistant", "content": response_text})
                
                return JSONResponse({
                    "assistant": response_text,
                    "session_id": session_id,
                    "workflow_generated": True,
                    "workflow": result,
                })
            except Exception as e:
                # Fall back to regular chat if workflow generation fails
                pass
    
    # Otherwise, use regular chat endpoint
    return await chat(payload)