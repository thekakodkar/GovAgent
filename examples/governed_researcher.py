import asyncio
from govagent.agent import ExecutiveAgent
from govagent.policy import Policy
from govagent.telemetry import TelemetryManager

# Mock Model Client for demonstration (No API key needed)
class MockModel:
    async def generate_plan(self, task, persona):
        # Simulating a thought process and an action
        return (
            "I need to search for Q4 trends but the cost is rising.",
            "web_search",
            {"query": "2026 tech trends", "source": "verified-news.com"}
        )

async def main():
    # 1. Load the Governance Policy
    policy = Policy.from_yaml("examples/policy.yaml")
    
    # 2. Initialize Telemetry and Agent
    telemetry = TelemetryManager()
    agent = ExecutiveAgent(
        persona="Strategic Analyst",
        policy=policy,
        model_client=MockModel(),
        telemetry=telemetry
    )

    print("--- Starting Governed Task ---")
    
    # 3. Execute Task
    # This will trigger the Think -> Guard -> Act cycle
    result = await agent.execute("Analyze upcoming 2026 AI market shifts.")

    # 4. Review the Executive Summary
    print("\n--- Execution Summary ---")
    print(f"Status: {result.status}")
    print(f"Final Cost: ${result.estimated_cost_usd:.4f}")
    print(f"Human Labor Saved: {result.human_minutes_saved} minutes")
    print(f"Audit ID: {result.trace_id}")

if __name__ == "__main__":
    asyncio.run(main())