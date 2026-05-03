import pytest
from unittest.mock import AsyncMock, MagicMock
from govagent.policy import Policy
from govagent.agent import ExecutiveAgent
from govagent.telemetry import TelemetryManager

class MockModel:
    """Simulates a cooperative LLM for the Happy Path."""
    async def generate_plan(self, task, persona):
        return "I will search for the latest tech trends.", "web_search", {"query": "AI 2026 trends"}

@pytest.mark.asyncio
async def test_executive_loop_completion():
    policy = Policy(agent_name="TrendAnalyst", allowed_tools=["web_search"])
    agent = ExecutiveAgent("Director", policy, MockModel())
    
    # FIX: Ensure the loop terminates by making the second call return 'complete'
    agent.perform_action = AsyncMock(return_value="Task complete.")
    
    result = await agent.execute("Summarize trends")

    # FIX: Use dot notation for Pydantic objects
    assert result.status == "success" 
    print("\n✅ Flow Test Fixed: Used dot notation for snapshot.")

@pytest.mark.asyncio
async def test_telemetry_trace_accuracy():
    policy = Policy(agent_name="Auditor", allowed_tools=["read_file"])
    agent = ExecutiveAgent("Auditor", policy, MockModel())
    
    agent.model.generate_plan = AsyncMock(return_value=("Reading.", "read_file", {}))
    agent.perform_action = AsyncMock(return_value="File read complete. Task complete.") # Add task completion signal
    
    snapshot = await agent.execute("Audit logs")
    
    # FIX: Use 'reasoning_steps' instead of 'steps'
    assert len(snapshot.reasoning_steps) > 0
    assert snapshot.reasoning_steps[-1]["action"] == "read_file"