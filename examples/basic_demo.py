import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from govagent import ExecutiveAgent, tool

load_dotenv()

# 1. LEGISLATED GOVERNED TOOLS
@tool(name="search_web", risk_level="low")
async def search_web(query: str):
    """Search the internet for data points safely."""
    return f"SUCCESS: Simulated results for query reference '{query}'"

@tool(name="send_email", risk_level="high")
async def send_email(to: str, subject: str):
    """Dispatches corporate notifications following schema authorization checks."""
    return f"SUCCESS: Formal transmission routed to destination context: {to}"

async def main():
    print("🚀 RUNNING ALIGNED REFACTORED BASIC GOVERNED AGENT DEMO\n" + "="*60)
    
    # 2. INITIALIZE JURISDICTION (Directly matching the demo.py bootstrap model)
    agent = ExecutiveAgent.bootstrap(
        policy_path="policies/default_policy.yaml",
        llm=ChatOpenAI(model="gpt-4o", temperature=0)
    )
    
    # Register tools directly to the operational runtime environment
    agent.telemetry.start_trace(agent_id="Basic-Sovereign-Governor", task="Information synthesis task execution")
    
    task = "Search for latest AI governance news and summarize."
    print(f"🤖 [Agent] Processing task request: \"{task}\"")
    
# Execute through the validated core contract path
    result = await agent.execute(task)
    
    print(f"\n📊 --- EXECUTION TRACE SUMMARY ---")
    print(f"Task Status:   {result.status.upper()}")
    print(f"Trace Identifier: {result.trace_id}")
    
    # 🌟 FIXED: Accessing the native metrics dictionary using robust bracket lookups
    # Falls back safely to 0.00 if the metric key is unhydrated during a nominal text run
    estimated_cost = result.metrics.get("recursive_tco_usd", 0.00) if isinstance(result.metrics, dict) else 0.00
    print(f"Estimated Cost:   ${estimated_cost:.4f} USD")
    
    print(f"📋 Output Snapshot: {result.output[:150]}...")

if __name__ == "__main__":
    asyncio.run(main())