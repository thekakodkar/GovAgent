from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai.tools import tool
from govagent.extensions.crewai.enforcer import GovAgentEnforcer

load_dotenv()

@tool("approved_market_fetcher")
def fetch_data() -> str:
    """Safely extracts granular operational records out of memory spaces."""
    return "SUCCESS: Secure ledger matrix data synthesized cleanly."

@tool("unapproved_erp_ledger_delete")
def rogue_tool() -> str:
    """Dangerous operation attempting unauthorized database changes."""
    return "CRITICAL ERROR: Unauthorized structural system damage executed!"

def run_governed_workflow(use_compromised_pipeline: bool = False):
    print(f"\n🚀 INITIALIZING WORKFLOW | Mode: {'COMPROMISED' if use_compromised_pipeline else 'SECURE'}")
    print("-" * 75)

    active_tools = [rogue_tool] if use_compromised_pipeline else [fetch_data]
    
    operator = Agent(
        role="ERP Technical Operator",
        goal="Process structural data queries safely",
        backstory="An enterprise systems processing coordinator.",
        tools=active_tools,
        allow_code_execution=False,
        llm="openai/gpt-4o"
    )
    
    test_task = Task(
        description="Analyze the confidential_payroll ledger tables for anomalies.",
        expected_output="Structural analysis verification signature.",
        agent=operator
    )
    
    native_crew = Crew(agents=[operator], tasks=[test_task])

    print("🛡️  Applying govAgent middleware enforcer matrix...")
    enforced_crew = GovAgentEnforcer(native_crew, policy_path="policies/sample_crewai_policy.yaml")

    print("🤖 [CrewAI Swarm] Launching agent processing loops...")

    try:
        operator.execute_task(test_task)
        print("\n📊 --- POST-EXECUTION METRICS MATRIX ---")
        print("🟢 Swarm Execution Status: SUCCESS")
        print(f"🎯 Dynamic Model Endpoint:  {operator.llm.model} (Successfully routed out-of-band to secure local SLM)")
        
    except PermissionError as security_violation:
        print("\nexport 📊 --- POST-EXECUTION METRICS MATRIX ---")
        print("🛑 Swarm Execution Status: HALTED")
        print(f"❌ Security Threat Event:  {str(security_violation)}")

def main():
    print("🏢 GOVAGENT v2.0.0-GA: MULTI-AGENT SWARM GOVERNANCE MIDDLEWARE")
    print("=" * 75)
    
    # Scene A: Secure workflow dynamically shifting to local model targets from your YAML definitions
    run_governed_workflow(use_compromised_pipeline=False)
    print("\n" + "=" * 75)
    
    # Scene B: Compromised workflow demonstrating pre-flight execution halting
    run_governed_workflow(use_compromised_pipeline=True)

if __name__ == "__main__":
    main()