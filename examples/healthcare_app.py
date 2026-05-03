import os
from pathlib import Path
import asyncio
from govagent.agent import ExecutiveAgent
from govagent.policy import Policy
from govagent.registry import tool, registry
from govagent.hitl import HITLManager

# Get the directory where the script is located
base_path = Path(__file__).parent

# 1. Define Business-Specific Governed Tools
@tool(name="authorize_claim_payment", risk_level="high", category="financial")
async def authorize_claim_payment(claim_id: str, amount: float):
    """Business logic for disbursement."""
    return {"status": "disbursed", "amount": amount}

async def run_healthcare_agent():
    # 1. Resolve the absolute path to the policy file
    # This ensures the script runs regardless of which directory you start it from
    policy_path = base_path / "../policies/healthcare_ops_policy.yaml"
    
    # 2. Initialize the Governance Layer
    # We use .resolve() to handle the '../' notation correctly across OS platforms
    if not policy_path.exists():
        raise FileNotFoundError(f"Critical Error: Policy file not found at {policy_path.resolve()}")
        
    policy = Policy.from_yaml(policy_path.resolve())
    
    # 3. Synchronize Registry with Policy (The v0.2.0 Audit)
    policy.validate_registry()

    # 4. Bootstrap the Executive and Judiciary
    hitl = HITLManager()
    agent = ExecutiveAgent(
        persona="Healthcare Billing Director",
        policy=policy,
        model_client=None, # Ensure you inject your LLM client here for execution
        hitl_manager=hitl
    )

    print("🛡️ GovAgent: Healthcare Instance Online & Audited.")
    
if __name__ == "__main__":
    asyncio.run(run_healthcare_agent())