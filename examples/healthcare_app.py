import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# LangChain / OpenAI Integration
from langchain_openai import ChatOpenAI

# GovAgent v0.2.3 Modular API
from govagent.agent import ExecutiveAgent
from govagent.policy import Policy
from govagent.registry import tool, registry
from govagent.hitl import HITLManager, SlackJudiciaryAdapter

# Load environment variables (API Keys, Slack Tokens)
load_dotenv()
base_path = Path(__file__).parent

# 1. Define Business-Specific Governed Tools
# v0.2.3: We explicitly define 'guards' to ensure multi-layer validation
@tool(name="authorize_claim_payment", risk_level="high", category="financial", guards=["fiscal", "judiciary"])
async def authorize_claim_payment(claim_id: str, amount: float):
    """
    Final business logic for disbursement. 
    Only reachable if Fiscal and Judiciary guards pass in the Agent.
    """
    # Note: In production, the tool calls evaluate() to trigger the interceptor
    await agent_instance.evaluate(
        guards=["fiscal", "judiciary"],
        value=amount,
        intent={"action": "authorize_claim_payment", "params": {"claim_id": claim_id, "amount": amount}},
        reason=f"Processing healthcare claim {claim_id}"
    )
    
    return {"status": "disbursed", "amount": amount, "claim_id": claim_id}

async def run_healthcare_agent():
    # 2. Infrastructure Setup
    policy_path = (base_path / "../policies/healthcare_ops_policy.yaml").resolve()
    if not policy_path.exists():
        raise FileNotFoundError(f"Policy file not found: {policy_path}")
        
    policy = Policy.from_yaml(policy_path)
    
    # 3. Judiciary Setup (Slack Socket Mode)
    # Mirroring your working Slack configuration for real-time human oversight
    adapter = SlackJudiciaryAdapter(
        bot_token=os.getenv("SLACK_BOT_TOKEN"),
        app_token=os.getenv("SLACK_APP_TOKEN"),
        channel_id=os.getenv("SLACK_CHANNEL_ID")
    )
    adapter.start()
    
    # 4. Bootstrap the Executive Engine
    # Injecting GPT-4o as the 'Engine' and GovAgent as the 'Control Plane'
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    global agent_instance
    agent_instance = ExecutiveAgent(
        persona="Healthcare Billing Director",
        policy=policy,
        model_client=llm,
        hitl_manager=HITLManager(adapter=adapter)
    )

    # 5. v0.2.0 Compliance Audit: Alignment Check
    policy.validate_registry()
    print("🛡️ GovAgent: Healthcare Instance Online & Audited.")

    # 6. Execute Governed Task
    # The LLM will identify the need for payment, but the Guard will intercept.
    task = "Process claim #7742 for $1,250.00 for the outpatient procedure."
    
    try:
        print(f"\n🚀 Starting Task: {task}")
        report = await agent_instance.execute(task)
        print(f"\n🏁 Session Status: {report.status}")
    except Exception as e:
        print(f"\n🛑 Governance Stop: {e}")

if __name__ == "__main__":
    asyncio.run(run_healthcare_agent())