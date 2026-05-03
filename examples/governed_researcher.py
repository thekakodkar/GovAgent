import os
import asyncio
from pathlib import Path
from govagent.agent import ExecutiveAgent
from govagent.policy import Policy
from govagent.telemetry import TelemetryManager

# Path resolution for cross-environment stability
base_path = Path(__file__).parent

# 1. Aligned Mock Model Client
class MockModel:
    async def generate_plan(self, task, persona):
        """
        v0.2.0 Refactor: Returning the explicit 3-value tuple.
        (Intent_Dict, Cost_Float, Tokens_Int)
        """
        intent = {
            "thought": "Analysis of 2026 shifts requires verified market data.",
            "action": "web_search",
            "params": {"query": "2026 AI market shifts", "domain": "verified-news.com"}
        }
        # Explicit telemetry data to satisfy the ExecutiveAgent unpacker
        cost = 0.0050 
        tokens = 120
        
        return intent, cost, tokens

async def main():
    # 2. Robust Policy Loading
    policy_path = base_path / "../policies/market_research_policy.yaml"
    
    if not policy_path.exists():
        print(f"❌ Error: Policy not found at {policy_path.resolve()}")
        return

    # Load the policy (Ensure your YAML contains 'restricted_domains')
    policy = Policy.from_yaml(policy_path.resolve())
    
    # 3. Initialize Telemetry and Agent
    telemetry = TelemetryManager()
    agent = ExecutiveAgent(
        persona="Strategic Analyst",
        policy=policy,
        model_client=MockModel(),
        telemetry=telemetry
    )

    print("🛡️ GovAgent: Market Research Instance Online.")
    print("--- Starting Governed Task ---")
    
    # 4. Execute Task
    # The ExecutiveAgent now correctly separates the 'web_search' intent 
    # from the financial cost of $0.0050.
    result = await agent.execute("Analyze upcoming 2026 AI market shifts.")

    # 5. Review the Executive Summary (Audit Log)
    print("\n--- Execution Summary ---")
    print(f"Status: {result.status}")
    # Using the standardized TelemetryManager attributes
   # Change result.total_cost_usd to result.estimated_cost_usd
    print(f"Final Cost: ${result.estimated_cost_usd:.4f}")
    print(f"Audit Trace ID: {result.trace_id}")

if __name__ == "__main__":
    asyncio.run(main())