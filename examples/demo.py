import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from govagent import ExecutiveAgent, tool
from govagent.telemetry.exporters import MockSOCExporter

load_dotenv()

# 1. DEFINE SHARED TOOLS
@tool(name="execute_financial_transaction", risk_level="high")
async def pay(amount: float, reference_id: str):
    return f"SUCCESS: Transacted ${amount}"

@tool(name="audit_transaction_logs", risk_level="low")
async def audit():
    return "SUCCESS: Audit trail verified for Article 12."

async def main():
    print("🏢 GOVAGENT v0.6.0: FEDERATED SWARM ORCHESTRATION\n" + "="*55)

    # 2. INITIALIZE THE DIRECTOR (Healthcare Finance Policy)
    director = ExecutiveAgent.bootstrap(
        policy_path="policies/finance_policy.yaml",
        llm=ChatOpenAI(model="gpt-4o", temperature=0)
    )

    # 3. INITIALIZE THE AUDITOR (Audit Policy)
    auditor = ExecutiveAgent.bootstrap(
        policy_path="policies/audit_policy.yaml",
        llm=ChatOpenAI(model="gpt-4o", temperature=0)
    )

    # 4. ENROLL SHARED FORENSIC SINK
    shared_soc = MockSOCExporter()
    director.telemetry.add_exporter(shared_soc)
    auditor.telemetry.add_exporter(shared_soc)

    # 5. EXECUTION: Director performs transaction, then delegates audit to Auditor
    print("🤖 [Director] Processing high-risk transaction...")
    tx_report = await director.execute("Reimburse patient #442 for $150.00")
    
    print(f"\n🤖 [Director] Delegating forensic verification to Auditor...")
    # Trace ID inheritance ensures Article 12 continuity
    audit_report = await auditor.execute(f"Verify the logs for Trace ID: {tx_report.trace_id}")

    print(f"\n📊 --- FEDERATED SWARM AUDIT ---")
    print(f"Director Status: {tx_report.status.upper()}")
    print(f"Auditor Status: {audit_report.status.upper()}")
    print(f"Aggregated Traceability: {'VERIFIED' if tx_report.trace_id else 'FAILED'}")

if __name__ == "__main__":
    asyncio.run(main())