import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# LangChain & OpenAI Imports
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool as langchain_tool

# GovAgent v0.2.3 Modular API
from govagent import ExecutiveAgent, Policy, HITLManager, SlackJudiciaryAdapter

load_dotenv()
BASE_DIR = Path(__file__).parent

@langchain_tool
async def healthcare_payment_tool(amount: float) -> str:
    """
    Authorizes payments for healthcare claims. 
    Use this tool only when a specific disbursement amount is identified.
    """
    # Note: In a production environment, the agent and policy should be 
    # initialized once at the application level, not inside the tool.
    
    # Access the globally configured agent/policy (simplified for this demo)
    # We use the centralized 'evaluate' to protect the OpenAI session ROI.
    await agent.evaluate(
        guards=["fiscal", "judiciary"],
        value=amount,
        intent={"action": "healthcare_payment_tool", "params": {"amount": amount}},
        reason=f"LLM requested a healthcare disbursement of ${amount}"
    )

    return f"SUCCESS: Disbursement of ${amount} processed via Governed Pipe."

async def main():
    print("🚀 Initializing Governed LLM Session (OpenAI + Slack)...")

    # 1. Initialize the LLM (The Engine)
    # We use gpt-4o for complex reasoning while GovAgent handles the safety.
    llm = ChatOpenAI(
        model="gpt-4o", 
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0
    )

    # 2. Setup GovAgent Control Plane
    adapter = SlackJudiciaryAdapter(
        bot_token=os.getenv("SLACK_BOT_TOKEN"),
        app_token=os.getenv("SLACK_APP_TOKEN"),
        channel_id=os.getenv("SLACK_CHANNEL_ID")
    )
    adapter.start()
    
    manager = HITLManager(adapter=adapter)
    policy = Policy.from_yaml(BASE_DIR / "../policies/langchain_integration_sample_policy.yaml")

    # 3. Initialize the ExecutiveAgent
    # Global 'agent' variable so the tool can access it (for demo purposes)
    global agent
    agent = ExecutiveAgent(
        persona="Healthcare Billing Director",
        policy=policy,
        model_client=llm,
        hitl_manager=manager
    )

    # 4. EXECUTING THE GOVERNED LOOP
    # The LLM will parse this task, decide to use the tool, 
    # and then be intercepted by your v0.2.3 Guards.
    task = "I need to process a reimbursement for claim #882 in the amount of $1200."
    
    try:
        print(f"🤖 Task: {task}")
        result = await agent.execute(task)
        print(f"\n🏁 Final System Output: {result.status}")
    except Exception as e:
        print(f"\n🛑 Governance Circuit Breaker: {e}")

if __name__ == "__main__":
    asyncio.run(main())