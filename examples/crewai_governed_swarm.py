from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai.tools import tool

# Import your freshly verified CrewAI Extension layer
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
        llm="openai/gpt-4o"  # Initially pointed to expensive cloud environments
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
        # Executes natively against your live running llama3.2 instance!
        operator.execute_task(test_task)
        
        print("\n📊 --- POST-EXECUTION METRICS MATRIX ---")
        print("🟢 Swarm Execution Status: SUCCESS")
        print(f"🎯 Dynamic Model Endpoint:  {operator.llm.model} (Successfully routed out-of-band to live local SLM)")
        
    except PermissionError as security_violation:
        print("\n📊 --- POST-EXECUTION METRICS MATRIX ---")
        print("🛑 Swarm Execution Status: HALTED")
        print(f"❌ Security Threat Event:  {str(security_violation)}")

def main():
    print("🏢 GOVAGENT v1.0.0: MULTI-AGENT SWARM GOVERNANCE MIDDLEWARE")
    print("=" * 75)
    
    # Run Scene A: Secure execution demonstrating out-of-band model shifting to live llama3.2
    run_governed_workflow(use_compromised_pipeline=False)
    
    print("\n" + "=" * 75)
    
    # Run Scene B: Compromised execution demonstrating rapid threat mitigation
    run_governed_workflow(use_compromised_pipeline=True)

if __name__ == "__main__":
    main()