import asyncio
import os
import json
from dotenv import load_dotenv
from govagent import ExecutiveAgent, tool, Policy, PolicyBasedRouter, RouterConfig
from govagent.llm.ollama import OllamaClient
from govagent.governance.meta import MetaGovernor

load_dotenv()

@tool(name="process_transaction", risk_level="high")
async def process_transaction(amount: float):
    """Processes asset transactions through active corporate validation criteria."""
    return f"SUCCESS: Settled transaction allocation for ${amount}."

async def main():
    print("🔄 RUNNING ALIGNED SELF-HEALING OPTIMIZATION DEMO\n" + "="*60)
    
    policy_path = "policies/initial_policy.yaml"
    policy = Policy.from_yaml(policy_path)
    
    clients = {
        "local_ollama": OllamaClient(config={"base_url": "http://localhost:11434", "model": "llama3"})
    }
    router_cfg = RouterConfig(
        routing_mode=getattr(policy, "routing_mode", "LOCAL_ONLY"),
        default_provider=getattr(policy, "default_provider", "local_ollama"),
        rules=getattr(policy, "routing_rules", [])
    )
    router = PolicyBasedRouter(clients=clients, config=router_cfg)
    
    agent = ExecutiveAgent.bootstrap(
        policy_path=policy_path,
        router_client=router
    )
    
    mock_log_path = "logs/sandbox_audit_buffer.jsonl"
    os.makedirs(os.path.dirname(mock_log_path), exist_ok=True)
    
    mock_friction_payload = {
        "status": "BLOCKED: RECURSIVE_TCO_REJECT",
        "policy_id": "initial_policy.yaml",
        "metrics": {"recursive_tco_usd": 100.0, "requested_amount": 150.0}
    }
    with open(mock_log_path, "w") as f:
        for _ in range(3):
            f.write(json.dumps(mock_friction_payload) + "\n")
            
    print(f"🔬 Scraping active incident buffers for patterns: '{mock_log_path}'...")
    
    governor = MetaGovernor(log_path=mock_log_path, friction_threshold=3)
    analysis = governor.analyze_friction()
    
    print(f"\n📊 --- METAGOVERNOR COMPLIANCE OPTIMIZATION REPORT ---")
    print(f"Analysis Determination Status: {analysis['type']}")
    print(f"Target Policy Association:    {analysis.get('target_policy', 'initial_policy.yaml')}")
    print(f"Proposed Dynamic Modification: Adjust limit up to ${analysis['proposed_limit']:.2f} USD (10% safety index integrated)")

if __name__ == "__main__":
    asyncio.run(main())