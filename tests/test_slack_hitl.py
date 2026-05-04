import pytest
import asyncio
import os
from dotenv import load_dotenv 
from govagent.hitl.manager import HITLManager, ApprovalRequest
from govagent.hitl.slack_adapter import SlackJudiciaryAdapter

# Load environment variables from .env file
load_dotenv()

@pytest.mark.asyncio
async def test_slack_interaction():
    """
    Integration Test: Verifies the Slack Socket Mode handshake and 
    the synchronous blocking/resuming of the Judiciary layer.
    """
    
    # 1. Configuration Check
    bot_token = os.getenv("SLACK_BOT_TOKEN")
    app_token = os.getenv("SLACK_APP_TOKEN")
    channel_id = os.getenv("SLACK_CHANNEL_ID")

    if not all([bot_token, app_token, channel_id]):
        pytest.fail("❌ Environment Error: Ensure SLACK_BOT_TOKEN, SLACK_APP_TOKEN, and SLACK_CHANNEL_ID are set.")

    print(f"\n📡 Connecting to Slack Channel: {channel_id}...")

    # 2. Initialize the Adapter
    # This fulfills EU AI Act Article 14 (Human Oversight) requirements.
    adapter = SlackJudiciaryAdapter(
        bot_token=bot_token,
        app_token=app_token,
        channel_id=channel_id
    )
    
    # Start the Socket Mode listener
    # This establishes the persistent websocket connection.
    adapter.start()
    
    # 3. Initialize the Manager
    manager = HITLManager(adapter=adapter)
    
    print("🚀 Sending High-Risk Approval Request to your mobile...")

    # 4. The Blocking Call
    # This replicates the 'Chain of Accountability' pausing for a human signal.
    approved = await manager.secure_approval(
        agent_id="Compliance-Auditor-v1",
        reason="Authorization required for tool: 'authorize_payment' (High Risk).",
        context={
            "amount": "$5,000.00",
            "recipient": "Acme Infrastructure Corp",
            "policy_violation": "None - Requires manual sign-off per v0.1.7 SOP."
        }
    )

    # 5. Verification
    # If you click 'Approve' in Slack, this should be True.
    # If you click 'Reject', this should be False.
    print(f"\n⚖️  Judiciary Decision Received: {'APPROVED ✅' if approved else 'REJECTED ❌'}")
    
    assert isinstance(approved, bool), "The HITL response must be a boolean decision."

if __name__ == "__main__":
    # Standard entry point for manual execution outside of pytest
    asyncio.run(test_slack_interaction())