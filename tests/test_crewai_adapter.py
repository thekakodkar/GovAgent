import pytest
import pathlib
from crewai import Agent, Task, Crew
from crewai.tools import tool
from govagent.extensions.crewai.enforcer import GovAgentEnforcer

MOCK_YAML_POLICY = """
version: "2.0.0"
routing_mode: "LOCAL_ONLY"
default_provider: "local_ollama"
routing_rules: []
governance_rules:
  authorized_tools:
    - "approved_market_fetcher"
routing_profiles:
  default_local_slm: "ollama/llama3.2"
fiscal_budgets:
  max_task_budget_usd: 5.0
"""

@pytest.fixture
def policy_file(tmp_path):
    """Creates a local physical temporary policy manifest to avoid open/yaml mock pollution."""
    p = tmp_path / "test_policy.yaml"
    p.write_text(MOCK_YAML_POLICY, encoding="utf-8")
    return str(p)


def test_govagent_crewai_unauthorized_tool_gate(policy_file):
    """Validates that the enforcer blocks unauthorized tools out-of-band."""
    @tool("unapproved_erp_ledger_delete")
    def rogue_tool() -> str:
        """Dangerous operation attempting unauthorized database changes."""
        return "Executed"

    rogue_agent = Agent(
        role="Automated Operator", 
        goal="System cleanup", 
        backstory="Operational boundaries test.",
        tools=[rogue_tool], 
        allow_code_execution=False, 
        llm="mock-llm"
    )
    
    test_task = Task(description="Execute deletions.", expected_output="Success", agent=rogue_agent)
    crew = Crew(agents=[rogue_agent], tasks=[test_task])
    
    # Initialize using a completely clean file trace
    enforced_crew = GovAgentEnforcer(crew, policy_path=policy_file)
    
    with pytest.raises(PermissionError) as exc_info:
        rogue_agent.execute_task(test_task)
    
    assert "Unauthorized tool invocation blocked" in str(exc_info.value)


def test_govagent_crewai_dynamic_policy_routing(policy_file):
    """Validates model assignment maps precisely to YAML declarations through the bridge."""
    compliant_agent = Agent(
        role="Auditor", 
        goal="Review transactions", 
        backstory="Compliance reviewer.",
        tools=[], 
        llm="mock-llm"
    )
    
    test_task = Task(description="Analyze confidential payroll tables.", expected_output="Report", agent=compliant_agent)
    crew = Crew(agents=[compliant_agent], tasks=[test_task])
    enforced_crew = GovAgentEnforcer(crew, policy_path=policy_file)

    try:
        compliant_agent.execute_task(test_task)
    except Exception:
        pass

    yaml_target = enforced_crew.raw_config.get("routing_profiles", {}).get("default_local_slm", "")
    expected_model_name = yaml_target.split("/")[-1] if "/" in yaml_target else yaml_target

    assert compliant_agent.llm.model == expected_model_name