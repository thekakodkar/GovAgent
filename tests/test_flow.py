import pytest
from govagent.agent import ExecutiveAgent
from govagent.policy import Policy
from govagent.context import get_current_agent

@pytest.mark.asyncio
async def test_executive_loop_context_isolation():
    """
    v0.3.0: Validates that the agent enrolls itself in the async context 
    during execution, enabling 'Invisible Governance'.
    """
    config = {
        "metadata": {"agent_name": "ContextTester"},
        "tools": [{"name": "web_search", "risk_level": "low"}]
    }
    policy = Policy(config)

    class MockClient:
        def __init__(self):
            self.steps = 0

        async def generate_plan(self, task, persona):
            self.steps += 1
            # Step 1: Perform the action
            if self.steps == 1:
                assert get_current_agent() is not None
                intent = {"action": "web_search", "params": {"query": "test"}, "thought": "Thinking..."}
                return intent, 0.01, 10
            
            # Step 2: Signal completion (This triggers the success return in agent.py)
            return {"thought": "I have found the info.", "action": None}, 0.0, 0
    
    agent = ExecutiveAgent(persona="Tester", policy=policy, model_client=MockClient())
    
    # Before execution, context should be empty
    assert get_current_agent() is None
    
    report = await agent.execute("Test context enrollment")
    
    assert report.status == "success"
    # After execution, context must be cleared (Article 12 integrity)
    assert get_current_agent() is None

@pytest.mark.asyncio
async def test_fiscal_circuit_breaker_triage():
    """
    v0.3.0: Confirms Stage 1 (Fiscal) stops execution before Stage 3 (Judiciary).
    """
    config = {
        "metadata": {"agent_name": "BudgetController"},
        "global_limits": {"max_per_transaction": 0.5},
        "tools": [{"name": "expensive_tool", "risk_level": "high"}]
    }
    policy = Policy(config)

    class HighCostClient:
        async def generate_plan(self, task, persona):
            # Intent triggers a $500 cost check
            return {"action": "expensive_tool", "params": {}}, 500.0, 100

    agent = ExecutiveAgent(persona="Auditor", policy=policy, model_client=HighCostClient())
    report = await agent.execute("Run expensive operation")

    assert "blocked" in report.status
    assert "FISCAL" in report.status.upper()
    # Ensure no 'Judiciary' leakage happened
    assert "judiciary" not in report.guards_evaluated

@pytest.mark.asyncio
async def test_telemetry_audit_trail_integrity():
    """
    v0.3.0: Ensures Article 12 compliance via guards_evaluated persistence.
    """
    config = {
        "metadata": {"agent_name": "Auditor"},
        "tools": [{"name": "read_file", "risk_level": "low"}]
    }
    policy = Policy(config)
    # Using bootstrap logic (mocked) or direct init
    agent = ExecutiveAgent(persona="Auditor", policy=policy, model_client=None)
    
    # Simulate a partial evaluation
    agent.telemetry.start_trace("Auditor", "Trace Integrity Test")
    await agent.evaluate(guards=["policy"], intent={"action": "read_file"})
    
    assert "policy" in agent.telemetry.current_session.guards_evaluated