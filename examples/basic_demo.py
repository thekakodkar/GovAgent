import asyncio
from dotenv import load_dotenv
from govagent import ExecutiveAgent, tool, Policy, PolicyBasedRouter, RouterConfig
from govagent.llm.ollama import OllamaClient
# from govagent.llm.openai import OpenAIClient  # Un-comment as client wrappers stabilize

load_dotenv()

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
    
    # 1. Parse policy first to extract infrastructure rules dynamically
    policy = Policy.from_yaml("policies/default_policy.yaml")
    
    # 2. Build the client registry mapping
    clients = {
        "local_ollama": OllamaClient(config={"base_url": "http://localhost:11434", "model": "llama3.2"})
    }
    
    # 3. Construct the router matching the active policy profile settings
    router_cfg = RouterConfig(
        routing_mode=getattr(policy, "routing_mode", "LOCAL_ONLY"),
        default_provider=getattr(policy, "default_provider", "local_ollama"),
        rules=getattr(policy, "routing_rules", [])
    )
    router = PolicyBasedRouter(clients=clients, config=router_cfg)
    
    # 4. Inject the Sovereign Router cleanly into the Agent instance
    agent = ExecutiveAgent(
        persona=policy.metadata.get("agent_name", "Basic-Sovereign-Governor"),
        policy=policy,
        router=router
    )
    
    agent.telemetry.start_trace(agent_id="Basic-Sovereign-Governor", task="Information synthesis task execution")
    
    task = "Search for latest AI governance news and summarize."
    print(f"🤖 [Agent] Processing task request: \"{task}\"")
    
    result = await agent.execute(task)
    
    print(f"\n📊 --- EXECUTION TRACE SUMMARY ---")
    print(f"Task Status:   {result.status.upper()}")
    print(f"Trace Identifier: {result.trace_id}")
    
    estimated_cost = result.metrics.get("recursive_tco_usd", 0.00) if isinstance(result.metrics, dict) else 0.00
    print(f"Estimated Cost:   ${estimated_cost:.4f} USD")
    print(f"📋 Output Snapshot: {str(result.output)[:150]}...")

if __name__ == "__main__":
    asyncio.run(main())