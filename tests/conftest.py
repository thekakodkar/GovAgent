import pytest
from govagent.policy import Policy

@pytest.fixture
def standard_policy_config():
    """Returns a baseline configuration for a low-risk agent."""
    return {
        "metadata": {"agent_name": "StandardBot"},
        "global_limits": {
            "daily_budget_usd": 10.0,
            "max_per_transaction": 2.0,
            "max_tokens_per_run": 2000
        },
        "tools": [
            {"name": "search", "risk_level": "low"}
        ],
        "judiciary": {
            "channel": "cli",
            "confidence_threshold": 0.8
        }
    }

@pytest.fixture
def high_risk_policy_config():
    """Returns a configuration requiring high-stakes human oversight."""
    return {
        "metadata": {"agent_name": "AdminBot"},
        "global_limits": {
            "daily_budget_usd": 100.0,
            "max_per_transaction": 50.0
        },
        "tools": [
            {
                "name": "delete_db", 
                "risk_level": "high", 
                "require_human_approval": True
            }
        ],
        "judiciary": {
            "channel": "slack",
            "timeout_seconds": 600
        }
    }

@pytest.fixture
def standard_policy(standard_policy_config):
    """Fixture to provide a pre-instantiated Standard Policy."""
    return Policy(standard_policy_config)

@pytest.fixture
def high_risk_policy(high_risk_policy_config):
    """Fixture to provide a pre-instantiated High-Risk Policy."""
    return Policy(high_risk_policy_config)