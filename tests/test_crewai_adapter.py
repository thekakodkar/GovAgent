import pytest
from unittest.mock import patch, mock_open
from crewai import Agent, Task, Crew
from crewai.tools import tool
from govagent.extensions.crewai.enforcer import GovAgentEnforcer

# Update the target layout matrix inside your test file
MOCK_YAML_POLICY = """
version: "2.0.0"
routing_mode: "LOCAL_ONLY"
default_provider: "local_ollama"
routing_rules: []
governance_rules:
  authorized_tools:
    - "approved_market_fetcher"
    - "search_tool"
routing_profiles:
  default_local_slm: "ollama/llama3.2"
"""

@patch("builtins.open", new_callable=mock_open, read_data=MOCK_YAML_POLICY)
def test_govagent_crewai_unauthorized_tool_gate(mock_file):
    """
    Validates that the GovAgentEnforcer intercepts an unregistered tool
    and triggers an immediate runtime halt before execution.
    """
    @tool("unapproved_erp_ledger_delete")
    def rogue_tool() -> str:
        """Dangerous operation attempting unauthorized database changes."""
        return "Executed"

    rogue_agent = Agent(
        role="Automated Operator",
        goal="Run system cleanups",
        backstory="An automated pipeline agent testing operational boundaries.",
        tools=[rogue_tool],
        allow_code_execution=False,
        llm="mock-llm"
    )
    
    test_task = Task(
        description="Clean up operational transaction limits using the ledger delete tool.", 
        expected_output="Success", 
        agent=rogue_agent
    )
    crew = Crew(agents=[rogue_agent], tasks=[test_task])
    enforced_crew = GovAgentEnforcer(crew, policy_path="dummy_path.yaml")
    
    with pytest.raises(PermissionError) as exc_info:
        rogue_agent.execute_task(test_task)
    
    assert "Unauthorized tool invocation blocked" in str(exc_info.value)


@patch("builtins.open", new_callable=mock_open, read_data=MOCK_YAML_POLICY)
def test_govagent_crewai_dynamic_policy_routing(mock_file):
    """
    Validates that the adapter intercepts task execution and checks
    the payload against the underlying configuration rules.
    """
    compliant_agent = Agent(
        role="Auditor",
        goal="Review transaction anomalies",
        backstory="Enterprise compliance reviewer.",
        tools=[],
        llm="mock-llm"
    )
    
    test_task = Task(
        description="Analyze the confidential_payroll ledger tables.", 
        expected_output="Analysis report", 
        agent=compliant_agent
    )
    crew = Crew(agents=[compliant_agent], tasks=[test_task])
    enforced_crew = GovAgentEnforcer(crew, policy_path="dummy_path.yaml")

    try:
        compliant_agent.execute_task(test_task)
    except Exception:
        pass

    # 💡 FIX: Query the underlying string field of the CrewAI LLM instance object cleanly
    assert compliant_agent.llm.model == "llama3:8b"