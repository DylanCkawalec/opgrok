"""
Genius Enhancements for Grok + n8n Workflow Builder

Advanced features for workflow optimization and user experience
"""

import asyncio
import json
from typing import Dict, Any, List, Optional
import httpx


class WorkflowOptimizer:
    """Optimizes workflows after generation for better performance"""
    
    def __init__(self, xai_api_key: str):
        self.api_key = xai_api_key
        self.api_url = "https://api.x.ai/v1/chat/completions"
    
    async def optimize_workflow_performance(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Use Grok to suggest performance optimizations"""
        
        system_prompt = """You are a workflow performance expert. Analyze this n8n workflow and suggest optimizations:

1. Identify potential bottlenecks
2. Suggest caching strategies  
3. Recommend error handling improvements
4. Optimize node execution order
5. Suggest resource usage improvements

Respond with JSON:
{
  "optimizations": [
    {
      "type": "performance|error_handling|caching",
      "node_id": "affected_node", 
      "suggestion": "specific improvement",
      "impact": "high|medium|low"
    }
  ],
  "estimated_improvement": "20% faster execution",
  "complexity_score": 1-10,
  "recommendations": "overall suggestions"
}"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Workflow to optimize:\n{json.dumps(workflow_data, indent=2)}"},
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
                    "max_tokens": 1024,
                },
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]

            try:
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                return json.loads(content)
            except json.JSONDecodeError:
                return {"optimizations": [], "estimated_improvement": "No optimizations available"}


class WorkflowTemplateManager:
    """Manages workflow templates and patterns"""
    
    @staticmethod
    def get_common_patterns() -> Dict[str, Any]:
        """Get common workflow patterns for quick generation"""
        return {
            "email_to_slack": {
                "name": "Email to Slack Notification",
                "description": "Monitor email and send alerts to Slack",
                "nodes": ["gmail_trigger", "filter", "slack_send"],
                "connections": [("gmail_trigger", "filter"), ("filter", "slack_send")]
            },
            "api_to_sheet": {
                "name": "API Data to Google Sheets",
                "description": "Fetch API data and save to spreadsheet",
                "nodes": ["schedule", "http_request", "google_sheets"],
                "connections": [("schedule", "http_request"), ("http_request", "google_sheets")]
            },
            "webhook_processor": {
                "name": "Webhook Data Processor",
                "description": "Receive, validate, and process webhook data",
                "nodes": ["webhook", "validate", "process", "respond"],
                "connections": [("webhook", "validate"), ("validate", "process"), ("process", "respond")]
            },
            "monitoring_alert": {
                "name": "System Monitoring with Alerts",
                "description": "Monitor system and send alerts on issues",
                "nodes": ["schedule", "check_status", "condition", "alert"],
                "connections": [("schedule", "check_status"), ("check_status", "condition"), ("condition", "alert")]
            }
        }
    
    @staticmethod
    def suggest_template(user_prompt: str) -> Optional[str]:
        """Suggest a template based on user prompt keywords"""
        prompt_lower = user_prompt.lower()
        
        if any(word in prompt_lower for word in ["email", "gmail", "slack"]):
            return "email_to_slack"
        elif any(word in prompt_lower for word in ["api", "sheets", "spreadsheet"]):
            return "api_to_sheet"
        elif any(word in prompt_lower for word in ["webhook", "form", "submit"]):
            return "webhook_processor"
        elif any(word in prompt_lower for word in ["monitor", "check", "alert", "down"]):
            return "monitoring_alert"
        
        return None


class EnhancedPromptProcessor:
    """Advanced prompt processing with context understanding"""
    
    def __init__(self, xai_api_key: str):
        self.api_key = xai_api_key
        self.api_url = "https://api.x.ai/v1/chat/completions"
    
    async def analyze_user_intent(self, prompt: str) -> Dict[str, Any]:
        """Deep analysis of user intent for better workflow generation"""
        
        system_prompt = """You are a workflow intent analyzer. Extract key information from user requests:

1. Primary goal and business logic
2. Data sources and destinations  
3. Timing and triggers
4. Required integrations
5. Error handling needs
6. Security considerations
7. Scalability requirements

Respond with detailed JSON analysis."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "grok-3-mini",
                    "messages": messages,
                    "temperature": 0.3,
                    "max_tokens": 1024,
                },
            )
            response.raise_for_status()
            return response.json()


# Integration with existing workflow generation
async def generate_genius_workflow(
    user_prompt: str,
    xai_api_key: str,
    n8n_service,
    mode: str = "interpret",
    use_templates: bool = True,
    optimize_performance: bool = True
) -> Dict[str, Any]:
    """
    Genius-level workflow generation with all enhancements
    """
    
    # Stage 1: Check for template matches
    template_manager = WorkflowTemplateManager()
    suggested_template = template_manager.suggest_template(user_prompt) if use_templates else None
    
    # Stage 2: Deep intent analysis
    intent_processor = EnhancedPromptProcessor(xai_api_key)
    intent_analysis = await intent_processor.analyze_user_intent(user_prompt)
    
    # Stage 3: Generate workflow (using existing enhanced system)
    from .n8n_service import generate_workflow_from_prompt
    result = await generate_workflow_from_prompt(
        user_prompt, xai_api_key, n8n_service, mode=mode
    )
    
    # Stage 4: Performance optimization
    if optimize_performance:
        optimizer = WorkflowOptimizer(xai_api_key)
        optimizations = await optimizer.optimize_workflow_performance(result["workflow"])
        result["optimizations"] = optimizations
    
    # Stage 5: Add template suggestions
    if suggested_template:
        result["suggested_template"] = template_manager.get_common_patterns()[suggested_template]
    
    return result
