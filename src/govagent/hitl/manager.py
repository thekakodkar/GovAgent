from enum import Enum
from typing import Optional, Any, Set, List
from pydantic import BaseModel, Field
import uuid

class ApprovalStatus(Enum):
    PENDING = "pending"
    QUORUM_MET = "approved" 
    REJECTED = "rejected"

class ApprovalRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str
    reason: str 
    action_type: str = "policy"  # FIX: Defined for triggered_by mapping
    context: Any 
    status: ApprovalStatus = ApprovalStatus.PENDING
    
    # Federated State (v0.5.0)
    min_approvals: int = 1
    approvers: Set[str] = Field(default_factory=set)
    message_ts: Optional[str] = None # For threaded Slack updates

class HITLManager:
    """Orchestrates the Federated Judiciary process."""
    def __init__(self, adapter=None):
        from .adapters import CLIAdapter
        self.adapter = adapter or CLIAdapter()
        self.history = []

    async def secure_approval(
        self, 
        agent_id: str, 
        reason: str, 
        context: dict = None, 
        triggered_by: str = "policy", 
        config: dict = None            
    ):
        request = ApprovalRequest(
            agent_id=agent_id,
            reason=reason,
            action_type=triggered_by, 
            context=context or {},
            min_approvals=config.get("min_approvals", 1) if config else 1
        )
        
        is_approved = await self.adapter.notify(request)
        request.status = ApprovalStatus.QUORUM_MET if is_approved else ApprovalStatus.REJECTED
        self.history.append(request)
        
        return is_approved