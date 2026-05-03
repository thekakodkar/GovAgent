import pytest
from unittest.mock import AsyncMock, MagicMock
from govagent.policy import Policy
from govagent.agent import ExecutiveAgent
from govagent.hitl import HITLManager

class MockModel:
    """Simulates LLM plan generation."""
    async def generate_plan(self, task, persona):
        return "I need to delete the database.", "delete_database", {"db_id": "prod_01"}

@pytest.mark.asyncio
async def test_hitl_blocking_on_high_risk_tool():
    # FIX: Add tool to allowed_tools so it passes the Guard and hits HITL
    policy = Policy(
        agent_name="TestAgent", 
        allowed_tools=["delete_database"], 
        high_risk_tools=["delete_database"]
    )
    mock_adapter = AsyncMock(return_value=True)
    hitl_manager = HITLManager(adapter=mock_adapter)

    agent = ExecutiveAgent("Admin", policy, MockModel(), hitl_manager=hitl_manager)
    agent.is_task_complete = MagicMock(return_value=True)
    
    await agent.execute("Delete database")
    mock_adapter.notify.assert_called_once()

@pytest.mark.asyncio
async def test_hitl_rejection_halts_execution():
    policy = Policy(
        agent_name="TestAgent", 
        allowed_tools=["wire_transfer"], 
        high_risk_tools=["wire_transfer"]
    )
    mock_adapter = AsyncMock(return_value=False) 
    hitl_manager = HITLManager(adapter=mock_adapter)

    agent = ExecutiveAgent("Finance", policy, AsyncMock(), hitl_manager=hitl_manager)
    agent.model.generate_plan.return_value = ("Transfer.", "wire_transfer", {})

    result = await agent.execute("Send money")
    
    # Assertions
    assert "rejected" in result.status.lower()
    # Ensure it stopped immediately and didn't call the adapter 10 times
    assert mock_adapter.notify.call_count == 1
    print("\n✅ Governance Test Fixed: Agent halted immediately on rejection.")