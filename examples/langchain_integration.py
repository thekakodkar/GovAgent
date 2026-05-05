import asyncio
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# LangChain & GovAgent Imports
from langchain_core.tools import tool as langchain_tool

# GovAgent v0.2.2 Flat API
from govagent import ExecutiveAgent, Policy, HITLManager, SlackJudiciaryAdapter

load_dotenv()
BASE_DIR = Path(__file__).parent

@langchain_tool
async def healthcare_payment_tool(amount: float) -> str:
    """Authorizes payments for healthcare claims. Input: amount."""
    
    # 1. Setup Slack Adapter (Mirroring your working test)
    adapter = SlackJudiciaryAdapter(
        bot_token=os.getenv("SLACK_BOT_TOKEN"),
        app_token=os.getenv("SLACK_APP_TOKEN"),
        channel_id=os.getenv("SLACK_CHANNEL_ID")
    )
    adapter.start() # Start Socket Mode listener
    
    # 2. Setup Manager & Policy
    manager = HITLManager(adapter=adapter)
    policy = Policy.from_yaml(BASE_DIR / "../policies/langchain_integration_sample_policy.yaml")
    
    # 3. Initialize Agent
    agent = ExecutiveAgent(
        persona="Healthcare Billing Director",
        policy=policy,
        model_client=None,
        hitl_manager=manager
    )

    print(f"\n⚖️ [GovAgent] Intercepting request for ${amount}...")

    # 4. ARTICLE 14: Use the 'secure_approval' method from your working test
    # We call the manager directly to ensure the Slack handshake happens
    approved = await manager.secure_approval(
        agent_id="Healthcare-Director-v0.3.0",
        reason=f"Authorization required for GuardedPayment (${amount}).",
        context={
            "amount": f"${amount}",
            "tool": "GuardedPayment",
            "compliance_check": "EU-AI-ACT-HIGH-RISK"
        }
    )

    if approved:
        # In a real app, this would call your business logic
        return f"SUCCESS: Payment of ${amount} was approved via Slack."
    else:
        return "REJECTED: The transaction was denied by the Human Judiciary in Slack."

async def main():
    print("🚀 Starting Governed LangChain Session (Slack Mode)...")
    # Simulate a high-risk tool call
    result = await healthcare_payment_tool.ainvoke({"amount": 1200.0})
    print(f"\n🏁 Final System Output: {result}")

if __name__ == "__main__":
    asyncio.run(main())