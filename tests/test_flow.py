import pytest
from govagent.agent import ExecutiveAgent
from govagent.policy import Policy
from govagent.guards import GovernanceViolation

@pytest.mark.asyncio
async def test_executive_loop_with_modular_guards():
    """
    v0.2.3: Validates the 'Think -> Evaluate -> Act' loop 
    with parameterized guards.
    """
    config = {
        "metadata": {"agent_name": "TrendAnalyst"},
        "global_limits": {
            "daily_budget_usd": 100.0,
            "max_per_transaction": 50.0
        },
        "tools": [
            {"name": "web_search", "risk_level": "low", "guards": ["policy"]}
        ]
    }
    policy = Policy(config)

    class MockClient:
        async def generate_plan(self, task, persona):
            # v0.2.3: Return (Intent, Cost, Tokens)
            intent = {"action": "web_search", "params": {"query": "AI 2026"}, "thought": "Searching..."}
            return intent, 0.05, 100

    agent = ExecutiveAgent(
        persona="Analyst",
        policy=policy,
        model_client=MockClient()
    )

    report = await agent.execute("What is the latest in AI?")
    
    # Assert successful execution through the 'Policy' guard
    assert report.status == "success"
    assert "policy" in report.guards_evaluated

@pytest.mark.asyncio
async def test_fiscal_circuit_breaker_triage():
    """
    v0.2.3: Assert that the Fiscal Guard triggers a Hard Stop 
    before the agent acts.
    """
    config = {
        "metadata": {"agent_name": "BudgetController"},
        "global_limits": {
            "daily_budget_usd": 1.0, # Tiny budget for testing
            "max_per_transaction": 0.5
        },
        "tools": [{"name": "expensive_tool", "risk_level": "high"}]
    }
    policy = Policy(config)

    class HighCostClient:
        async def generate_plan(self, task, persona):
            return {"action": "expensive_tool"}, 500.0, 100 # $500 cost

    agent = ExecutiveAgent(persona="Auditor", policy=policy, model_client=HighCostClient())
    
    report = await agent.execute("Run expensive operation")

    # Assert that governance blocked the execution
    assert "blocked" in report.status
    assert "FISCAL REJECT" in report.status
    # Verify that the 'judiciary' (Slack) was never even reached to save costs
    assert "judiciary" not in report.guards_evaluated

@pytest.mark.asyncio
async def test_telemetry_forensic_integrity():
    """
    v0.2.3: Ensures the JSONL snapshot contains the guard manifest.
    """
    config = {
        "metadata": {"agent_name": "Auditor"},
        "tools": [{"name": "read_file", "risk_level": "low"}]
    }
    policy = Policy(config)
    agent = ExecutiveAgent(persona="Auditor", policy=policy, model_client=None)
    
    agent.telemetry.start_trace("Auditor", "Audit logs")
    agent.telemetry.log_guard_evaluation("fiscal", "passed")
    
    assert "fiscal" in agent.telemetry.current_session.guards_evaluated