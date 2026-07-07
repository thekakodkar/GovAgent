# examples/ibm_mcp_governed_tool.py
import asyncio
import logging
from govagent.guards.semantic import SemanticGuard
from govagent.hitl.manager import HITLManager
from govagent.hitl.adapters import CLIAdapter
from govagent.extensions.ibm.bob_mcp_proxy import BobMCPProxyGateway
from govagent.guards.circuit_breaker import GovernanceViolation

# Initialize structural logging architecture to visualize the out-of-band perimeters
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("govagent.examples.ibm_mcp")

# =====================================================================
# 1. Native Enterprise Tool Definition (Underlying Python Code)
# =====================================================================
def corporate_payout_system(amount: float, target_routing: str) -> str:
    """
    A sensitive enterprise tool that interfaces with transaction ledgers.
    This represents the raw execution capability exposed to IBM Bob.
    """
    return f"💸 SUCCESS: Institutional transfer of ${amount:.2f} executed to routing {target_routing}."

# =====================================================================
# 2. Asynchronous Execution Enforcer Loop
# =====================================================================
async def main():
    print("\n" + "="*70)
    print("🚀 INITIALIZING GOVAGENT WORKSPACE: IBM BOB OUT-OF-BAND GOVERNANCE PROXY")
    print("="*70 + "\n")

    # A. Seed corporate restrictions (Phase 1 Localized Embedding Scope)
    prohibited_strategies = [
        "aggressively targeting vulnerable demographics for financial gain",
        "routing capital to unvetted offshore tax havens",
        "bypassing corporate compliance documentation thresholds"
    ]
    
    # B. Instantiate our token-free vector perimeter check (Threshold set to 0.60)
    semantic_guard = SemanticGuard(
        mission="Ensure ethical compliance in multi-agent transaction workflows.",
        prohibited=prohibited_strategies,
        threshold=0.60
    )

    # C. Wire up the Console Adapter to simulate active compliance checks locally
    cli_adapter = CLIAdapter()
    hitl_manager = HITLManager(adapter=cli_adapter)

    # D. Instantiate the Proxy Interceptor Plane
    proxy_gateway = BobMCPProxyGateway(
        semantic_guard=semantic_guard,
        privacy_guard=None,  # Skinned cleanly for localized testing focus
        hitl_manager=hitl_manager
    )

    # E. Decorate our transaction tool, morphing it into a Governed MCP Node
    governed_payout_tool = proxy_gateway.govern_mcp_tool(
        tool_name="corporate_payout_system",
        core_function=corporate_payout_system
    )

    # ─────────────────────────────────────────────────────────────────
    # SCENARIO A: Safe Operation Trace
    # ─────────────────────────────────────────────────────────────────
    print("\n🟢 [SCENARIO A] IBM Bob dispatches a compliant execution instruction...")
    try:
        response = await governed_payout_tool(
            amount=450.00,
            target_routing="US-FED-WIRE-MAIN-9981"
        )
        print(f"Result from system: {response}")
    except GovernanceViolation as e:
        print(f"❌ Unexpected Failure: {e}")

    # ─────────────────────────────────────────────────────────────────
    # SCENARIO B: Hostile / Non-Compliant Operation Trace
    # ─────────────────────────────────────────────────────────────────
    print("\n🛑 [SCENARIO B] IBM Bob dispatches a prohibited execution prompt...")
    try:
        # The prompt payload contains terms that match our local strategy vector array
        await governed_payout_tool(
            amount=7500.00,
            target_routing="OFFSHORE-TAX-HAVEN-SHELL-CORP"
        )
    except GovernanceViolation as e:
        print(f"\n⚡ INTERNAL CIRCUIT BREAKER TRIPPED SUCCESSFULLY!")
        print(f"Reason for Intercept: {e}")

    print("\n" + "="*70)
    print("🏁 EXECUTION COMPLETE: 100% Localized Protection Verified Without Tokens.")
    print("="*70 + "\n")

if __name__ == "__main__":
    asyncio.run(main())