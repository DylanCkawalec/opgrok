"""
Agentic Workflow Connector - AI-Powered Connection System

Uses Grok to:
1. Analyze workflow nodes and their purposes
2. Decide HOW nodes should connect (not hardcoded rules!)
3. Generate executable Python connection code
4. Verify connections appear in n8n visual editor
"""

import json
from typing import Dict, Any, List
import httpx


class AgenticWorkflowConnector:
    """AI-powered connection system - Grok decides, Python executes"""
    
    def __init__(self, xai_api_key: str, n8n_service):
        self.api_key = xai_api_key
        self.n8n = n8n_service
        self.api_url = "https://api.x.ai/v1/chat/completions"
    
    async def intelligent_connect(self, workflow_id: str) -> Dict[str, Any]:
        """
        Main method: Use AI to intelligently connect workflow nodes
        
        Process:
        1. Fetch workflow from n8n
        2. Send to Grok for analysis
        3. Grok returns connection instructions
        4. Execute connections
        5. Verify in n8n
        """
        
        # Step 1: Get workflow
        workflow = await self.n8n.get_workflow(workflow_id)
        
        # Step 2: Create rich context for Grok
        analysis_context = self._build_workflow_context(workflow)
        
        # Step 3: Ask Grok to decide connections
        connection_plan = await self._ask_grok_for_connections(analysis_context)
        
        # Step 4: Execute the plan
        execution_result = await self._execute_connection_plan(
            workflow_id,
            workflow,
            connection_plan
        )
        
        # Step 5: Verify in n8n
        verification = await self._verify_connections(workflow_id)
        
        return {
            "success": execution_result["success"],
            "ai_analysis": connection_plan.get("reasoning", ""),
            "connections_made": execution_result["connections_made"],
            "verification": verification,
            "workflow_id": workflow_id,
            "n8n_url": f"http://localhost:5678/workflow/{workflow_id}"
        }
    
    def _build_workflow_context(self, workflow: Dict[str, Any]) -> str:
        """Build detailed context for AI analysis"""
        
        nodes = workflow.get("nodes", [])
        current_connections = workflow.get("connections", {})
        
        context_lines = [
            "WORKFLOW TO ANALYZE:",
            f"Name: {workflow.get('name')}",
            f"Total Nodes: {len(nodes)}",
            "",
            "NODES (with types and purposes):"
        ]
        
        for i, node in enumerate(nodes):
            node_type = node.get("type", "").replace("n8n-nodes-base.", "")
            params = node.get("parameters", {})
            
            # Extract key info
            purpose = ""
            if "schedule" in node_type.lower():
                interval = params.get("rule", {}).get("interval", [{}])[0]
                purpose = f"Triggers {interval}"
            elif "http" in node_type.lower():
                url = params.get("url", "")[:50]
                purpose = f"Fetches from {url}"
            elif "function" in node_type.lower():
                purpose = "Processes/transforms data"
            elif "telegram" in node_type.lower():
                purpose = f"Sends to Telegram"
            elif "email" in node_type.lower():
                purpose = "Sends email"
            
            context_lines.append(
                f"{i+1}. [{node.get('id')}] {node.get('name')} ({node_type})"
            )
            if purpose:
                context_lines.append(f"   Purpose: {purpose}")
        
        context_lines.append("\nCURRENT CONNECTIONS:")
        if current_connections:
            for src, conn in current_connections.items():
                targets = [t.get("node") for t in conn.get("main", [[]])[0]]
                context_lines.append(f"  {src} → {targets}")
        else:
            context_lines.append("  None - needs connections!")
        
        return "\n".join(context_lines)
    
    async def _ask_grok_for_connections(self, context: str) -> Dict[str, Any]:
        """
        Ask Grok to analyze and decide HOW to connect nodes
        
        Grok acts as intelligent architect, not following rules
        """
        
        system_prompt = """You are an n8n workflow architect AI. Analyze the workflow and decide HOW to connect nodes.

Think about:
1. Data flow - where does data come from and go to?
2. Logical sequence - what order makes sense?
3. Error handling - which nodes need error paths?
4. Purpose - what is each node trying to achieve?

Respond with JSON:
{
  "reasoning": "explain your thinking about the optimal flow",
  "connections": [
    {
      "from": "source_node_id",
      "to": "target_node_id",
      "reason": "why this connection makes sense"
    }
  ],
  "warnings": ["any potential issues"],
  "confidence": 0.0-1.0
}

Be SPECIFIC with node IDs from the workflow.
Think like an engineer - what's the optimal data flow?
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": context}
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
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            return json.loads(content)
    
    async def _execute_connection_plan(
        self,
        workflow_id: str,
        workflow: Dict[str, Any],
        plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute the AI's connection plan via n8n API
        """
        
        # Build connections from AI's plan
        connections = dict(workflow.get("connections", {}))
        connections_made = 0
        
        for conn in plan.get("connections", []):
            source_id = conn.get("from")
            target_id = conn.get("to")
            
            if not source_id or not target_id:
                continue
            
            # Initialize if needed
            if source_id not in connections:
                connections[source_id] = {"main": [[]]}
            
            # Check if already exists
            existing = [t.get("node") for t in connections[source_id].get("main", [[]])[0]]
            
            if target_id not in existing:
                connections[source_id]["main"][0].append({
                    "node": target_id,
                    "type": "main",
                    "index": 0
                })
                connections_made += 1
        
        # Update workflow via n8n API (using PUT with full object)
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.n8n.api_url}/workflows/{workflow_id}",
                headers=self.n8n._get_headers(),
                auth=self.n8n._get_auth(),
                json={
                    "name": workflow["name"],
                    "nodes": workflow["nodes"],
                    "connections": connections,
                    "active": workflow.get("active", False),
                    "settings": workflow.get("settings", {}),
                    "staticData": workflow.get("staticData"),
                    "tags": workflow.get("tags", [])
                }
            )
            
            response.raise_for_status()  # Raise on error
            
            return {
                "success": True,
                "connections_made": connections_made,
                "updated_workflow": response.json()
            }
    
    async def _verify_connections(self, workflow_id: str) -> Dict[str, Any]:
        """
        Verify connections actually appear in n8n
        """
        
        # Fetch fresh from n8n
        workflow = await self.n8n.get_workflow(workflow_id)
        
        connections = workflow.get("connections", {})
        nodes = workflow.get("nodes", [])
        
        # Count what's actually connected
        connected_nodes = set()
        for src, conn_data in connections.items():
            connected_nodes.add(src)
            for target in conn_data.get("main", [[]])[0]:
                connected_nodes.add(target.get("node"))
        
        return {
            "total_nodes": len(nodes),
            "connected_nodes": len(connected_nodes),
            "connection_sources": len(connections),
            "visual_refresh_needed": True,  # User must refresh n8n editor
            "all_connected": len(connected_nodes) == len(nodes)
        }


async def agentic_connect_workflow(workflow_id: str, xai_api_key: str, n8n_service) -> Dict[str, Any]:
    """
    Main function: AI-powered intelligent workflow connection
    """
    connector = AgenticWorkflowConnector(xai_api_key, n8n_service)
    return await connector.intelligent_connect(workflow_id)
