import pytest
from govagent.policy import Policy
from govagent.context import reset_fiscal_ledger

@pytest.fixture(autouse=True)
def clean_institutional_state():
    """Automatically resets the ledger before every test to prevent spend leakage."""
    reset_fiscal_ledger()
    yield

@pytest.fixture
def v6_policy_config():
    """Returns a v0.6.0 Sovereign Policy configuration."""
    return {
        "metadata": {
            "agent_name": "SovereignDirector",
            "version": "0.6.0"
        },
        "registry_alignment": {
            "allowed_tools": ["execute_financial_transaction"],
            "high_risk_tools": ["execute_financial_transaction"]
        },
        "fiscal_governance": {
            "currency": "USD",
            "global_limits": {
                "daily_budget_usd": 100.0,
                "recursive_tco_limit": 150.0
            }
        }
    }

@pytest.fixture
def sovereign_policy(v6_policy_config):
    return Policy(v6_policy_config)

def mock_audit_ledger(tmp_path):
    """
    v0.6.0 Engineering Fixture.
    Generates a thread-safe path to test MetaGovernor log-scraping capabilities.
    """
    return tmp_path / "audit_buffer.jsonl"