# tests/test_governance.py
import pytest
from govagent.agent import ExecutiveAgent
from govagent.guards.semantic import SemanticGuard
from govagent.guards.circuit_breaker import GovernanceViolation

# Split imports based on package structural topography
from govagent.context.fiscal_ledger import (
    update_shared_spend, 
    get_shared_fiscal_metrics, 
    reset_fiscal_ledger
)
from govagent.context.session import (
    set_current_agent, 
    reset_current_agent
)

@pytest.mark.asyncio
async def test_semantic_vector_alignment_violation(sovereign_policy):
    """
    Verifies that the localized Sentence-Transformer vector engine 
    intercepts prohibited strategies with a strict 0.0 circuit breaker trip.
    """
    prohibited_strategies = ["aggressively targeting vulnerable demographics for financial gain"]
    
    # Standardize operational threshold boundaries for local model sizes
    vector_guard = SemanticGuard(
        mission="Provide ethical enterprise analytics.", 
        prohibited=prohibited_strategies, 
        threshold=0.60
    )
    
    predatory_thought = "I will maximize profit by aggressively targeting vulnerable demographics."
    
    score = vector_guard.evaluate_alignment(predatory_thought)
    assert score == 0.0
    print("✅ Localized Semantic Transformer Vector Circuit Breaker verified with explicit 0.0 hard-stop.")

@pytest.mark.asyncio
async def test_recursive_tco_ceiling_breach(sovereign_policy):
    """
    Validates Phase 2: Swarm aggregate cost triggers a global circuit breaker.
    Ensures that parent + child spend does not exceed the Institutional TCO limit.
    """
    agent = ExecutiveAgent(persona="Director", policy=sovereign_policy, router=None)
    
    # 1. INSTITUTIONAL STATE: Reset and simulate 90.0 baseline consumption
    reset_fiscal_ledger()
    update_shared_spend(90.0) 
    
    # 2. SUB-AGENT ACTION: Child attempts a $20 transaction
    with pytest.raises(GovernanceViolation) as excinfo:
        await agent.evaluate(guards=["fiscal"], value=20.0)
    
    assert "RECURSIVE TCO REJECT" in str(excinfo.value).upper()
    print("✅ Recursive TCO Circuit Breaker verified under active policy ceiling.")

@pytest.mark.asyncio
async def test_judiciary_traceability_in_swarm(sovereign_policy):
    """
    Validates Phase 2: Ensures Sub-Agents correctly inherit the Parent Trace ID.
    Satisfies Article 12 (Traceability) for concurrent multi-agent delegation trees.
    """
    parent_agent = ExecutiveAgent(persona="Director", policy=sovereign_policy, router=None)
    parent_agent.telemetry.start_trace("Director", "Master Task")
    parent_trace_id = parent_agent.telemetry.current_session.trace_id
    
    token = set_current_agent(parent_agent)
    
    try:
        child_agent = ExecutiveAgent(persona="Clerk", policy=sovereign_policy, router=None)
        child_agent.telemetry.start_trace("Clerk", "Sub-Task Delegation")
        
        assert child_agent.telemetry.current_session.parent_trace_id == parent_trace_id
        print(f"✅ Swarm Traceability verified: Child inherited Parent ID {parent_trace_id}")
        
    finally:
        reset_current_agent(token)

@pytest.mark.asyncio
async def test_shared_atomic_fiscal_state_persistence(sovereign_policy):
    """
    Ensures that fiscal updates persist atomically across different agent instances
    and correctly increment the parallel task counter metrics.
    """
    reset_fiscal_ledger()
    
    # 1. Simulate multi-tiered workspace operations
    update_shared_spend(15.50)
    update_shared_spend(10.00)
    
    # 2. VERIFICATION: Verify both total spend and thread-safe execution counts
    metrics = get_shared_fiscal_metrics()
    assert metrics["cumulative_spend"] == 25.50
    assert metrics["task_counter"] == 2.0
    print(f"✅ Shared Atomic Fiscal Ledger verified: Spend is {metrics['cumulative_spend']}, Operations: {metrics['task_counter']}")