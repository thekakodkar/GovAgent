import pytest
from govagent.agent import ExecutiveAgent
from govagent.context import get_current_agent

@pytest.mark.asyncio
async def test_privacy_redaction_flow(sovereign_policy):
    """Verifies Article 9 compliance: PII is redacted before LLM ingestion."""
    # Updated: router=None injected instead of legacy model_client
    agent = ExecutiveAgent(persona="Director", policy=sovereign_policy, router=None)
    
    # Task containing PII
    raw_task = "Pay John Doe at 123 Main St for invoice #99."
    
    # Manually trigger the redaction guard (Stage 0)
    sanitized = agent.guard.privacy.redact_task(raw_task)
    
    assert "John Doe" not in sanitized
    assert "123 Main St" not in sanitized

@pytest.mark.asyncio
async def test_pydantic_schema_enforcement(sovereign_policy):
    """Verifies Pillar 1 Integrity: Malformed tool calls fail at the schema level."""
    # Updated: router=None injected instead of legacy model_client
    agent = ExecutiveAgent(persona="Director", policy=sovereign_policy, router=None)
    
    # Intent with a 'string' where a 'float' is required for amount
    malformed_intent = {"action": "execute_financial_transaction", "params": {"amount": "invalid_amt"}}
    
    from govagent.registry import registry
    with pytest.raises(Exception): # Pydantic ValidationError
        registry.validate_intent_schema(malformed_intent["action"], malformed_intent["params"])