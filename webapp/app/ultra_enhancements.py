"""
Ultra Enhancements - Invisible Intelligence Layer

Code optimizations and agentic features that improve the system
without adding user complexity. Works silently in the background.
"""

import asyncio
import json
from typing import Dict, Any, List, Optional
from functools import lru_cache
import hashlib
import time


class IntelligentCache:
    """Smart caching for workflow generations to avoid redundant API calls"""

    def __init__(self, ttl_seconds: int = 3600):
        self.cache: Dict[str, tuple[Any, float]] = {}
        self.ttl = ttl_seconds

    def _hash_key(self, prompt: str, mode: str) -> str:
        """Create cache key from prompt + mode"""
        content = f"{prompt}:{mode}"
        return hashlib.md5(content.encode()).hexdigest()

    def get(self, prompt: str, mode: str) -> Optional[Any]:
        """Get cached result if exists and not expired"""
        key = self._hash_key(prompt, mode)
        if key in self.cache:
            result, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return result
            else:
                del self.cache[key]
        return None

    def set(self, prompt: str, mode: str, result: Any):
        """Cache a result"""
        key = self._hash_key(prompt, mode)
        self.cache[key] = (result, time.time())

    def clear_old(self):
        """Remove expired entries"""
        current_time = time.time()
        expired = [
            k for k, (_, ts) in self.cache.items() if current_time - ts > self.ttl
        ]
        for k in expired:
            del self.cache[k]


class ProactiveSuggestions:
    """Analyzes user behavior and proactively suggests workflows"""

    def __init__(self):
        self.user_patterns: Dict[str, List[str]] = {}

    def record_workflow_creation(self, user_id: str, workflow_type: str):
        """Track what types of workflows users create"""
        if user_id not in self.user_patterns:
            self.user_patterns[user_id] = []
        self.user_patterns[user_id].append(workflow_type)

    def suggest_next_workflow(self, user_id: str) -> List[str]:
        """Suggest workflows based on user history"""
        if user_id not in self.user_patterns:
            return [
                "Start with a simple schedule → email workflow",
                "Try monitoring your website uptime",
                "Automate invoice processing from email",
            ]

        patterns = self.user_patterns[user_id]

        # If user created monitoring workflow, suggest related
        if any("monitor" in p.lower() for p in patterns):
            return [
                "Add alerting to your monitoring workflow",
                "Create backup monitoring for redundancy",
                "Set up performance tracking",
            ]

        # If user created data sync, suggest enhancements
        if any("sync" in p.lower() or "api" in p.lower() for p in patterns):
            return [
                "Add error handling to your sync workflow",
                "Create rollback mechanism for failed syncs",
                "Set up data validation before sync",
            ]

        return [
            "Enhance your workflows with error handling",
            "Add notifications to track execution",
            "Create backup workflows for critical automations",
        ]


class ContextAwareAssistant:
    """AI assistant that remembers context across conversations"""

    def __init__(self):
        self.conversation_memory: Dict[str, List[Dict[str, str]]] = {}
        self.workflow_context: Dict[str, str] = {}  # session_id -> current workflow_id

    def remember_conversation(self, session_id: str, role: str, message: str):
        """Store conversation for context"""
        if session_id not in self.conversation_memory:
            self.conversation_memory[session_id] = []

        self.conversation_memory[session_id].append(
            {"role": role, "content": message, "timestamp": time.time()}
        )

        # Keep last 20 messages only
        self.conversation_memory[session_id] = self.conversation_memory[session_id][
            -20:
        ]

    def set_workflow_context(self, session_id: str, workflow_id: str):
        """Remember which workflow user is currently working on"""
        self.workflow_context[session_id] = workflow_id

    def get_context_prompt(self, session_id: str) -> str:
        """Build context-aware system prompt"""
        context_parts = []

        # Add conversation history
        if session_id in self.conversation_memory:
            recent = self.conversation_memory[session_id][-5:]
            context_parts.append("Recent conversation:")
            for msg in recent:
                context_parts.append(f"  {msg['role']}: {msg['content'][:100]}")

        # Add workflow context
        if session_id in self.workflow_context:
            context_parts.append(
                f"\nCurrently viewing workflow: {self.workflow_context[session_id]}"
            )

        return "\n".join(context_parts) if context_parts else "New conversation"


class WorkflowOptimizer:
    """Automatically optimizes workflows after generation"""

    @staticmethod
    def optimize_connections(workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Remove duplicate connections and optimize flow"""
        connections = workflow.get("connections", {})
        optimized = {}

        for source, conn_data in connections.items():
            optimized[source] = {"main": [[]]}

            # Remove duplicates
            seen_targets = set()
            for connection in conn_data.get("main", [[]])[0]:
                target = connection.get("node")
                if target and target not in seen_targets:
                    seen_targets.add(target)
                    optimized[source]["main"][0].append(connection)

        workflow["connections"] = optimized
        return workflow

    @staticmethod
    def optimize_positioning(workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize node positions for better visual flow"""
        nodes = workflow.get("nodes", [])

        # Group nodes by connection depth
        connections = workflow.get("connections", {})
        depths = {}

        # Calculate depth for each node
        def calculate_depth(node_id, visited=None):
            if visited is None:
                visited = set()
            if node_id in visited:
                return 0
            visited.add(node_id)

            # Find nodes that connect TO this node
            predecessors = [
                source
                for source, conn_data in connections.items()
                if any(c.get("node") == node_id for c in conn_data.get("main", [[]])[0])
            ]

            if not predecessors:
                return 0

            return 1 + max(
                calculate_depth(pred, visited.copy()) for pred in predecessors
            )

        for node in nodes:
            depths[node.get("id")] = calculate_depth(node.get("id"))

        # Position nodes based on depth
        depth_groups = {}
        for node_id, depth in depths.items():
            if depth not in depth_groups:
                depth_groups[depth] = []
            depth_groups[depth].append(node_id)

        # Apply positions
        for node in nodes:
            node_id = node.get("id")
            depth = depths.get(node_id, 0)
            position_in_depth = depth_groups[depth].index(node_id)

            node["position"] = [
                200 + (depth * 350),  # X: spreads horizontally by depth
                200 + (position_in_depth * 200),  # Y: stacks vertically within depth
            ]

        workflow["nodes"] = nodes
        return workflow


# Global instances (singleton pattern)
_cache = IntelligentCache(ttl_seconds=3600)
_suggestions = ProactiveSuggestions()
_context_assistant = ContextAwareAssistant()


def get_cache() -> IntelligentCache:
    """Get global cache instance"""
    return _cache


def get_suggestions() -> ProactiveSuggestions:
    """Get global suggestions engine"""
    return _suggestions


def get_context_assistant() -> ContextAwareAssistant:
    """Get global context-aware assistant"""
    return _context_assistant
