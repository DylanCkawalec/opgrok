"""
Workflow Intelligence - Complete Deep n8n Editor Integration

Grok becomes embedded in n8n, understanding and modifying workflows through:
1. Real-time workflow data fetching
2. Deep context awareness
3. Command parsing and execution
4. Safe API updates to n8n
"""

import json
import re
from typing import Dict, Any, List, Optional
import httpx


class WorkflowIntelligenceEngine:
    """Complete integration between Grok AI and n8n workflow editor"""

    def __init__(self, xai_api_key: str, n8n_service):
        self.api_key = xai_api_key
        self.n8n = n8n_service
        self.api_url = "https://api.x.ai/v1/chat/completions"
        self.workflow_contexts: Dict[str, List[Dict]] = {}

    async def chat_with_editor(
        self, workflow_id: str, user_message: str
    ) -> Dict[str, Any]:
        """
        Main method: Chat that knows the workflow and can modify it
        """
        # Fetch current workflow state from n8n
        workflow = await self.n8n.get_workflow(workflow_id)

        # Build comprehensive context
        editor_context = self._build_complete_context(workflow)

        # Get conversation history
        history = self.workflow_contexts.get(workflow_id, [])

        # Query Grok with full context
        grok_response = await self._query_grok_with_context(
            editor_context, history, user_message
        )

        # Parse for modification commands
        modifications = self._extract_modification_intent(grok_response, workflow)

        # Execute modifications if found
        changes_made = []
        if modifications:
            changes_made = await self._apply_modifications(workflow_id, modifications)

        # Update conversation history
        if workflow_id not in self.workflow_contexts:
            self.workflow_contexts[workflow_id] = []

        self.workflow_contexts[workflow_id].extend(
            [
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": grok_response},
            ]
        )
        self.workflow_contexts[workflow_id] = self.workflow_contexts[workflow_id][-10:]

        return {
            "assistant": grok_response,
            "workflow_modified": len(changes_made) > 0,
            "changes": changes_made,
            "workflow_id": workflow_id,
            "n8n_url": f"http://localhost:5678/workflow/{workflow_id}",
        }

    def _build_complete_context(self, workflow: Dict[str, Any]) -> str:
        """Build rich context with ALL workflow data"""

        nodes = workflow.get("nodes", [])
        connections = workflow.get("connections", {})

        context_parts = [
            f"You are inside the n8n editor for workflow: {workflow.get('name')}",
            f"",
            f"WORKFLOW DATA:",
            f"• ID: {workflow.get('id')}",
            f"• Nodes: {len(nodes)}",
            f"• Active: {workflow.get('active')}",
            f"",
            f"NODES (with complete details):",
        ]

        for i, node in enumerate(nodes):
            context_parts.append(f"\n{i+1}. {node.get('name')} (ID: {node.get('id')})")
            context_parts.append(f"   Type: {node.get('type')}")
            context_parts.append(f"   Position: {node.get('position')}")

            params = node.get("parameters", {})
            if params:
                context_parts.append(
                    f"   Parameters: {json.dumps(params, indent=6)[:200]}"
                )

        context_parts.append(f"\nCONNECTIONS:")
        for source_id, conn_data in connections.items():
            source_name = next(
                (n.get("name") for n in nodes if n.get("id") == source_id), source_id
            )
            for target in conn_data.get("main", [[]])[0]:
                target_id = target.get("node")
                target_name = next(
                    (n.get("name") for n in nodes if n.get("id") == target_id),
                    target_id,
                )
                context_parts.append(f"  {source_name} → {target_name}")

        context_parts.append(
            f"""

You can help users by:
1. Explaining the workflow
2. Suggesting improvements  
3. Identifying what to modify

When user asks to modify something, be specific about:
- Which node (use the ID)
- What parameter to change
- What the new value should be

Example: "To run every 30 minutes, change the schedule node's cronExpression to '*/30 * * * *'"
"""
        )

        return "\n".join(context_parts)

    async def _query_grok_with_context(
        self, system_context: str, history: List[Dict], user_message: str
    ) -> str:
        """Query Grok with full workflow context"""

        messages = [{"role": "system", "content": system_context}]
        messages.extend(history[-6:])  # Last 6 messages
        messages.append({"role": "user", "content": user_message})

        async with httpx.AsyncClient(timeout=45.0) as client:
            response = await client.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "grok-4-fast-non-reasoning",
                    "messages": messages,
                    "temperature": 0.3,
                    "max_tokens": 1536,
                },
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    def _extract_modification_intent(
        self, grok_response: str, workflow: Dict[str, Any]
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Extract actionable modifications from Grok's response

        Looks for patterns like:
        - "change X to Y"
        - "update parameter Z"
        - "set schedule to..."
        """
        modifications = []

        # Pattern: change/update schedule to every X minutes
        if re.search(
            r"(change|update|modify|set).*(schedule|cron)", grok_response, re.I
        ):
            if re.search(r"every (\d+) minute", grok_response, re.I):
                match = re.search(r"every (\d+) minute", grok_response, re.I)
                minutes = match.group(1)

                # Find schedule node
                schedule_node = next(
                    (
                        n
                        for n in workflow.get("nodes", [])
                        if "schedule" in n.get("type", "").lower()
                        or "trigger" in n.get("type", "").lower()
                    ),
                    None,
                )
                if schedule_node:
                    modifications.append(
                        {
                            "type": "update_node",
                            "node_id": schedule_node.get("id"),
                            "field": "schedule",
                            "value": f"every {minutes} minute",
                        }
                    )
