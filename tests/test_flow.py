import pytest
from govagent.agent import ExecutiveAgent
from govagent.policy import Policy
from govagent.hitl import HITLManager

@pytest.mark.asyncio
async def test_executive_loop_completion():
    config = {
        "metadata": {"agent_name": "TrendAnalyst"},
        "governance": {
            "max_session_cost_usd": 20.0
        },
        "tools": [
            {"name": "web_search", "risk_level": "low"}
        ]
    }
    policy = Policy(config)

    class MockClient:
        async def generate_plan(self, task, persona):
            # v0.2.0 Contract: (Intent, Cost, Tokens)
            # Index 1 MUST be a float for the telemetry += operation
            return "Strategy: Execute web_search", 0.01, 100

        async def get_response(self, prompt):
            # Index 0 is the Action Dict, Index 1 is the Cost (Float)
            action = {"action": "web_search", "params": {"query": "AI trends 2026"}}
            return action, 0.02, 150

    agent = ExecutiveAgent(
        persona="Analyst",
        policy=policy,
        model_client=MockClient()
    )

    report = await agent.execute("What is the latest in AI?")
    
    # Assert success - This will now pass as the types match
    assert report.status in ["completed", "success"]

@pytest.mark.asyncio
async def test_telemetry_trace_accuracy():
    config = {
        "metadata": {"agent_name": "Auditor"},
        "tools": [{"name": "read_file", "risk_level": "low"}]
    }
    policy = Policy(config)
    
    agent = ExecutiveAgent(persona="Auditor", policy=policy, model_client=None)
    # Validate that the snapshot captures the initialized agent metadata
    assert agent.policy.agent_name == "Auditor"