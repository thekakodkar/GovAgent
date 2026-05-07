import pytest
from govagent.policy import Policy

@pytest.fixture
def v4_policy_config():
    """Returns a v0.4.0 Sovereign Policy configuration."""
    return {
        "metadata": {
            "agent_name": "SovereignDirector",
            "pii_redaction_enabled": True # Article 9 Requirement
        },
        "global_limits": {
            "daily_budget_usd": 100.0,
            "recursive_tco_ceiling": 150.0, # Phase 2 Shared Ceiling
            "max_per_transaction": 50.0
        },
        "tools": [
            {"name": "execute_financial_transaction", "risk_level": "high"}
        ],
        "judiciary": {"channel": "cli"}
    }

@pytest.fixture
def sovereign_policy(v4_policy_config):
    return Policy(v4_policy_config)