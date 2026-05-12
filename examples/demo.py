import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path
from govagent import ExecutiveAgent, tool 
from langchain_openai import ChatOpenAI

# 1. Load institutional credentials
load_dotenv()

@tool(name="execute_financial_transaction", guards=["fiscal", "judiciary"], risk_level="high")
async def process_payment(amount: float, reference_id: str):
    """Executes a financial disbursement under institutional oversight."""
    return f"SUCCESS: Paid ${amount} for Ref: {reference_id}"

async def main():
    print("🏢 GOVAGENT v0.5.0: FEDERATED JUDICIARY QUICKSTART\n" + "="*45)
    
    # Bootstrap initializes Judiciary, Alignment, and Telemetry layers
    agent = ExecutiveAgent.bootstrap(
        policy_path="policies/finance_policy.yaml",
        llm=ChatOpenAI(model="gpt-4o", temperature=0)
    )

    # Triggering Article 9 Privacy Redaction (Stage 0)
    task = "Process claim #882 for John Doe in the amount of $1200.00"
    print(f"🤖 Initializing Governed Execution for: {task}")
    
    # Resolved report is now an ExecutionSnapshot with Federated Quorum data
    report = await agent.execute(task)
    
    print(f"\n📊 --- INSTITUTIONAL AUDIT ---")
    print(f"Status: {report.status.upper()}")
    print(f"Recursive TCO: ${report.recursive_tco_usd:.4f}") # Swarm-wide fiscality
    print(f"Trace ID: {report.trace_id}") # Forensic ID for Article 12
    print(f"Guards Evaluated: {', '.join(report.guards_evaluated)}") # Verification trail

if __name__ == "__main__":
    asyncio.run(main())