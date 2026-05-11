import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path

# 1. Load institutional credentials
load_dotenv()

# 2. FIX: Explicitly import 'tool' and 'ExecutiveAgent'
from govagent import ExecutiveAgent, tool 
from langchain_openai import ChatOpenAI
# Load credentials before initializing the model

@tool(name="execute_financial_transaction", guards=["fiscal", "judiciary"], risk_level="high")
async def process_payment(amount: float, reference_id: str):
    """Executes a financial disbursement under institutional oversight."""
    return f"SUCCESS: Paid ${amount} for Ref: {reference_id}"

async def main():
    print("🏢 GOVAGENT v0.4.0: 60-SECOND QUICKSTART\n" + "="*45)
    
    agent = ExecutiveAgent.bootstrap(
        policy_path="policies/finance_policy.yaml",
        llm=ChatOpenAI(model="gpt-4o")
    )

    # Demonstrate Privacy Guard (Stage 0)
    task = "Process claim #882 for John Doe in the amount of $1200.00"
    print(f"🤖 Initializing Governed Execution for: {task}")
    
    report = await agent.execute(task)
    
    print(f"\n📊 --- INSTANT AUDIT ---")
    print(f"Status: {report.status.upper()}")
    print(f"Recursive TCO: ${report.recursive_tco_usd:.4f}") #
    print(f"Trace ID: {report.trace_id}") #

if __name__ == "__main__":
    asyncio.run(main())