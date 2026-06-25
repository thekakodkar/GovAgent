import asyncio
import os
import json
from dotenv import load_dotenv
from govagent import ExecutiveAgent, tool, Policy, PolicyBasedRouter, RouterConfig
from govagent.llm.ollama import OllamaClient
from govagent.telemetry.exporters import MockSOCExporter
from govagent.governance.meta import MetaGovernor

load_dotenv()

@tool(name="execute_financial_transaction", risk_level="high")
async def pay(amount: float, reference_id: str):
    """Executes an industry-agnostic payment following Role-Weighted Quorum validation."""
    return f"SUCCESS: Transacted ${amount} under Reference: {reference_id}"

@tool(name="audit_transaction_logs", risk_level="low")
async def audit():
    """Verifies logs for Article 12 forensic compliance."""
    return "SUCCESS: Cross-org audit trail verified for multi-tenant isolation."

async def main():
    print("🏢 GOVAGENT v1.0.0: LOCAL SWARM ORCHESTRATION & OPTIMIZATION\n" + "="*60)

    clients = {
        "local_ollama": OllamaClient(config={"base_url": "http://localhost:11434", "model": "llama3"})
    }
    
    router_cfg = RouterConfig(routing_mode="LOCAL_ONLY", default_provider="local_ollama")
    router = PolicyBasedRouter(clients=clients, config=router_cfg)

    # Natively attach corresponding policy frameworks
    director = ExecutiveAgent.bootstrap(
        policy_path="policies/finance_policy.yaml",
        router_client=router
    )

    auditor = ExecutiveAgent.bootstrap(
        policy_path="policies/audit_policy.yaml",
        router_client=router
    )

    shared_soc = MockSOCExporter()
    director.telemetry.add_exporter(shared_soc)
    auditor.telemetry.add_exporter(shared_soc)

    print("🤖 [Director] Ingesting instruction and evaluating risk tier...")
    tx_report = await director.execute("Reimburse patient contract for $150.00")
    
    print(f"\n🤖 [Director] Delegating forensic verification to Auditor...")
    audit_report = await auditor.execute(f"Verify the logs for Trace ID: {tx_report.trace_id}")

    print(f"\n📊 --- FEDERATED SWARM AUDIT SUMMARY ---")
    print(f"Director Status: {tx_report.status.upper()}")
    print(f"Auditor Status:  {audit_report.status.upper()}")
    print(f"Traceability:    {'VERIFIED' if tx_report.trace_id else 'FAILED'}")

    print("\n🔄 --- PILLAR 1: AUTOMATED POLICY TUNING HANDSHAKE ---")
    mock_log_path = "logs/audit_buffer.jsonl"
    os.makedirs(os.path.dirname(mock_log_path), exist_ok=True)
    
    mock_friction_entry = {
        "status": "BLOCKED: RECURSIVE_TCO_REJECT",
        "policy_id": "finance_policy.yaml",
        "metrics": {"recursive_tco_usd": 100.0, "requested_amount": 150.0}
    }
    with open(mock_log_path, "w") as f:
        for _ in range(3):
            f.write(json.dumps(mock_friction_entry) + "\n")

    print(f"🔬 MetaGovernor: Evaluating log file '{mock_log_path}' for operational friction...")
    governor = MetaGovernor(log_path=mock_log_path, friction_threshold=3)
    analysis = governor.analyze_friction()
    
    print(f"📋 Optimization Result: {analysis['type']}")
    print(f"🎯 Proposed Budget Adjustments: Limit raised to ${analysis['proposed_limit']:.2f} USD (with 10% safety margin)")

if __name__ == "__main__":
    asyncio.run(main())