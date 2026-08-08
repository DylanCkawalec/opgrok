"""
Audit Logger - Track all workflow modifications for transparency and debugging

Every action is logged with:
- Timestamp
- User/session
- Action type
- Before/after state
- Success/failure
- Execution time
"""

import json
import time
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path


class AuditLogger:
    """Production-grade audit logging for workflow operations"""
    
    def __init__(self, log_dir: str = ".n8n/audit"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.current_session = {}
    
    def log_workflow_generation(
        self,
        prompt: str,
        workflow_id: Optional[str],
        success: bool,
        duration: float,
        error: Optional[str] = None
    ):
        """Log workflow generation attempt"""
        self._write_log("workflow_generation", {
            "prompt_length": len(prompt),
            "prompt_preview": prompt[:200],
            "workflow_id": workflow_id,
            "success": success,
            "duration_seconds": round(duration, 2),
            "error": error
        })
    
    def log_workflow_modification(
        self,
        workflow_id: str,
        modification_type: str,
        before_state: Dict[str, Any],
        after_state: Dict[str, Any],
        success: bool,
        user_request: str
    ):
        """Log workflow modification"""
        self._write_log("workflow_modification", {
            "workflow_id": workflow_id,
            "modification_type": modification_type,
            "user_request": user_request,
            "before": {
                "nodes": len(before_state.get("nodes", [])),
                "connections": len(before_state.get("connections", {}))
            },
            "after": {
                "nodes": len(after_state.get("nodes", [])),
                "connections": len(after_state.get("connections", {}))
            },
            "success": success
        })
    
    def log_auto_connection(
        self,
        workflow_id: str,
        connections_added: int,
        nodes_connected: List[str],
        success: bool
    ):
        """Log automatic node connection"""
        self._write_log("auto_connection", {
            "workflow_id": workflow_id,
            "connections_added": connections_added,
            "nodes_connected": nodes_connected,
            "success": success
        })
    
    def log_api_call(
        self,
        endpoint: str,
        method: str,
        status_code: int,
        duration: float,
        error: Optional[str] = None
    ):
        """Log n8n API calls for debugging"""
        self._write_log("api_call", {
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "duration_ms": round(duration * 1000, 2),
            "success": 200 <= status_code < 300,
            "error": error
        })
    
    def _write_log(self, log_type: str, data: Dict[str, Any]):
        """Write log entry to file"""
        timestamp = datetime.utcnow().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "type": log_type,
            **data
        }
        
        # Write to daily log file
        log_file = self.log_dir / f"audit_{datetime.utcnow().strftime('%Y%m%d')}.jsonl"
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def get_recent_logs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve recent audit logs"""
        log_file = self.log_dir / f"audit_{datetime.utcnow().strftime('%Y%m%d')}.jsonl"
        
        if not log_file.exists():
            return []
        
        logs = []
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    logs.append(json.loads(line))
                except:
                    pass
        
        return logs[-limit:]


# Global audit logger
_audit_logger = AuditLogger()


def get_audit_logger() -> AuditLogger:
    """Get global audit logger instance"""
    return _audit_logger
