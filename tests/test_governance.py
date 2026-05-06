import pytest
from govagent.agent import ExecutiveAgent
from govagent.policy import Policy
from govagent.hitl import HITLManager, ApprovalStatus
from govagent.guards import GovernanceViolation

@pytest.mark.asyncio
async def test_hitl_escalation_on_high_risk():
    """
    v0.2.3: Validates that high-risk tools trigger the Judiciary guard
    through the centralized evaluate() method.
    """
    config = {
        "metadata": {"agent_name": "TestAgent"},
        "global_limits": {"max_per_transaction": 5000.0},
        "tools": [
            {"name": "delete_database", "risk_level": "high", "require_human_approval": True}
        ]
    }
    policy = Policy(config)
    
    # Mock Adapter that Approves
    class MockApproveAdapter:
        async def notify(self, request):
            return True # Simulating Slack 'Approve' click

    hitl = HITLManager(adapter=MockApproveAdapter())
    agent = ExecutiveAgent(
        persona="Admin", 
        policy=policy, 
        model_client=None, 
        hitl_manager=hitl
    )
    
    # 1. Verify policy identification
    assert policy.is_high_risk("delete_database") is True
    
    # 2. Verify centralized evaluation passes on approval
    # value=0.0 means it passes the fiscal guard first
    result = await agent.evaluate(
        guards=["fiscal", "judiciary"],
        intent={"action": "delete_database", "params": {"id": "db_001"}},
        value=10.0 
    )
    assert result is True

@pytest.mark.asyncio
async def test_hitl_rejection_raises_violation():
    """
    v0.2.3: Validates that a human rejection raises a GovernanceViolation,
    terminating the agent loop immediately.
    """
    config = {
        "metadata": {"agent_name": "FinanceBot"},
        "tools": [
            {"name": "wire_transfer", "risk_level": "high"}
        ]
    }
    policy = Policy(config)
    
    # Mock Adapter that REJECTS
    class MockRejectAdapter:
        async def notify(self, request):
            return False # Simulating Slack 'Reject' click

    hitl = HITLManager(adapter=MockRejectAdapter())
    agent = ExecutiveAgent(
        persona="FinanceBot", 
        policy=policy, 
        model_client=None, 
        hitl_manager=hitl
    )
    
    # Verify that evaluate() raises the expected exception on rejection
    with pytest.raises(GovernanceViolation) as excinfo:
        await agent.evaluate(
            guards=["judiciary"],
            intent={"action": "wire_transfer", "params": {"amount": 1000}}
        )
    
    assert "human judiciary denied" in str(excinfo.value).lower()

@pytest.mark.asyncio
async def test_fiscal_overrides_judiciary_triage():
    """
    v0.2.3: Prove the 'Triage' logic—if fiscal fails, judiciary is never called.
    """
    config = {
        "metadata": {"agent_name": "TriageTest"},
        "global_limits": {"max_per_transaction": 100.0},
        "tools": [{"name": "wire_transfer", "risk_level": "high"}]
    }
    policy = Policy(config)
    
    # This adapter should NEVER be called because fiscal guard is checked first
    class FailIfCalledAdapter:
        async def notify(self, request):
            pytest.fail("Judiciary guard was called even though Fiscal guard failed!")

    agent = ExecutiveAgent(
        persona="Bot", 
        policy=policy, 
        model_client=None, 
        hitl_manager=HITLManager(adapter=FailIfCalledAdapter())
    )

    # Attempting a $500 transfer when limit is $100
    with pytest.raises(GovernanceViolation) as excinfo:
        await agent.evaluate(
            guards=["fiscal", "judiciary"],
            intent={"action": "wire_transfer"},
            value=500.0
        )
    
    assert "fiscal reject" in str(excinfo.value).lower()