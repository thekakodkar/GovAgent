import asyncio
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# LangChain & OpenAI Imports
from langchain_openai import ChatOpenAI
from govagent import ExecutiveAgent, tool 
from govagent.exporters.base import BaseExporter
from govagent.exporters.cloudwatch import CloudWatchExporter

load_dotenv()
BASE_DIR = Path(__file__).parent

# --- PILLAR 4: INSTITUTIONAL MOCK EXPORTER ---
class MockSOCExporter(BaseExporter):
    """Forensic Sink for Local Validation."""
    async def export(self, snapshot_data: Dict[str, Any]) -> bool:
        print(f"📡 [MOCK SOC] Dispatching Trace: {snapshot_data.get('trace_id')}")
        print(f"💰 [MOCK SOC] Recursive TCO: ${snapshot_data.get('recursive_tco_usd', 0):.4f}")
        return True

# --- PILLAR 1: DETERMINISTIC TOOLING ---
@tool(name="execute_financial_transaction", guards=["fiscal", "judiciary"], risk_level="high")
async def execute_financial_transaction(amount: float, reference_id: str = "UNKNOWN") -> str:
    """Authorizes and executes a financial disbursement."""
    return f"SUCCESS: Transaction of ${amount} for Ref: {reference_id} processed."

async def run_governed_swarm():
    """
    v0.4.0 Stress Test: Full Control Plane Activation.
    """
    print("🏢 INITIALIZING INSTITUTIONAL CONTROL PLANE (v0.4.0)\n" + "="*55)
    
    # 1. COMMISSION THE DIRECTOR (Must happen first to avoid UnboundLocalError)
    # This establishes the base context and policy alignment.
    agent = ExecutiveAgent.bootstrap(
        policy_path=BASE_DIR / "../policies/langchain_integration_sample_policy.yaml",
        llm=ChatOpenAI(model="gpt-4o", temperature=0),
        slack_channel=os.getenv("SLACK_CHANNEL_ID")
    )

    # 2. ENROLL FORENSIC SINKS (The Hybrid SOC Handshake)
    # We check for credentials to determine the destination of the Evidence Stream.
    aws_ready = all([os.getenv("AWS_ACCESS_KEY_ID"), os.getenv("AWS_DEFAULT_REGION")])
    
    if aws_ready:
        print("☁️ [SOC] AWS Credentials detected. Enrolling CloudWatch Exporter.")
        cw_exporter = CloudWatchExporter(log_group="/aws/govagent/stress-test")
        agent.telemetry.add_exporter(cw_exporter)
    else:
        print("⚠️ [SOC] AWS Credentials missing. Enrolling Mock Forensic Sink.")
        agent.telemetry.add_exporter(MockSOCExporter())

    # 3. TASK EXECUTION: Triggers PII scrubbing and Recursive TCO
    task = "Process claim #882 for John Doe ($1200.00) and audit the transaction logs."
    
    print(f"🤖 [Director] Sanitizing task and initiating governance cycle...")
     
    # FIX: Explicitly await the execution to resolve the Snapshot object
    report = await agent.execute(task) 
    
    # Now that the coroutine is resolved, 'report' is an ExecutionSnapshot
    print(f"\n📊 --- INSTITUTIONAL AUDIT REPORT ---")
    print(f"Status: {report.status.upper()}")
    print(f"Trace ID: {report.trace_id}")
    print(f"Individual Cost: ${report.estimated_cost_usd:.4f}")
    print(f"Recursive Swarm TCO: ${report.recursive_tco_usd:.4f}") #

if __name__ == "__main__":
    # Standard entry point for async institutional workloads
    asyncio.run(run_governed_swarm())