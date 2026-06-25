import asyncio
from dotenv import load_dotenv
from govagent import ExecutiveAgent, tool, Policy, PolicyBasedRouter, RouterConfig
from govagent.llm.ollama import OllamaClient
from govagent.context import get_shared_fiscal_metrics, update_shared_spend

load_dotenv()

@tool(name="analyze_report", risk_level="low")
async def analyze_report(report_id: str):
    """Executes granular structural analysis on localized corporate financial ledgers."""
    # Simulate an automatic micro-spend accumulation per file item processed
    update_shared_spend(5.00) 
    return f"SUCCESS: Data evaluation completed for target resource target register {report_id}."

async def main():
    print("💰 RUNNING ALIGNED COST CONTROL + FISCAL GUARD DEMO\n" + "="*60)
    
    # 1. Parse the policy profile upfront to check compliance infrastructure mappings
    policy_path = "policies/cost_control_policy.yaml"
    policy = Policy.from_yaml(policy_path)
    
    # 2. Instantiate your active client pool registry
    clients = {
        "local_ollama": OllamaClient(config={"base_url": "http://localhost:11434", "model": "llama3.2"})
    }
    
    # 3. Compile the Router configuration from the parsed policy variables
    router_cfg = RouterConfig(
        routing_mode=getattr(policy, "routing_mode", "LOCAL_ONLY"),
        default_provider=getattr(policy, "default_provider", "local_ollama"),
        rules=getattr(policy, "routing_rules", [])
    )
    router = PolicyBasedRouter(clients=clients, config=router_cfg)
    
    # 4. Corrected Factory Call: Injecting the Sovereign Router client instance
    agent = ExecutiveAgent.bootstrap(
        policy_path=policy_path,
        router_client=router
    )
    
    task = "Analyze 50 quarterly financial reports and give summary."
    print(f"🤖 [Cost-Agent] Initializing recursive sweep loop payload...")
    
    # Ingest the batch instruction
    result = await agent.execute(task)
    
    # Extrapolate post-execution forensic calculations
    metrics = get_shared_fiscal_metrics()
    
    print(f"\n📊 --- FISCAL MONITOR SEGMENT ---")
    print(f"Final Status:          {result.status.upper()}")
    print(f"Aggregate Swarm Footprint: ${metrics['cumulative_spend']:.2f} USD")
    
    if result.status.upper() == "BLOCKED":
        print(f"⚠️ Circuit Breaker Status: ACTIVE 🛑 Policy ceiling limit breached.")
        if hasattr(result, 'block_reason'):
            print(f"❌ Rejection Matrix Reason:  {result.block_reason}")
    else:
        print("🟢 Circuit Breaker Status: NOMINAL within enterprise budget boundaries.")

if __name__ == "__main__":
    asyncio.run(main())