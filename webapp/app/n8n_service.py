"""
n8n Workflow Builder Service

This module provides intelligent workflow generation using Grok API
to automatically create, configure, and deploy n8n workflows.
"""

import os
import json
from typing import Dict, Any, List, Optional
import httpx
from pydantic import BaseModel


class N8NNode(BaseModel):
    """Represents an n8n workflow node"""
    id: str
    name: str
    type: str
    typeVersion: int = 1
    position: List[float]
    parameters: Dict[str, Any] = {}
    credentials: Dict[str, Any] = {}


class N8NConnection(BaseModel):
    """Represents connections between n8n nodes"""
    source: str
    sourceOutput: int = 0
    target: str
    targetInput: int = 0


class N8NWorkflow(BaseModel):
    """Complete n8n workflow structure"""
    name: str
    nodes: List[N8NNode]
    connections: Dict[str, Any]
    settings: Dict[str, Any] = {}
    tags: List[str] = []
    
    def to_create_dict(self) -> Dict[str, Any]:
        """Convert to dict for creation (excludes read-only fields like active, tags)"""
        return {
            "name": self.name,
            "nodes": [node.dict() for node in self.nodes],
            "connections": self.connections,
            "settings": self.settings
        }


class N8NService:
    """Service for interacting with n8n API and building workflows"""

    def __init__(
        self,
        api_url: Optional[str] = None,
        auth_user: Optional[str] = None,
        auth_password: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        self.api_url = api_url or os.getenv("N8N_API_URL", "http://localhost:5678/api/v1")
        self.auth_user = auth_user or os.getenv("N8N_AUTH_USER", "admin")
        self.auth_password = auth_password or os.getenv("N8N_AUTH_PASSWORD", "changeme")
        self.api_key = api_key or os.getenv("N8N_API_KEY")
        self.webhook_url = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678")

    def _get_headers(self) -> Dict[str, str]:
        """Get authentication headers (API key or basic auth)"""
        if self.api_key:
            return {"X-N8N-API-KEY": self.api_key}
        return {}

    def _get_auth(self):
        """Get basic auth credentials (only if no API key)"""
        if self.api_key:
            return None
        return (self.auth_user, self.auth_password)

    async def health_check(self) -> bool:
        """Check if n8n is accessible"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_url}/workflows",
                    headers=self._get_headers(),
                    auth=self._get_auth(),
                    timeout=5.0,
                )
                return response.status_code == 200
        except Exception:
            return False

    async def list_workflows(self) -> List[Dict[str, Any]]:
        """List all workflows"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/workflows",
                headers=self._get_headers(),
                auth=self._get_auth(),
            )
            response.raise_for_status()
            return response.json().get("data", [])

    async def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Get a specific workflow by ID"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/workflows/{workflow_id}",
                headers=self._get_headers(),
                auth=self._get_auth(),
            )
            response.raise_for_status()
            return response.json()

    async def create_workflow(self, workflow: N8NWorkflow) -> Dict[str, Any]:
        """Create a new workflow"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/workflows",
                headers=self._get_headers(),
                auth=self._get_auth(),
                json=workflow.to_create_dict(),
            )
            response.raise_for_status()
            return response.json()

    async def update_workflow(
        self, workflow_id: str, workflow: N8NWorkflow
    ) -> Dict[str, Any]:
        """Update an existing workflow"""
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{self.api_url}/workflows/{workflow_id}",
                headers=self._get_headers(),
                auth=self._get_auth(),
                json=workflow.dict(),
            )
            response.raise_for_status()
            return response.json()

    async def activate_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Activate a workflow"""
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{self.api_url}/workflows/{workflow_id}",
                headers=self._get_headers(),
                auth=self._get_auth(),
                json={"active": True},
            )
            response.raise_for_status()
            return response.json()

    async def execute_workflow(
        self, workflow_id: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Manually execute a workflow"""
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.api_url}/workflows/{workflow_id}/execute",
                headers=self._get_headers(),
                auth=self._get_auth(),
                json={"data": data or {}},
            )
            response.raise_for_status()
            return response.json()

    async def delete_workflow(self, workflow_id: str) -> bool:
        """Delete a workflow"""
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.api_url}/workflows/{workflow_id}",
                headers=self._get_headers(),
                auth=self._get_auth(),
            )
            response.raise_for_status()
            return True


class GrokWorkflowBuilder:
    """Advanced n8n workflow builder using multi-stage Grok AI processing"""

    def __init__(self, xai_api_key: str):
        self.api_key = xai_api_key
        self.api_url = "https://api.x.ai/v1/chat/completions"
        
        # Different models for different tasks
        self.models = {
            "analysis": "grok-4-0709",  # Complex reasoning for workflow design
            "enhancement": "grok-3-mini",  # Fast enhancement and validation
            "configuration": "grok-4-fast-non-reasoning"  # Fast parameter generation
        }

    async def enhance_user_input(
        self, 
        user_prompt: str, 
        mode: str = "interpret", 
        node_sequence: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Stage 1: Use Grok-3-mini to enhance and validate user input
        This is fast and improves the quality of the main analysis
        """
        system_prompt = f"""You are a workflow enhancement AI. Your job is to take user input and enhance it for optimal workflow generation.

Mode: {mode}
- "interpret": Be creative and add helpful details
- "exact": Follow user instructions precisely, minimal interpretation

{"User specified node sequence: " + node_sequence if node_sequence else "No specific sequence provided"}

Enhance the user's workflow request by:
1. Clarifying ambiguous requirements
2. Adding missing technical details
3. Suggesting optimal node sequence if not provided
4. Identifying required integrations and APIs
5. Adding error handling considerations

Respond with JSON:
{{
  "enhanced_prompt": "improved and detailed prompt",
  "suggested_sequence": ["node1", "node2", "node3"],
  "required_integrations": ["slack", "gmail", "sheets"],
  "estimated_complexity": "simple|medium|complex",
  "recommendations": "helpful suggestions"
}}"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        async with httpx.AsyncClient(timeout=30.0) as client:  # Fast model
            response = await client.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.models["enhancement"],  # grok-3-mini
                    "messages": messages,
                    "temperature": 0.3,
                    "max_tokens": 1024,
                },
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]

            try:
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()

                return json.loads(content)
            except json.JSONDecodeError:
                # Fallback if enhancement fails
                return {
                    "enhanced_prompt": user_prompt,
                    "suggested_sequence": [],
                    "required_integrations": [],
                    "estimated_complexity": "medium",
                    "recommendations": "No enhancements available"
                }

    async def analyze_workflow_request(
        self, 
        enhanced_prompt: str, 
        complexity: str = "medium"
    ) -> Dict[str, Any]:
        """
        Step 1: Use Grok to analyze and break down the workflow request
        """
        system_prompt = """You are an expert n8n workflow architect. Analyze the user's workflow request and break it down into:

1. Workflow goal and description
2. Required nodes (with types from n8n's node library)
3. Data flow and connections between nodes
4. Required credentials and configurations
5. Input/output specifications
6. Error handling requirements

IMPORTANT GUIDELINES:
- Keep workflows SIMPLE and focused (max 8 nodes for reliability)
- Use only common, well-supported n8n node types
- Ensure each node has a clear purpose
- Create linear data flow when possible
- Include proper error handling

Respond ONLY with valid JSON in this exact format:
{
  "workflow_name": "descriptive name",
  "description": "what this workflow does",
  "nodes": [
    {
      "id": "unique_descriptive_id",
      "name": "Clear Node Name",
      "type": "n8n-nodes-base.nodetype",
      "parameters": {
        "key": "value"
      }
    }
  ],
  "connections": [
    {
      "source": "source_node_id",
      "target": "target_node_id"
    }
  ],
  "tags": ["tag1", "tag2"]
}

Common n8n node types:
- n8n-nodes-base.webhook (HTTP webhooks)
- n8n-nodes-base.httpRequest (make HTTP requests)
- n8n-nodes-base.set (set/transform data)
- n8n-nodes-base.if (conditional logic)
- n8n-nodes-base.function (custom JavaScript)
- n8n-nodes-base.slack (Slack integration)
- n8n-nodes-base.gmail (Gmail integration)
- n8n-nodes-base.googleSheets (Google Sheets)
- n8n-nodes-base.scheduleTrigger (cron schedule)
- n8n-nodes-base.respondToWebhook (respond to webhook)
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        # Use different timeouts and models based on complexity
        timeout = 60.0 if complexity == "simple" else 120.0 if complexity == "medium" else 240.0
        model = self.models["analysis"] if complexity in ["medium", "complex"] else self.models["configuration"]

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": 0.2,  # More deterministic for complex workflows
                    "max_tokens": 4096,
                },
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]

            # Parse JSON from response
            try:
                # Try to extract JSON from code blocks
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()

                return json.loads(content)
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse Grok response as JSON: {e}\n{content}")

    async def generate_node_configuration(
        self, node_type: str, context: str
    ) -> Dict[str, Any]:
        """
        Step 2: Use Grok to generate detailed configuration for a specific node
        """
        system_prompt = f"""You are configuring an n8n workflow node of type: {node_type}

Generate the complete configuration parameters for this node based on the context.
Respond ONLY with valid JSON representing the node's parameters object.

Example for httpRequest node:
{{
  "method": "POST",
  "url": "https://api.example.com/endpoint",
  "authentication": "none",
  "sendHeaders": true,
  "headerParameters": {{
    "parameters": [
      {{"name": "Content-Type", "value": "application/json"}}
    ]
  }},
  "sendBody": true,
  "bodyParameters": {{
    "parameters": [
      {{"name": "key", "value": "value"}}
    ]
  }}
}}
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": context},
        ]

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "grok-4-fast-non-reasoning",
                    "messages": messages,
                    "temperature": 0.2,
                    "max_tokens": 2048,
                },
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]

            # Parse JSON from response
            try:
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()

                return json.loads(content)
            except json.JSONDecodeError:
                return {}

    async def build_complete_workflow(
        self, 
        user_prompt: str,
        mode: str = "interpret",
        node_sequence: Optional[str] = None,
        progress_callback: Optional[callable] = None
    ) -> N8NWorkflow:
        """
        Complete workflow: Multi-stage AI-powered workflow generation
        """
        if progress_callback:
            progress_callback("Enhancing user input with Grok-3-mini...")
        
        # Stage 1: Enhance user input (fast)
        enhancement = await self.enhance_user_input(user_prompt, mode, node_sequence)
        enhanced_prompt = enhancement.get("enhanced_prompt", user_prompt)
        complexity = enhancement.get("estimated_complexity", "medium")
        
        if progress_callback:
            progress_callback(f"Analyzing workflow structure ({complexity} complexity)...")
        
        # Stage 2: Analyze the enhanced request
        analysis = await self.analyze_workflow_request(enhanced_prompt, complexity)

        if progress_callback:
            progress_callback(f"Building {len(analysis.get('nodes', []))} nodes...")
        
        # Stage 3: Build nodes with advanced configurations
        nodes = []
        node_map = {}

        for i, node_spec in enumerate(analysis.get("nodes", [])):
            # Generate detailed configuration if needed
            if not node_spec.get("parameters"):
                context = f"Node: {node_spec['name']}, Type: {node_spec['type']}, Purpose: {analysis.get('description', '')}"
                parameters = await self.generate_node_configuration(
                    node_spec["type"], context
                )
            else:
                parameters = node_spec.get("parameters", {})

            # Create node with intelligent positioning for complex workflows
            row = i // 4  # 4 nodes per row
            col = i % 4   # Column in current row
            position = node_spec.get("position", [
                200 + (col * 300),  # X: 200, 500, 800, 1100, then wrap
                200 + (row * 200)   # Y: 200, 400, 600, etc.
            ])

            # Validate and clean parameters
            parameters = self._validate_node_parameters(
                node_spec["type"], 
                parameters if parameters else {}
            )

            node = N8NNode(
                id=node_spec.get("id", f"node_{i}"),
                name=node_spec["name"],
                type=node_spec["type"],
                position=position,
                parameters=parameters,
            )
            nodes.append(node)
            node_map[node.id] = node

        if progress_callback:
            progress_callback("Creating intelligent node connections...")
        
        # Stage 4: Build intelligent connections
        connections = self._build_intelligent_connections(analysis, node_map)
        
        # Stage 5: Validate and optimize connections
        connections = self._validate_and_optimize_connections(connections, node_map)

        # Step 4: Create complete workflow
        workflow = N8NWorkflow(
            name=analysis.get("workflow_name", "AI Generated Workflow"),
            nodes=nodes,
            connections=connections,
            tags=analysis.get("tags", ["ai-generated", "grok"]),
            settings={
                "executionOrder": "v1",
            },
        )

        return workflow

    def _validate_node_parameters(self, node_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and fix node parameters to prevent n8n errors"""
        
        # Common parameter fixes
        clean_params = {}
        
        for key, value in parameters.items():
            if value is None:
                continue  # Skip None values
            
            # Handle arrays that might not be iterable
            if isinstance(value, str) and key in ['headers', 'parameters']:
                # These should be objects, not strings
                continue
            
            # Handle nested objects
            if isinstance(value, dict):
                clean_nested = {}
                for nested_key, nested_value in value.items():
                    if nested_value is not None:
                        clean_nested[nested_key] = nested_value
                if clean_nested:  # Only add if not empty
                    clean_params[key] = clean_nested
            else:
                clean_params[key] = value
        
        # Node-type specific validation
        if node_type == "n8n-nodes-base.httpRequest":
            # Ensure HTTP request has proper structure
            if "method" not in clean_params:
                clean_params["method"] = "GET"
            if "url" not in clean_params:
                clean_params["url"] = "https://api.example.com"
                
        elif node_type == "n8n-nodes-base.scheduleTrigger":
            # Ensure schedule has proper format
            if "rule" not in clean_params and "cronExpression" not in clean_params:
                clean_params["cronExpression"] = "0 9 * * *"  # Default: daily at 9 AM
                
        elif node_type == "n8n-nodes-base.function":
            # Ensure function has code
            if "functionCode" not in clean_params:
                clean_params["functionCode"] = "return items;"
                
        elif node_type == "n8n-nodes-base.if":
            # Ensure IF node has conditions
            if "conditions" not in clean_params:
                clean_params["conditions"] = {
                    "string": [
                        {
                            "value1": "={{$json.status}}",
                            "operation": "equal",
                            "value2": "success"
                        }
                    ]
                }
        
        return clean_params

    def _build_intelligent_connections(
        self, analysis: Dict[str, Any], node_map: Dict[str, N8NNode]
    ) -> Dict[str, Any]:
        """Build intelligent connections ensuring proper workflow flow"""
        connections = {}
        
        # Get specified connections first
        specified_connections = set()
        for conn_spec in analysis.get("connections", []):
            source_id = conn_spec["source"]
            target_id = conn_spec["target"]
            
            # Validate nodes exist
            if source_id not in node_map or target_id not in node_map:
                continue
                
            specified_connections.add((source_id, target_id))
            
            # Initialize connection structure
            if source_id not in connections:
                connections[source_id] = {"main": [[]]}
            
            connections[source_id]["main"][0].append({
                "node": target_id,
                "type": "main",
                "index": 0,
            })
        
        # Auto-connect nodes that aren't connected but should be (based on node types)
        node_list = list(node_map.values())
        
        for i in range(len(node_list) - 1):
            current_node = node_list[i]
            next_node = node_list[i + 1]
            
            # Skip if already connected
            if (current_node.id, next_node.id) in specified_connections:
                continue
            
            # Connect based on node type logic
            should_connect = self._should_auto_connect(current_node.type, next_node.type)
            
            if should_connect:
                if current_node.id not in connections:
                    connections[current_node.id] = {"main": [[]]}
                
                connections[current_node.id]["main"][0].append({
                    "node": next_node.id,
                    "type": "main",
                    "index": 0,
                })
        
        return connections

    def _should_auto_connect(self, source_type: str, target_type: str) -> bool:
        """Determine if two node types should be auto-connected"""
        
        # Triggers should connect to first processing node
        if "trigger" in source_type.lower():
            return True
            
        # HTTP requests often connect to functions or other processors
        if "httpRequest" in source_type:
            return target_type in ["n8n-nodes-base.function", "n8n-nodes-base.set", "n8n-nodes-base.if"]
            
        # Functions often connect to output nodes
        if "function" in source_type:
            return "telegram" in target_type or "slack" in target_type or "email" in target_type
            
        # Set nodes connect to most things
        if "set" in source_type:
            return True
            
        # Default: connect sequential nodes unless they're both output types
        output_types = ["telegram", "slack", "email", "webhook", "respondToWebhook"]
        both_output = any(t in source_type for t in output_types) and any(t in target_type for t in output_types)
        
        return not both_output

    def _validate_and_optimize_connections(
        self, connections: Dict[str, Any], node_map: Dict[str, N8NNode]
    ) -> Dict[str, Any]:
        """Validate connections and fix common issues"""
        
        optimized = {}
        
        for source_id, conn_data in connections.items():
            if source_id not in node_map:
                continue  # Skip invalid source nodes
            
            optimized[source_id] = {"main": [[]]}
            
            # Validate each connection
            for connection in conn_data.get("main", [[]])[0]:
                target_id = connection.get("node")
                
                if target_id and target_id in node_map:
                    optimized[source_id]["main"][0].append({
                        "node": target_id,
                        "type": "main",
                        "index": 0,
                    })
        
        # Ensure no orphaned nodes (connect any unconnected nodes)
        connected_nodes = set()
        for source_id, conn_data in optimized.items():
            connected_nodes.add(source_id)
            for connection in conn_data.get("main", [[]])[0]:
                connected_nodes.add(connection["node"])
        
        # Connect any orphaned nodes to the workflow
        all_nodes = list(node_map.keys())
        orphaned = [node_id for node_id in all_nodes if node_id not in connected_nodes]
        
        if orphaned and all_nodes:
            # Connect orphaned nodes to the last connected node
            if optimized:
                last_connected = list(optimized.keys())[-1]
                for orphan_id in orphaned:
                    if last_connected not in optimized:
                        optimized[last_connected] = {"main": [[]]}
                    
                    optimized[last_connected]["main"][0].append({
                        "node": orphan_id,
                        "type": "main", 
                        "index": 0,
                    })
        
        return optimized


async def generate_workflow_from_prompt(
    user_prompt: str, 
    xai_api_key: str, 
    n8n_service: N8NService,
    mode: str = "interpret",
    node_sequence: Optional[str] = None,
    progress_callback: Optional[callable] = None
) -> Dict[str, Any]:
    """
    Advanced workflow generation with multi-stage AI processing
    """
    if progress_callback:
        progress_callback("Starting advanced workflow generation...")
    
    # Build the workflow using enhanced multi-stage Grok processing
    builder = GrokWorkflowBuilder(xai_api_key)
    workflow = await builder.build_complete_workflow(
        user_prompt, 
        mode=mode, 
        node_sequence=node_sequence,
        progress_callback=progress_callback
    )

    if progress_callback:
        progress_callback("Deploying workflow to n8n...")

    # Deploy to n8n
    result = await n8n_service.create_workflow(workflow)

    if progress_callback:
        progress_callback("Workflow successfully created!")

    return {
        "success": True,
        "workflow_id": result.get("id"),
        "workflow_name": workflow.name,
        "workflow": workflow.dict(),
        "deployed": result,
        "n8n_url": f"http://localhost:5678/workflow/{result.get('id')}",
        "enhancement_used": mode,
    }
