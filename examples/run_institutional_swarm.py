import asyncio
import os
from dotenv import load_dotenv
from govagent import ExecutiveAgent, tool, Policy, PolicyBasedRouter, RouterConfig
from govagent.llm.ollama import OllamaClient
from govagent.telemetry.exporters.federated import FederatedTelemetryExporter
from govagent.context import reset_fiscal_ledger

load_dotenv()

@tool(name="execute_financial_transaction", risk_level="high")
async def pay(amount: float, reference_id: str):
    """Executes an industry-agnostic disbursement after consensus is met."""
    return f"SUCCESS: Settled ${amount} for Reference: {reference_id}"

@tool(name="audit_transaction_logs", risk_level="low")
async def audit(trace_id: str):
    """Verifies ledger states for Article 12 forensic tracing."""
    return f"SUCCESS: Forensic verification matched for trace {trace_id}. No leaks detected."

async def run_live_swarm():
    reset_fiscal_ledger()
    print("🏢 GOVAGENT v1.0.0: LIVE INTER-ORGANIZATION SWARM DEPLOYED\n" + "="*60)

    clients = {
        "local_ollama": OllamaClient(config={"base_url": "http://localhost:11434", "model": "llama3"})
    }
    router_cfg = RouterConfig(routing_mode="LOCAL_ONLY", default_provider="local_ollama")
    router = PolicyBasedRouter(clients=clients, config=router_cfg)

    director = ExecutiveAgent.bootstrap(
        policy_path="policies/finance_policy.yaml",
        router_client=router
    )
    
    auditor = ExecutiveAgent.bootstrap(
        policy_path="policies/audit_policy.yaml",
        router_client=router
    )

    federated_exporter = FederatedTelemetryExporter()
    federated_exporter.register_organization_sink("ORG_ALPHA_LOGISTICS", {"type": "SECURE_S3_LEDGER"})
    federated_exporter.register_organization_sink("ORG_BETA_RETAIL", {"type": "COMPLIANCE_KAFKA_STREAM"})
    
    director.telemetry.add_exporter(federated_exporter)
    auditor.telemetry.add_exporter(federated_exporter)

    print("🤖 [Director] Initiating transaction loop across organizational boundary...")
    tx_result = await director.execute("Disburse $150 to account reference vendor for invoice #882")

    snapshot = tx_result.model_dump()
    snapshot["organization_id"] = "ORG_ALPHA_MANUFACTURING"

    print(f"\n🤖 [Director] Delegating multi-tenant forensic audit to Auditor...")
    final_report = await auditor.execute(f"Audit the logs for the last transaction.")

    print(f"\n🚀 Broadcasting session results to federated organization networks...")
    await federated_exporter.export(snapshot)

    print(f"\n🏁 LIVE RUN COMPLETE: Status={final_report.status.upper()}")

if __name__ == "__main__":
    asyncio.run(run_live_swarm())