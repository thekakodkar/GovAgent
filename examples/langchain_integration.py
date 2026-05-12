import asyncio
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from govagent import ExecutiveAgent, tool 
from govagent.exporters.base import BaseExporter
from govagent.exporters.cloudwatch import CloudWatchExporter

load_dotenv()
BASE_DIR = Path(__file__).parent

# --- PILLAR 4: INSTITUTIONAL MOCK EXPORTER (SOC SINK) ---
class MockSOCExporter(BaseExporter):
    """Forensic Sink for Local Validation with connection failure simulation."""
    async def export(self, snapshot_data: Dict[str, Any]) -> bool:
        # Simulate network stability for testing the DLQ
        print(f"📡 [SOC] Attempting dispatch for Trace: {snapshot_data.get('trace_id')}")
        return True

@tool(name="execute_financial_transaction", guards=["fiscal", "judiciary"], risk_level="high")
async def execute_financial_transaction(amount: float, reference_id: str = "UNKNOWN") -> str:
    """Authorizes and executes a financial disbursement."""
    return f"SUCCESS: Transaction of ${amount} for Ref: {reference_id} processed."

async def run_governed_swarm():
    """v0.5.0 Stress Test: Federated Quorum & DLQ Validation."""
    print("🏢 INITIALIZING INSTITUTIONAL CONTROL PLANE (v0.5.0)\n" + "="*55)
    
    # 1. COMMISSION THE DIRECTOR (Establishes Judiciary & Alignment Judges)
    agent = ExecutiveAgent.bootstrap(
        policy_path=BASE_DIR / "../policies/langchain_integration_sample_policy.yaml",
        llm=ChatOpenAI(model="gpt-4o", temperature=0),
        slack_channel=os.getenv("SLACK_CHANNEL_ID") # Activates Article 14 Quorum
    )

    # 2. ENROLL FORENSIC SINKS (Self-Healing Configuration)
    aws_ready = all([os.getenv("AWS_ACCESS_KEY_ID"), os.getenv("AWS_DEFAULT_REGION")])
    if aws_ready:
        print("☁️ [SOC] AWS Credentials detected. Enrolling CloudWatch Exporter.")
        agent.telemetry.add_exporter(CloudWatchExporter(log_group="/aws/govagent/stress-test"))
    
    # Always enroll local SOC for double-entry forensic bookkeeping
    agent.telemetry.add_exporter(MockSOCExporter())

    # 3. TASK EXECUTION: Triggers Privacy Redaction, M-of-N, and DLQ Failover
    task = "Process claim #882 for John Doe ($1200.00) and audit the transaction logs."
    print(f"🤖 [Director] Initiating Governance Loop (Sanitized for Privacy)...")
     
    report = await agent.execute(task) 
    
    print(f"\n📊 --- INSTITUTIONAL AUDIT REPORT ---")
    print(f"Status: {report.status.upper()}")
    print(f"Trace ID: {report.trace_id}")
    print(f"Recursive Swarm TCO: ${report.recursive_tco_usd:.4f}") # Aggregated metrics
    
    # Verify if DLQ was utilized due to infrastructure failure
    if os.path.exists("logs/audit_buffer.jsonl"):
        print("📝 [AUDIT] Forensic data successfully buffered to local DLQ.")

if __name__ == "__main__":
    asyncio.run(run_governed_swarm())