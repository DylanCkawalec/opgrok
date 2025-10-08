"""
Workflow Modification Engine

Deep integration with n8n API to actually modify workflows
based on natural language AI understanding.
"""

import json
from typing import Dict, Any, List, Optional
import httpx


class WorkflowModificationEngine:
    """Executes actual workflow modifications in n8n based on AI analysis"""

    def __init__(self, n8n_service):
        self.n8n = n8n_service

    async def analyze_modification_request(
        self, workflow_id: str, user_request: str, xai_api_key: str
    ) -> Dict[str, Any]:
        """
        Stage 1: Get workflow + Use Grok to understand what needs to change
        """
        # Get current workflow state
        current_workflow = await self.n8n.get_workflow(workflow_id)

        # Create detailed workflow summary for AI context
        workflow_summary = self._create_workflow_summary(current_workflow)

        # Ask Grok what to change
        system_prompt = f"""You are an n8n workflow modification expert. You can ACTUALLY modify workflows through API calls.

CURRENT WORKFLOW SUMMARY:
{workflow_summary}

FULL WORKFLOW DATA:
{json.dumps(current_workflow, indent=2)}

Analyze the user's modification request and respond with EXECUTABLE modifications in JSON:

{{
  "action": "update|add_node|remove_node|change_schedule|modify_connection",
  "changes": [
    {{
      "operation": "update_node_parameter",
      "node_id": "schedule1",
      "parameter_path": "cronExpression",
      "old_value": "0 * * * *",
      "new_value": "*/30 * * * *",
      "reason": "Change from hourly to every 30 minutes"
    }}
  ],
  "summary": "Changed schedule from hourly to every 30 minutes",
  "validation": {{
    "safe": true,
    "breaking_changes": false,
    "requires_credentials": false
  }}
}}

Be SPECIFIC with node IDs, parameter paths, and exact values.
Only suggest changes that are SAFE and won't break the workflow."""

        async with httpx.AsyncClient(timeout=45.0) as client:
            response = await client.post(
                "https://api.x.ai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {xai_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "grok-4-fast-non-reasoning",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_request},
                    ],
                    "temperature": 0.2,
                    "max_tokens": 2048,
                },
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]

            # Parse AI response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            return json.loads(content)

    def _create_workflow_summary(self, workflow: Dict[str, Any]) -> str:
        """Create human-readable workflow summary for AI context"""
        nodes = workflow.get("nodes", [])
        connections = workflow.get("connections", {})

        summary_parts = [
            f"Workflow: {workflow.get('name', 'Unnamed')}",
            f"Total Nodes: {len(nodes)}",
            f"Status: {'Active' if workflow.get('active') else 'Inactive'}",
            "",
            "NODES:",
        ]

        for i, node in enumerate(nodes):
            node_type = node.get("type", "").replace("n8n-nodes-base.", "")
            params = node.get("parameters", {})

            # Extract key parameters
            key_params = []
            if "cronExpression" in params:
                key_params.append(f"schedule='{params['cronExpression']}'")
            if "url" in params:
                key_params.append(f"url='{params.get('url', '')[:50]}'")
            if "method" in params:
                key_params.append(f"method={params['method']}")
            if "chatId" in params:
                key_params.append(f"chatId='{params['chatId']}'")

            param_str = ", ".join(key_params) if key_params else "no params"

            summary_parts.append(
                f"{i+1}. [{node.get('id')}] {node.get('name')} ({node_type}): {param_str}"
            )

        summary_parts.append("")
        summary_parts.append("CONNECTIONS:")
        for source, conn_data in connections.items():
            targets = conn_data.get("main", [[]])[0]
            for target in targets:
                summary_parts.append(f"  {source} → {target.get('node')}")

        return "\n".join(summary_parts)

    async def execute_modifications(
        self, workflow_id: str, modifications: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Stage 2: Execute the modifications by calling n8n API
        """
        # Get current workflow
        current_workflow = await self.n8n.get_workflow(workflow_id)

        # Apply each modification
        for change in modifications.get("changes", []):
            operation = change.get("operation")

            if operation == "update_node_parameter":
                self._apply_parameter_update(current_workflow, change)
            elif operation == "update_schedule":
                self._apply_schedule_update(current_workflow, change)
            elif operation == "add_node":
                self._apply_add_node(current_workflow, change)
            elif operation == "remove_node":
                self._apply_remove_node(current_workflow, change)
            elif operation == "change_connection":
                self._apply_connection_change(current_workflow, change)

        # Update workflow in n8n (send as dict, not N8NWorkflow object)
        # Use PATCH to update only the changed fields
        import httpx

        headers = self.n8n._get_headers()
        auth = self.n8n._get_auth()

        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{self.n8n.api_url}/workflows/{workflow_id}",
                headers=headers,
                auth=auth,
                json={
                    "nodes": current_workflow.get("nodes"),
                    "connections": current_workflow.get("connections"),
                    "settings": current_workflow.get("settings", {}),
                },
            )
            response.raise_for_status()
            updated = response.json()

        return {
            "success": True,
            "workflow_id": workflow_id,
            "modifications_applied": len(modifications.get("changes", [])),
            "summary": modifications.get("summary", "Workflow updated"),
            "updated_workflow": updated,
        }

    def _apply_parameter_update(self, workflow: Dict[str, Any], change: Dict[str, Any]):
        """Update a specific node parameter"""
        node_id = change.get("node_id")
        param_path = change.get("parameter_path")
        new_value = change.get("new_value")

        # Find the node
        nodes = workflow.get("nodes", [])
        for node in nodes:
            if node.get("id") == node_id:
                # Navigate to parameter and update
                params = node.get("parameters", {})

                # Handle nested paths (e.g., "rule.interval.0.seconds")
                if "." in param_path:
                    parts = param_path.split(".")
                    current = params
                    for part in parts[:-1]:
                        if part.isdigit():
                            current = current[int(part)]
                        else:
                            if part not in current:
                                current[part] = {}
                            current = current[part]

                    last_part = parts[-1]
                    if last_part.isdigit():
                        current[int(last_part)] = new_value
                    else:
                        current[last_part] = new_value
                else:
                    params[param_path] = new_value

                node["parameters"] = params
                break

    def _apply_schedule_update(self, workflow: Dict[str, Any], change: Dict[str, Any]):
        """Update schedule/cron expressions"""
        node_id = change.get("node_id") or change.get("target")
        new_schedule = change.get("new_value")

        nodes = workflow.get("nodes", [])
        for node in nodes:
            if (
                node.get("id") == node_id
                or "schedule" in node.get("type", "").lower()
                or "trigger" in node.get("name", "").lower()
            ):

                params = node.get("parameters", {})
                params["cronExpression"] = new_schedule
                node["parameters"] = params
                break

    def _apply_add_node(self, workflow: Dict[str, Any], change: Dict[str, Any]):
        """Add a new node to the workflow"""
        new_node = change.get("node_config", {})

        # Ensure required fields
        if not new_node.get("id"):
            import uuid

            new_node["id"] = f"node_{uuid.uuid4().hex[:8]}"

        if not new_node.get("position"):
            # Position at end
            existing_nodes = workflow.get("nodes", [])
            new_node["position"] = [200 + (len(existing_nodes) * 300), 200]

        workflow.get("nodes", []).append(new_node)

    def _apply_remove_node(self, workflow: Dict[str, Any], change: Dict[str, Any]):
        """Remove a node from the workflow"""
        node_id = change.get("node_id")

        # Remove from nodes list
        nodes = workflow.get("nodes", [])
        workflow["nodes"] = [n for n in nodes if n.get("id") != node_id]

        # Remove from connections
        connections = workflow.get("connections", {})
        if node_id in connections:
            del connections[node_id]

        # Remove connections TO this node
        for source, conn_data in list(connections.items()):
            for output_type, output_list in list(conn_data.items()):
                for i, target_list in enumerate(output_list):
                    output_list[i] = [
                        t for t in target_list if t.get("node") != node_id
                    ]

    def _apply_connection_change(
        self, workflow: Dict[str, Any], change: Dict[str, Any]
    ):
        """Add or modify node connections"""
        source_id = change.get("source_node")
        target_id = change.get("target_node")

        connections = workflow.get("connections", {})

        if source_id not in connections:
            connections[source_id] = {"main": [[]]}

        # Add connection if not exists
        existing_targets = [
            t.get("node") for t in connections[source_id].get("main", [[]])[0]
        ]

        if target_id not in existing_targets:
            connections[source_id]["main"][0].append(
                {"node": target_id, "type": "main", "index": 0}
            )


async def chat_modify_workflow(
    workflow_id: str, user_message: str, xai_api_key: str, n8n_service
) -> Dict[str, Any]:
    """
    Main function: Chat-based workflow modification that ACTUALLY updates n8n
    """
    engine = WorkflowModificationEngine(n8n_service)

    # Stage 1: AI analyzes what to change
    modification_plan = await engine.analyze_modification_request(
        workflow_id, user_message, xai_api_key
    )

    # Stage 2: Execute the changes in n8n
    if modification_plan.get("validation", {}).get("safe", True):
        result = await engine.execute_modifications(workflow_id, modification_plan)
        return {
            **result,
            "assistant_response": f"✅ I've modified your workflow! {modification_plan.get('summary', '')}\n\nChanges applied: {result.get('modifications_applied', 0)}\n\nRefresh the n8n editor to see the updates.",
            "modifications": modification_plan,
        }
    else:
        return {
            "success": False,
            "assistant_response": f"⚠️ These modifications might break the workflow. Please review:\n{modification_plan.get('summary', '')}",
            "modifications": modification_plan,
            "requires_confirmation": True,
        }
