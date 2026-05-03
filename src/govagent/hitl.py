from enum import Enum
from typing import Optional, Any, Protocol
from pydantic import BaseModel, Field
import uuid

class ApprovalStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class ApprovalRequest(BaseModel):
    """A formal request for human intervention."""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str
    reason: str 
    action_type: str  # e.g., "tool_call", "budget_override"
    context: Any 
    status: ApprovalStatus = ApprovalStatus.PENDING
    reviewer_notes: Optional[str] = None

class HITLAdapter(Protocol):
    """Protocol for different notification channels (CLI, Slack, Teams)."""
    async def notify(self, request: ApprovalRequest) -> bool:
        ...

class CLIAdapter:
    """Standard Console Adapter for local development."""
    async def notify(self, request: ApprovalRequest) -> bool:
        print(f"\n--- 🛑 GOVAGENT INTERVENTION REQUIRED ---")
        print(f"ID: {request.request_id}")
        print(f"Agent: {request.agent_id}")
        print(f"Reason: {request.reason}")
        print(f"Context: {request.context}")
        
        user_input = input("\nDecision (y/n) or add notes: ").strip().lower()
        if user_input.startswith('y'):
            return True
        return False

class HITLManager:
    """
    Orchestrates the Chain of Accountability's 'Judiciary' layer.
    """
    def __init__(self, adapter: HITLAdapter = None):
        self.adapter = adapter or CLIAdapter()
        self.history: list[ApprovalRequest] = []

    async def secure_approval(self, agent_id: str, reason: str, context: Any) -> bool:
        """
        The entry point for the Executive Loop to request permission.
        """
        request = ApprovalRequest(
            agent_id=agent_id,
            reason=reason,
            action_type="intervention",
            context=context
        )
        
        # Block execution until the adapter returns a decision
        is_approved = await self.adapter.notify(request)
        
        request.status = ApprovalStatus.APPROVED if is_approved else ApprovalStatus.REJECTED
        self.history.append(request)
        
        return is_approved