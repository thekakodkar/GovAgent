import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from govagent import ExecutiveAgent, tool
from govagent.telemetry.exporters.federated import FederatedTelemetryExporter
from govagent.context import reset_fiscal_ledger

load_dotenv()

# 1. LEGISLATED HORIZONTAL TOOLS
@tool(name="execute_financial_transaction", risk_level="high")
async def pay(amount: float, reference_id: str):
    """Executes an industry-agnostic disbursement after consensus is met."""
    return f"SUCCESS: Settled ${amount} for Reference: {reference_id}"

@tool(name="audit_transaction_logs", risk_level="low")
async def audit(trace_id: str):
    """Verifies ledger states for Article 12 forensic tracing."""
    return f"SUCCESS: Forensic verification matched for trace {trace_id}. No leaks detected."

async def run_live_swarm():
    # A. PURGE FISCAL MEMORY FOR CLEAN-ROOM RUN
    reset_fiscal_ledger()
    print("🏢 GOVAGENT v0.6.0: LIVE INTER-ORGANIZATION SWARM DEPLOYED\n" + "="*60)

    # B. INITIALIZE INDEPENDENT DISCRETE AGENTS
    director = ExecutiveAgent.bootstrap(
        policy_path="policies/finance_policy.yaml",
        llm=ChatOpenAI(model="gpt-4o", temperature=0)
    )
    
    auditor = ExecutiveAgent.bootstrap(
        policy_path="policies/audit_policy.yaml",
        llm=ChatOpenAI(model="gpt-4o", temperature=0)
    )

    # C. PILLAR 3: ESTABLISH FEDERATED CROSS-ORGANIZATION TELEMETRY
    federated_exporter = FederatedTelemetryExporter()
    
    # Enroll separate isolated compliance destinations representing distinct tenants
    federated_exporter.register_organization_sink("ORG_ALPHA_LOGISTICS", {"type": "SECURE_S3_LEDGER"})
    federated_exporter.register_organization_sink("ORG_BETA_RETAIL", {"type": "COMPLIANCE_KAFKA_STREAM"})
    
    # Attach the multi-tenant exporter directly into our agents' data collection engines
    director.telemetry.add_exporter(federated_exporter)
    auditor.telemetry.add_exporter(federated_exporter)

    # D. SECURE SWARM EXECUTION LOOP
    print("🤖 [Director] Initiating transaction loop across organizational boundary...")
    # This automatically runs: 1. Privacy scrubbing, 2. Dynamic Risk Tier Gating, 3. Role-Weighted Quorum
    tx_result = await director.execute("Disburse $150 to account reference vendor for invoice #882")

    # Manually configure the active session tenant payload mapping for verification
    snapshot = tx_result.model_dump()
    snapshot["organization_id"] = "ORG_ALPHA_MANUFACTURING"

    print(f"\n🤖 [Director] Delegating multi-tenant forensic audit to Auditor...")
    # Trace ID and tracking parameters are inherited by the downstream worker agent automatically
    final_report = await auditor.execute(f"Audit the logs for the last transaction.")

    # E. TRANSMIT FEDERATED LOG EVENTS
    print(f"\n🚀 Broadcasting session results to federated organization networks...")
    await federated_exporter.export(snapshot)

    print(f"\n🏁 LIVE RUN COMPLETE: Status={final_report.status.upper()}")

if __name__ == "__main__":
    asyncio.run(run_live_swarm())