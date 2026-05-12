import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from govagent import ExecutiveAgent, tool
from govagent.telemetry.exporters import MockSOCExporter, CloudWatchExporter
from govagent.context import reset_fiscal_ledger

load_dotenv()

# 1. LEGISLATED TOOLS
@tool(name="execute_financial_transaction", risk_level="high")
async def pay(amount: float, reference_id: str):
    """Executes a payment after Article 14 approval."""
    return f"SUCCESS: Paid ${amount} for Reference: {reference_id}"

@tool(name="audit_transaction_logs", risk_level="low")
async def audit(trace_id: str):
    """Verifies logs for Article 12 forensic integrity."""
    return f"SUCCESS: Forensic match found for {trace_id}. No anomalies."

async def run_live_swarm():
    # A. INSTITUTIONAL CLEANUP
    reset_fiscal_ledger()
    print("🏢 GOVAGENT v0.6.0: LIVE FEDERATED SWARM ACTIVE\n" + "="*55)

    # B. INITIALIZE JURISDICTIONS
    director = ExecutiveAgent.bootstrap(
        policy_path="policies/finance_policy.yaml",
        llm=ChatOpenAI(model="gpt-4o", temperature=0)
    )
    
    auditor = ExecutiveAgent.bootstrap(
        policy_path="policies/audit_policy.yaml",
        llm=ChatOpenAI(model="gpt-4o", temperature=0)
    )

    # C. ESTABLISH MULTI-CLOUD FORENSICS
    # In production, this streams to your Enterprise SOC
    forensic_sink = MockSOCExporter()
    director.telemetry.add_exporter(forensic_sink)
    auditor.telemetry.add_exporter(forensic_sink)

    # D. EXECUTION LOOP
    print("🤖 [Director] Initiating High-Risk Patient Reimbursement...")
    # This will trigger: 1. PII Redaction, 2. Fiscal Check, 3. M-of-N Quorum
    tx_result = await director.execute("Pay $150 to John Doe for Patient ID #882")

    print(f"\n🤖 [Director] Delegating Forensic Verification to Auditor...")
    # Inheritance: Auditor receives the Director's Trace ID automatically
    final_report = await auditor.execute(f"Audit the logs for the last transaction.")

    print(f"\n📊 SWARM METRICS: TCO=${tx_result.metrics.get('fiscal_impact', 0.0)} | Status={final_report.status.upper()}")

if __name__ == "__main__":
    asyncio.run(run_live_swarm())