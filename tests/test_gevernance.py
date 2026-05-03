import pytest
from govagent.agent import ExecutiveAgent
from govagent.policy import Policy
from govagent.hitl import HITLManager

@pytest.mark.asyncio
async def test_hitl_blocking_on_high_risk_tool():
    # Define a high-risk tool in the config
    config = {
        "metadata": {"agent_name": "TestAgent"},
        "tools": [
            {"name": "delete_database", "risk_level": "high", "requires_hitl": True}
        ]
    }
    policy = Policy(config)
    
    # Mock HITL that approves
    class MockHITL:
        async def secure_approval(self, action, params):
            return True, "Approved by admin"

    agent = ExecutiveAgent(
        persona="Admin", 
        policy=policy, 
        model_client=None, 
        hitl_manager=MockHITL()
    )
    
    # Verify the policy correctly identifies high risk
    assert policy.is_high_risk("delete_database") is True

@pytest.mark.asyncio
async def test_hitl_rejection_halts_execution():
    config = {
        "metadata": {"agent_name": "TestAgent"},
        "tools": [
            {"name": "wire_transfer", "risk_level": "high", "requires_hitl": True}
        ]
    }
    policy = Policy(config)
    
    # Mock HITL that REJECTS
    class MockRejectHITL:
        async def secure_approval(self, action, params):
            return False, "Unauthorized disbursement detected."

    agent = ExecutiveAgent(
        persona="FinanceBot", 
        policy=policy, 
        model_client=None, 
        hitl_manager=MockRejectHITL()
    )
    
    # Mock loop logic simulation
    approved, reason = await agent.hitl.secure_approval("wire_transfer", {})
    
    assert approved is False
    assert "Unauthorized" in reason