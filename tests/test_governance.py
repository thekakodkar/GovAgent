import pytest
from govagent.agent import ExecutiveAgent
from govagent.context import update_shared_spend, get_shared_fiscal_metrics, reset_current_agent, set_current_agent
from govagent.guards import GovernanceViolation

@pytest.mark.asyncio
async def test_recursive_tco_ceiling_breach(sovereign_policy):
    """
    Validates Phase 2: Swarm aggregate cost triggers a global circuit breaker.
    Ensures that parent + child spend does not exceed the Institutional TCO.
    """
    # Initialize the Director (Parent)
    agent = ExecutiveAgent(persona="Director", policy=sovereign_policy, model_client=None)
    
    # 1. INSTITUTIONAL STATE: Simulate Parent has already consumed 90% of the budget
    # In a real swarm, this is updated automatically via telemetry.finalize()
    update_shared_spend(90.0) 
    
    # 2. SUB-AGENT ACTION: Child attempts a $20 transaction
    # Total projected spend ($110) exceeds the $100 policy ceiling
    with pytest.raises(GovernanceViolation) as excinfo:
        await agent.evaluate(guards=["fiscal"], value=20.0)
    
    # 3. VERIFICATION: Ensure the rejection is specific to the Recursive TCO
    assert "RECURSIVE TCO REJECT" in str(excinfo.value).upper()
    print("✅ Recursive TCO Circuit Breaker verified.")

@pytest.mark.asyncio
async def test_judiciary_traceability_in_swarm(sovereign_policy):
    """
    Validates Phase 2: Ensures Sub-Agents correctly inherit the Parent Trace ID.
    Satisfies Article 12 (Traceability) for multi-agent delegation.
    """
    # 1. Setup Parent Context
    parent_agent = ExecutiveAgent(persona="Director", policy=sovereign_policy, model_client=None)
    parent_agent.telemetry.start_trace("Director", "Master Task")
    parent_trace_id = parent_agent.telemetry.current_session.trace_id
    
    # 2. Enroll Parent in Context (Simulating delegation)
    token = set_current_agent(parent_agent)
    
    try:
        # 3. Initialize Child (Sub-Agent)
        child_agent = ExecutiveAgent(persona="Clerk", policy=sovereign_policy, model_client=None)
        child_agent.telemetry.start_trace("Clerk", "Sub-Task Delegation")
        
        # 4. VERIFICATION: Child must hold the Parent's Trace ID as 'parent_trace_id'
        assert child_agent.telemetry.current_session.parent_trace_id == parent_trace_id
        print(f"✅ Swarm Traceability verified: Child inherited Parent ID {parent_trace_id}")
        
    finally:
        reset_current_agent(token)

@pytest.mark.asyncio
async def test_shared_fiscal_state_persistence(sovereign_policy):
    """
    Ensures that fiscal updates are persistent across different agent instances 
    within the same institutional session.
    """
    # 1. Initial spend
    update_shared_spend(15.50)
    
    # 2. Secondary spend from a different instance
    update_shared_spend(10.00)
    
    # 3. VERIFICATION: Total metrics must reflect the sum
    metrics = get_shared_fiscal_metrics()
    assert metrics["cumulative_spend"] == 25.50
    print(f"✅ Shared Fiscal State verified: Aggregate spend is {metrics['cumulative_spend']}")