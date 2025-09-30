import os
import subprocess
import uuid
import base64
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import httpx

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


# Note: xAI does not currently support image generation
# Only chat completions with vision (image analysis) are supported


app = FastAPI(title="Grok Chat WebApp")
app.mount("/static", StaticFiles(directory=os.path.join(APP_ROOT, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(APP_ROOT, "templates"))


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
) -> str:
    """Call xAI chat completions API directly (supports multimodal)."""
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
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                "https://api.x.ai/v1/chat/completions",
                headers=headers,
                json=body,
            )
            response.raise_for_status()
            data = response.json()
            
            # Extract assistant message
            choices = data.get("choices", [])
            if not choices:
                raise HTTPException(status_code=500, detail="No response from API")
            
            content = choices[0].get("message", {}).get("content", "")
            return content
            
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="API request timeout (60s)")
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
    assistant_response = ""
    
    if image_data_urls:
        # Use xAI API directly for multimodal (images + text)
        messages = []
        
        # System message
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # User message with text and images
        user_content = [{"type": "text", "text": payload.message}]
        for img_url in image_data_urls:
            user_content.append({
                "type": "image_url",
                "image_url": {"url": img_url}
            })
        
        messages.append({"role": "user", "content": user_content})
        
        # Call API
        assistant_response = await call_xai_chat_api(
            payload.model,
            messages,
            payload.max_tokens,
            effective_temp,
            api_key,
        )
        
    else:
        # Use Rust CLI for text-only (more efficient)
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
                timeout=60,
                cwd=REPO_ROOT,
            )
            
            if result.returncode != 0:
                error_detail = result.stderr.strip() or result.stdout.strip() or "Unknown error"
                raise HTTPException(status_code=500, detail=f"Inference error: {error_detail}")
            
            assistant_response = result.stdout.strip()
            
        except subprocess.TimeoutExpired:
            raise HTTPException(status_code=504, detail="Inference timeout (60s)")
    
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