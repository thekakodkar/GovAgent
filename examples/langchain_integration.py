import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# LangChain & OpenAI Imports
from langchain_openai import ChatOpenAI
from govagent import ExecutiveAgent, tool # Using our new v0.3.0 'tool' decorator

load_dotenv()
BASE_DIR = Path(__file__).parent

# v0.3.0: ZERO Boilerplate Tool. Governance is injected automatically.
@tool(name="execute_financial_transaction", guards=["fiscal", "judiciary"], risk_level="high")
async def execute_financial_transaction(amount: float, reference_id: str = "UNKNOWN") -> str:
    """
    Authorizes and executes a financial disbursement.
    Used for claims, refunds, payroll, or vendor payments.
    """
    return f"SUCCESS: Transaction of ${amount} for Ref: {reference_id} processed."

async def run_scenario(persona: str, policy_file: str, task: str, delay: int):
    """Worker function to simulate concurrent governed sessions."""
    await asyncio.sleep(delay) # Stagger start times
    
    print(f"🚀 [{persona}] Initializing Session...")
    
    # v0.3.0: One-line Institutional Bootstrap
    agent = ExecutiveAgent.bootstrap(
        policy_path=BASE_DIR / f"../policies/{policy_file}",
        llm=ChatOpenAI(model="gpt-4o", temperature=0),
        slack_channel=os.getenv("SLACK_CHANNEL_ID")
    )

    print(f"🤖 [{persona}] Task: {task}")
    try:
        report = await agent.execute(task)
        print(f"🏁 [{persona}] Status: {report.status} | Cost: ${report.estimated_cost_usd}")
    except Exception as e:
        print(f"🛑 [{persona}] Governance Halt: {e}")

async def main():
    print("🏢 STARTING MULTI-AGENT GOVERNANCE STRESS TEST (v0.3.0)\n" + "="*55)

    # We run two different directors with different policies concurrently
    # Scenario A: Billing Director (High Limit)
    # Scenario B: Junior Clerk (Low Limit - should trigger rejection or block)
    
    tasks = [
        run_scenario(
            persona="Billing_Director", 
            policy_file="langchain_integration_sample_policy.yaml",
            task="Process a reimbursement for claim #882 in the amount of $1200.",
            delay=0
        ),
        run_scenario(
            persona="Compliance_Auditor", 
            policy_file="auditor_policy.yaml", # Assume this policy has lower fiscal limits
            task="Approve urgent payment for claim #995 for $5000.00.",
            delay=1 # Starts slightly after to test async context isolation
        )
    ]

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())