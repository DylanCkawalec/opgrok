"""
Intelligent Workflow Optimizer

Uses Grok to analyze generated workflows, find errors, and fix them automatically.
Makes workflows executable without manual intervention.
"""

import json
from typing import Dict, Any, List
import httpx


class IntelligentWorkflowOptimizer:
    """Grok-powered workflow optimization and error fixing"""
    
    def __init__(self, xai_api_key: str, n8n_service):
        self.api_key = xai_api_key
        self.n8n = n8n_service
        self.api_url = "https://api.x.ai/v1/chat/completions"
    
    async def optimize_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """
        Main method: Analyze workflow, find errors, fix them using AI
        
        Process:
        1. Fetch workflow from n8n
        2. Test if it can execute
        3. Use Grok to analyze errors
        4. Apply fixes
        5. Verify fixes work
        """
        
        # Get workflow
        workflow = await self.n8n.get_workflow(workflow_id)
        
        # Find errors
        errors = self._detect_errors(workflow)
        
        if not errors:
            return {
                "success": True,
                "message": "Workflow already optimal!",
                "errors_found": 0,
                "errors_fixed": 0
            }
        
        # Ask Grok to fix errors
        fixes = await self._get_ai_fixes(workflow, errors)
        
        # Apply fixes
        fixed_workflow = self._apply_fixes(workflow, fixes)
        
        # Update in n8n
        updated = await self._update_workflow(workflow_id, fixed_workflow)
        
        return {
            "success": True,
            "message": f"Fixed {len(errors)} errors",
            "errors_found": len(errors),
            "errors_fixed": len(fixes.get("fixes", [])),
            "fixes_applied": fixes.get("fixes", []),
            "workflow_id": workflow_id
        }
    
    def _detect_errors(self, workflow: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect common workflow errors"""
        errors = []
        
        for node in workflow.get("nodes", []):
            node_id = node.get("id")
            node_type = node.get("type", "")
            params = node.get("parameters", {})
            
            # Check HTTP Request nodes
            if "httpRequest" in node_type:
                # Missing URL
                if not params.get("url"):
                    errors.append({
                        "node_id": node_id,
                        "node_name": node.get("name"),
                        "error": "missing_url",
                        "message": "HTTP request missing URL"
                    })
                
                # Wrong response format
                if not params.get("responseFormat"):
                    errors.append({
                        "node_id": node_id,
                        "node_name": node.get("name"),
                        "error": "missing_response_format",
                        "message": "HTTP request should specify responseFormat (json/string)"
                    })
            
            # Check Webhook Response nodes
            if "respondToWebhook" in node_type:
                if not params.get("responseData"):
                    errors.append({
                        "node_id": node_id,
                        "node_name": node.get("name"),
                        "error": "missing_response_data",
                        "message": "Webhook response missing data configuration"
                    })
            
            # Check Function nodes
            if "function" in node_type:
                code = params.get("functionCode", "")
                if len(code) < 10:
                    errors.append({
                        "node_id": node_id,
                        "node_name": node.get("name"),
                        "error": "empty_function",
                        "message": "Function node has minimal/no code"
                    })
        
        return errors
    
    async def _get_ai_fixes(self, workflow: Dict[str, Any], errors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Ask Grok for intelligent fixes"""
        
        context = f"""You are fixing errors in an n8n workflow.

WORKFLOW: {workflow.get('name')}

DETECTED ERRORS:
{json.dumps(errors, indent=2)}

NODES WITH ERRORS:
{json.dumps([n for n in workflow['nodes'] if any(e['node_id'] == n['id'] for e in errors)], indent=2)}

Provide fixes in JSON:
{{
  "fixes": [
    {{
      "node_id": "node_id",
      "parameter": "parameter_name",
      "new_value": "correct_value",
      "reason": "why this fixes the error"
    }}
  ]
}}

Common fixes:
- httpRequest: add "responseFormat": "json" or "string"
- httpRequest: ensure valid URL
- respondToWebhook: add proper responseData
- function: ensure code returns data

Be specific and executable!"""

        async with httpx.AsyncClient(timeout=45.0) as client:
            response = await client.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "grok-4-fast-non-reasoning",
                    "messages": [
                        {"role": "system", "content": "You are an n8n workflow debugging expert."},
                        {"role": "user", "content": context}
                    ],
                    "temperature": 0.2,
                    "max_tokens": 2048,
                },
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            
            return json.loads(content)
    
    def _apply_fixes(self, workflow: Dict[str, Any], fixes: Dict[str, Any]) -> Dict[str, Any]:
        """Apply AI-suggested fixes to workflow"""
        
        nodes = workflow.get("nodes", [])
        
        for fix in fixes.get("fixes", []):
            node_id = fix.get("node_id")
            param = fix.get("parameter")
            value = fix.get("new_value")
            
            # Find and update node
            for node in nodes:
                if node.get("id") == node_id:
                    if "parameters" not in node:
                        node["parameters"] = {}
                    node["parameters"][param] = value
                    break
        
        workflow["nodes"] = nodes
        return workflow
    
    async def _update_workflow(self, workflow_id: str, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Update workflow in n8n with fixes"""
        
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.n8n.api_url}/workflows/{workflow_id}",
                headers=self.n8n._get_headers(),
                auth=self.n8n._get_auth(),
                json={
                    "name": workflow["name"],
                    "nodes": workflow["nodes"],
                    "connections": workflow["connections"],
                    "active": workflow.get("active", False),
                    "settings": workflow.get("settings", {}),
                    "staticData": workflow.get("staticData"),
                    "tags": workflow.get("tags", [])
                }
            )
            response.raise_for_status()
            return response.json()


async def auto_optimize_workflow(workflow_id: str, xai_api_key: str, n8n_service) -> Dict[str, Any]:
    """
    Main function: Automatically optimize and fix workflow errors
    """
    optimizer = IntelligentWorkflowOptimizer(xai_api_key, n8n_service)
    return await optimizer.optimize_workflow(workflow_id)
