from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel, Field
import uuid

class ApprovalStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class ApprovalRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str
    reason: str 
    action_type: str 
    context: Any 
    status: ApprovalStatus = ApprovalStatus.PENDING

class HITLManager:
    """Orchestrates the Chain of Accountability's 'Judiciary' layer."""
    def __init__(self, adapter=None):
        # Default to CLI if no adapter is provided
        from .adapters import CLIAdapter
        self.adapter = adapter or CLIAdapter()
        self.history = []

    async def secure_approval(self, agent_id: str, reason: str, context: dict = None, triggered_by: str = "policy"):
        """Accepts 'triggered_by' to provide context to the human reviewer."""
        # ... logic to pass triggered_by to the adapter
        request = ApprovalRequest(
            agent_id=agent_id,
            reason=reason,
            action_type="intervention",
            context=context
        )
        
        is_approved = await self.adapter.notify(request)
        request.status = ApprovalStatus.APPROVED if is_approved else ApprovalStatus.REJECTED
        self.history.append(request)
        
        return is_approved