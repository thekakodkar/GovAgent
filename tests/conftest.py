# tests/conftest.py
import pytest
from govagent.policy import Policy

@pytest.fixture
def standard_policy():
    return Policy(agent_name="TestBot", allowed_tools=["search"])

@pytest.fixture
def high_risk_policy():
    return Policy(agent_name="AdminBot", high_risk_tools=["delete_db"])