from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel, Field

class ApprovalStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class ApprovalRequest(BaseModel):
    """A formal request for human intervention."""
    request_id: str
    agent_id: str
    reason: str  # e.g., "Confidence below threshold" or "High-risk tool call"
    context: Any # Data the agent was working on
    status: ApprovalStatus = ApprovalStatus.PENDING
    reviewer_notes: Optional[str] = None

class HITLManager:
    """
    Orchestrates human intervention. Designed to be extended 
    with Slack, Teams, or Email adapters.
    """
    def __init__(self):
        self.active_requests: dict[str, ApprovalRequest] = {}

    def request_approval(self, request: ApprovalRequest) -> bool:
        """
        In the 'Lite' version, this logs to console/file.
        In 'Pro', this would trigger a webhook to a messaging platform.
        """
        self.active_requests[request.request_id] = request
        print(f"\n[HITL REQUIRED] Agent: {request.agent_id}")
        print(f"Reason: {request.reason}")
        print(f"Action: {request.context}")
        
        # Simulated CLI Approval for the initial PyPI package
        user_input = input("Approve this action? (y/n/notes): ").lower()
        
        if user_input.startswith('y'):
            request.status = ApprovalStatus.APPROVED
            return True
        else:
            request.status = ApprovalStatus.REJECTED
            return False