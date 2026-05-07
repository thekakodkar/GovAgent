import pytest
from govagent.agent import ExecutiveAgent
from govagent.policy import Policy
from govagent.hitl import HITLManager
from govagent.guards import GovernanceViolation
from govagent.context import get_current_agent

@pytest.mark.asyncio
async def test_hitl_escalation_on_high_risk():
    """
    v0.3.0: Validates that 'High Risk' triggers the Synchronous HITL
    while maintaining Article 14 (Human Oversight) compliance.
    """
    config = {
        "metadata": {"agent_name": "TestAgent"},
        "tools": [
            {"name": "delete_database", "risk_level": "high"}
        ]
    }
    policy = Policy(config)
    
    # Mock Adapter: Simulates a successful 'Approve' click in Slack
    class MockApproveAdapter:
        async def notify(self, request):
            return True

    hitl = HITLManager(adapter=MockApproveAdapter())
    agent = ExecutiveAgent(
        persona="Admin", 
        policy=policy, 
        model_client=None, 
        hitl_manager=hitl
    )
    
    # Verify the centralized evaluation loop triggers the Judiciary
    result = await agent.evaluate(
        guards=["fiscal", "judiciary"],
        intent={"action": "delete_database", "params": {"id": "db_001"}},
        value=1.0 # Minimal value to pass Fiscal
    )
    
    assert result is True
    assert "judiciary" in agent.telemetry.current_session.guards_evaluated

@pytest.mark.asyncio
async def test_hitl_rejection_raises_violation():
    """
    v0.3.0: Validates that a Human Rejection triggers an immediate 
    Circuit Breaker, protecting the enterprise from unauthorized acts.
    """
    config = {
        "metadata": {"agent_name": "FinanceBot"},
        "tools": [{"name": "wire_transfer", "risk_level": "high"}]
    }
    policy = Policy(config)
    
    # Mock Adapter: Simulates a 'Reject' click in Slack
    class MockRejectAdapter:
        async def notify(self, request):
            return False

    hitl = HITLManager(adapter=MockRejectAdapter())
    agent = ExecutiveAgent(persona="FinanceBot", policy=policy, model_client=None, hitl_manager=hitl)
    
    # Verify rejection raises the specific GovernanceViolation
    with pytest.raises(GovernanceViolation) as excinfo:
        await agent.evaluate(
            guards=["judiciary"],
            intent={"action": "wire_transfer", "params": {"amount": 1000}}
        )
    
    assert "human judiciary denied" in str(excinfo.value).lower()

@pytest.mark.asyncio
async def test_fiscal_overrides_judiciary_triage():
    """
    v0.3.0: Proves the Triage hierarchy. Judiciary is a 'Stage 3' guard; 
    if 'Stage 1' (Fiscal) fails, we save human bandwidth by never pining Slack.
    """
    config = {
        "metadata": {"agent_name": "TriageTest"},
        "global_limits": {"max_per_transaction": 100.0},
        "tools": [{"name": "wire_transfer", "risk_level": "high"}]
    }
    policy = Policy(config)
    
    # This adapter should NEVER be hit if Fiscal works correctly
    class FailIfCalledAdapter:
        async def secure_approval(self, *args, **kwargs):
            pytest.fail("ERROR: Judiciary was engaged despite a Fiscal failure!")

    agent = ExecutiveAgent(
        persona="Bot", 
        policy=policy, 
        model_client=None, 
        hitl_manager=HITLManager(adapter=FailIfCalledAdapter())
    )

    # Attempting a $500 transfer against a $100 limit
    with pytest.raises(GovernanceViolation) as excinfo:
        await agent.evaluate(
            guards=["fiscal", "judiciary"],
            intent={"action": "wire_transfer"},
            value=500.0
        )
    
    assert "fiscal reject" in str(excinfo.value).lower()
    # Verify Judiciary was never pined
    assert "judiciary" not in agent.telemetry.current_session.guards_evaluated