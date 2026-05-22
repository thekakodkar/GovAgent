import asyncio
import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from govagent import ExecutiveAgent, tool
from govagent.telemetry.exporters import MockSOCExporter
from govagent.governance.meta import MetaGovernor

load_dotenv()

# 1. LEGISLATED GOVERNED TOOLS
@tool(name="execute_financial_transaction", risk_level="high")
async def pay(amount: float, reference_id: str):
    """Executes an industry-agnostic payment following Role-Weighted Quorum validation."""
    return f"SUCCESS: Transacted ${amount} under Reference: {reference_id}"

@tool(name="audit_transaction_logs", risk_level="low")
async def audit():
    """Verifies logs for Article 12 forensic compliance."""
    return "SUCCESS: Cross-org audit trail verified for multi-tenant isolation."

async def main():
    print("🏢 GOVAGENT v0.6.0: LOCAL SWARM ORCHESTRATION & OPTIMIZATION\n" + "="*60)

    # 2. INITIALIZE JURISDICTIONS (Natively attaching policy frameworks)
    director = ExecutiveAgent.bootstrap(
        policy_path="policies/finance_policy.yaml",
        llm=ChatOpenAI(model="gpt-4o", temperature=0)
    )

    auditor = ExecutiveAgent.bootstrap(
        policy_path="policies/audit_policy.yaml",
        llm=ChatOpenAI(model="gpt-4o", temperature=0)
    )

    # 3. ENROLL SYSTEMIC FORENSIC SINKS & TARGET TENANT IDENTITY
    shared_soc = MockSOCExporter()
    director.telemetry.add_exporter(shared_soc)
    auditor.telemetry.add_exporter(shared_soc)

    # 4. EXECUTION: Director processes high-risk task using Role-Weighted Quorum
    print("🤖 [Director] Ingesting instruction and evaluating risk tier...")
    tx_report = await director.execute("Reimburse patient contract for $150.00")
    
    # 5. SWARM DELEGATION: Trace ID inheritance ensures Article 12 compliance
    print(f"\n🤖 [Director] Delegating forensic verification to Auditor...")
    audit_report = await auditor.execute(f"Verify the logs for Trace ID: {tx_report.trace_id}")

    print(f"\n📊 --- FEDERATED SWARM AUDIT SUMMARY ---")
    print(f"Director Status: {tx_report.status.upper()}")
    print(f"Auditor Status:  {audit_report.status.upper()}")
    print(f"Traceability:    {'VERIFIED' if tx_report.trace_id else 'FAILED'}")

    # 6. DEMONSTRATE PILLAR 1: Self-Healing Meta-Governor Ingestion Loop
    print("\n🔄 --- PILLAR 1: AUTOMATED POLICY TUNING HANDSHAKE ---")
    mock_log_path = "logs/audit_buffer.jsonl"
    os.makedirs(os.path.dirname(mock_log_path), exist_ok=True)
    
    # Simulate recurring fiscal friction overruns (3 repetitive blocks) to trigger tuning
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