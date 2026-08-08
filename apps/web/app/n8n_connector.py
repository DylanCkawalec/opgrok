"""
N8N Deep Connector - Safe workflow connection analyzer and auto-connector

Analyzes n8n workflows and intelligently connects unconnected nodes
WITHOUT deleting or breaking existing configuration.
"""

from typing import Dict, Any, List, Set, Tuple, Optional


class N8NWorkflowAnalyzer:
    """Deep analysis of n8n workflow structure"""

    def __init__(self, workflow: Dict[str, Any]):
        self.workflow = workflow
        self.nodes = {n["id"]: n for n in workflow.get("nodes", [])}
        self.connections = workflow.get("connections", {})

    def analyze_structure(self) -> Dict[str, Any]:
        """Deep analysis of workflow structure"""

        connected_nodes = self._get_connected_nodes()
        unconnected_nodes = self._get_unconnected_nodes()
        node_types = self._analyze_node_types()
        triggers = self._find_trigger_nodes()
        outputs = self._find_output_nodes()
        processors = self._find_processor_nodes()

        return {
            "total_nodes": len(self.nodes),
            "connected_nodes": len(connected_nodes),
            "unconnected_nodes": len(unconnected_nodes),
            "triggers": triggers,
            "outputs": outputs,
            "processors": processors,
            "node_types": node_types,
            "connection_gaps": self._find_connection_gaps(),
            "suggested_connections": self._suggest_connections(),
        }

    def _get_connected_nodes(self) -> Set[str]:
        """Find all nodes that are part of the connection graph"""
        connected = set()

        for source_id, conn_data in self.connections.items():
            connected.add(source_id)
            for target in conn_data.get("main", [[]])[0]:
                connected.add(target.get("node"))

        return connected

    def _get_unconnected_nodes(self) -> List[Dict[str, Any]]:
        """Find nodes not connected to anything"""
        connected = self._get_connected_nodes()

        return [
            {"id": node_id, "name": node["name"], "type": node["type"]}
            for node_id, node in self.nodes.items()
            if node_id not in connected
        ]

    def _analyze_node_types(self) -> Dict[str, List[str]]:
        """Categorize nodes by type"""
        categories = {
            "triggers": [],
            "http": [],
            "functions": [],
            "conditions": [],
            "outputs": [],
            "data_processors": [],
            "other": [],
        }

        for node_id, node in self.nodes.items():
            node_type = node.get("type", "")

            if "trigger" in node_type.lower():
                categories["triggers"].append(node_id)
            elif "http" in node_type.lower():
                categories["http"].append(node_id)
            elif "function" in node_type.lower():
                categories["functions"].append(node_id)
            elif "if" in node_type.lower() or "switch" in node_type.lower():
                categories["conditions"].append(node_id)
            elif any(
                x in node_type.lower()
                for x in ["telegram", "slack", "email", "webhook"]
            ):
                categories["outputs"].append(node_id)
            elif any(x in node_type.lower() for x in ["set", "merge", "split"]):
                categories["data_processors"].append(node_id)
            else:
                categories["other"].append(node_id)

        return categories

    def _find_trigger_nodes(self) -> List[str]:
        """Find all trigger/start nodes"""
        return [
            node_id
            for node_id, node in self.nodes.items()
            if "trigger" in node.get("type", "").lower()
            or "webhook" in node.get("type", "").lower()
        ]

    def _find_output_nodes(self) -> List[str]:
        """Find all output/end nodes"""
        return [
            node_id
            for node_id, node in self.nodes.items()
            if any(
                x in node.get("type", "").lower()
                for x in ["telegram", "slack", "email", "respond", "write"]
            )
        ]

    def _find_processor_nodes(self) -> List[str]:
        """Find middle processing nodes"""
        triggers = set(self._find_trigger_nodes())
        outputs = set(self._find_output_nodes())

        return [
            node_id
            for node_id in self.nodes.keys()
            if node_id not in triggers and node_id not in outputs
        ]

    def _find_connection_gaps(self) -> List[Dict[str, Any]]:
        """Find logical connection gaps that should be filled"""
        gaps = []
        node_list = list(self.nodes.values())

        # Check for sequential nodes that aren't connected
        for i in range(len(node_list) - 1):
            current = node_list[i]
            next_node = node_list[i + 1]

            current_id = current["id"]
            next_id = next_node["id"]

            # Check if current connects to next
            current_connections = self.connections.get(current_id, {}).get(
                "main", [[]]
            )[0]
            connected_to_next = any(
                c.get("node") == next_id for c in current_connections
            )

            if not connected_to_next:
                gaps.append(
                    {
                        "source": current_id,
                        "target": next_id,
                        "reason": "Sequential nodes not connected",
                    }
                )

        return gaps

    def _suggest_connections(self) -> List[Dict[str, str]]:
        """Intelligently suggest connections based on node types"""
        suggestions = []

        triggers = self._find_trigger_nodes()
        outputs = self._find_output_nodes()
        processors = self._find_processor_nodes()

        # If trigger exists but not connected, connect to first processor
        for trigger_id in triggers:
            if (
                trigger_id not in self.connections
                or not self.connections[trigger_id].get("main", [[]])[0]
            ):
                if processors:
                    suggestions.append(
                        {
                            "source": trigger_id,
                            "target": processors[0],
                            "reason": "Connect trigger to first processor",
                        }
                    )

        # Connect unconnected processors in sequence
        unconnected_processors = [
            p
            for p in processors
            if p not in self.connections or not self.connections[p].get("main", [[]])[0]
        ]

        for i, proc_id in enumerate(unconnected_processors):
            if i < len(unconnected_processors) - 1:
                suggestions.append(
                    {
                        "source": proc_id,
                        "target": unconnected_processors[i + 1],
                        "reason": "Connect processors in sequence",
                    }
                )
            elif outputs:
                suggestions.append(
                    {
                        "source": proc_id,
                        "target": outputs[0],
                        "reason": "Connect last processor to output",
                    }
                )

        return suggestions


class N8NAutoConnector:
    """Automatically connects unconnected nodes intelligently"""

    @staticmethod
    def connect_all(workflow: Dict[str, Any]) -> Dict[str, Any]:
        """
        Intelligently connect ALL unconnected nodes
        Returns: Modified workflow with new connections (preserves all existing data!)
        """
        analyzer = N8NWorkflowAnalyzer(workflow)
        analysis = analyzer.analyze_structure()

        # Get current connections (preserve them!)
        connections = dict(workflow.get("connections", {}))

        # Apply suggested connections
        for suggestion in analysis["suggested_connections"]:
            source = suggestion["source"]
            target = suggestion["target"]

            # Initialize if doesn't exist
            if source not in connections:
                connections[source] = {"main": [[]]}

            # Check if connection already exists
            existing_targets = [
                c.get("node") for c in connections[source].get("main", [[]])[0]
            ]

            # Only add if not already connected
            if target not in existing_targets:
                connections[source]["main"][0].append(
                    {"node": target, "type": "main", "index": 0}
                )

        # Return workflow with updated connections (PRESERVE everything else!)
        return {
            **workflow,  # Keep ALL existing data
            "connections": connections,  # Only update connections
        }

    @staticmethod
    def create_connection_report(workflow: Dict[str, Any]) -> str:
        """Generate human-readable report of connections"""
        analyzer = N8NWorkflowAnalyzer(workflow)
        analysis = analyzer.analyze_structure()

        lines = [
            f"📊 Workflow Analysis: {workflow.get('name', 'Unnamed')}",
            f"",
            f"Nodes: {analysis['total_nodes']}",
            f"Connected: {analysis['connected_nodes']}",
            f"Unconnected: {analysis['unconnected_nodes']}",
            f"",
            f"Node Types:",
            f"  Triggers: {len(analysis['triggers'])}",
            f"  Processors: {len(analysis['processors'])}",
            f"  Outputs: {len(analysis['outputs'])}",
        ]

        if analysis["suggested_connections"]:
            lines.append(f"")
            lines.append(
                f"💡 Suggested Connections ({len(analysis['suggested_connections'])}):"
            )
            for conn in analysis["suggested_connections"]:
                source_name = analyzer.nodes[conn["source"]]["name"]
                target_name = analyzer.nodes[conn["target"]]["name"]
                lines.append(f"  {source_name} → {target_name}")
                lines.append(f"    Reason: {conn['reason']}")

        return "\n".join(lines)


async def auto_connect_workflow(workflow_id: str, n8n_service) -> Dict[str, Any]:
    """
    Main function: Automatically connect all unconnected nodes in a workflow
    SAFE: Preserves all existing nodes, parameters, and connections
    """
    # Get current workflow
    current_workflow = await n8n_service.get_workflow(workflow_id)

    # Create connection report BEFORE
    analyzer = N8NWorkflowAnalyzer(current_workflow)
    before_analysis = analyzer.analyze_structure()

    # Auto-connect
    connector = N8NAutoConnector()
    updated_workflow = connector.connect_all(current_workflow)

    # Update in n8n (SAFE - only updates connections field)
    import httpx

    headers = n8n_service._get_headers()
    auth = n8n_service._get_auth()

    async with httpx.AsyncClient() as client:
        # n8n requires PUT with FULL workflow object (not PATCH)
        response = await client.put(
            f"{n8n_service.api_url}/workflows/{workflow_id}",
            headers=headers,
            auth=auth,
            json={
                "name": updated_workflow["name"],
                "nodes": updated_workflow["nodes"],
                "connections": updated_workflow["connections"],
                "active": updated_workflow.get("active", False),
                "settings": updated_workflow.get("settings", {}),
                "staticData": updated_workflow.get("staticData"),
                "tags": updated_workflow.get("tags", [])
            },
        )
        response.raise_for_status()
        result = response.json()

    # Analyze AFTER
    after_analyzer = N8NWorkflowAnalyzer(result)
    after_analysis = after_analyzer.analyze_structure()

    return {
        "success": True,
        "workflow_id": workflow_id,
        "workflow_name": current_workflow.get("name"),
        "before": {
            "connected": before_analysis["connected_nodes"],
            "unconnected": before_analysis["unconnected_nodes"],
        },
        "after": {
            "connected": after_analysis["connected_nodes"],
            "unconnected": after_analysis["unconnected_nodes"],
        },
        "connections_added": after_analysis["connected_nodes"]
        - before_analysis["connected_nodes"],
        "report": connector.create_connection_report(result),
        "n8n_url": f"http://localhost:5678/workflow/{workflow_id}",
    }
