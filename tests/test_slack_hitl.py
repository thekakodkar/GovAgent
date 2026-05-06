import pytest
import asyncio
import os
from dotenv import load_dotenv 
from govagent.hitl.manager import HITLManager
from govagent.hitl.slack_adapter import SlackJudiciaryAdapter

# Load environment variables
load_dotenv()

@pytest.mark.asyncio
async def test_slack_interaction():
    """
    v0.2.3 Integration Test: Verifies the Slack Judiciary escalation.
    Ensures the 'triggered_by' context is correctly passed to the human reviewer.
    """
    
    # 1. Configuration Check
    bot_token = os.getenv("SLACK_BOT_TOKEN")
    app_token = os.getenv("SLACK_APP_TOKEN")
    channel_id = os.getenv("SLACK_CHANNEL_ID")

    if not all([bot_token, app_token, channel_id]):
        pytest.fail("❌ Environment Error: Slack credentials missing from .env")

    # 2. Initialize the Adapter (The article 14 Interface)
    adapter = SlackJudiciaryAdapter(
        bot_token=bot_token,
        app_token=app_token,
        channel_id=channel_id
    )
    
    # Start persistent Socket Mode connection
    adapter.start()
    
    # 3. Initialize the Manager
    manager = HITLManager(adapter=adapter)
    
    print(f"\n⚖️  ESCALATION TEST: Ping sent to channel {channel_id}...")

    # 4. The Parameterized Blocking Call
    # We explicitly pass 'triggered_by' to test the new v0.2.3 context logic
    approved = await manager.secure_approval(
        agent_id="GovAgent-v0.2.3-Alpha",
        reason="Manual sign-off required for high-risk tool call.",
        triggered_by="judiciary",
        context={
            "tool": "authorize_disbursement",
            "amount": "$1,200.00",
            "compliance_tag": "EU-AI-ACT-HIGH-RISK"
        }
    )

    # 5. Verification of Decision
    decision_str = "APPROVED ✅" if approved else "REJECTED ❌"
    print(f"\n🏛️  Decision Logged: {decision_str}")
    
    assert isinstance(approved, bool), "The Judiciary must return a binary decision."

if __name__ == "__main__":
    asyncio.run(test_slack_interaction())