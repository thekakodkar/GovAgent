import pytest
import asyncio
import os
from dotenv import load_dotenv 
from govagent.hitl import HITLManager, SlackJudiciaryAdapter
from unittest.mock import AsyncMock

# Load environment variables
load_dotenv()


@pytest.mark.asyncio
async def test_federated_quorum_logic():
    """
    v0.5.0 Validation: Verifies M-of-N quorum without live Slack connectivity.
    """
    # 1. Initialize a Mock Adapter to bypass live auth
    mock_adapter = AsyncMock()
    mock_adapter.notify.return_value = True # Simulate board approval
    
    manager = HITLManager(adapter=mock_adapter)
    
    federated_config = {"min_approvals": 2, "quorum_size": 3}
    
    approved = await manager.secure_approval(
        agent_id="GovAgent-v0.5.0",
        reason="High-value disbursement ($1200.00)",
        triggered_by="judiciary",
        config=federated_config
    )

    assert approved is True
    assert mock_adapter.notify.called

@pytest.mark.asyncio
async def test_slack_interaction():
    """
    v0.3.0 Integration Test: Verifies the Slack Judiciary escalation path.
    Ensures that high-risk context is accurately rendered for the human reviewer.
    """
    
    # 1. Configuration Check
    bot_token = os.getenv("SLACK_BOT_TOKEN")
    app_token = os.getenv("SLACK_APP_TOKEN")
    channel_id = os.getenv("SLACK_CHANNEL_ID")

    if not all([bot_token, app_token, channel_id]):
        pytest.skip("⚠️ Skipping Slack integration test: Credentials missing from .env")

    # 2. Initialize the Adapter (The Article 14 Interface)
    adapter = SlackJudiciaryAdapter(
        bot_token=bot_token,
        app_token=app_token,
        channel_id=channel_id
    )
    
    try:
        # Start persistent Socket Mode connection
        adapter.start()
        
        # 3. Initialize the Manager
        manager = HITLManager(adapter=adapter)
        
        print(f"\n⚖️  ESCALATION TEST: Dispatching approval request to {channel_id}...")

        # 4. The Parameterized Blocking Call
        # v0.3.0 standard: Passing structured context for executive decision support
        approved = await manager.secure_approval(
            agent_id="GovAgent-v0.3.0-Scale",
            reason="Institutional sign-off required for high-value disbursement.",
            triggered_by="judiciary",
            context={
                "action": "authorize_disbursement",
                "params": {"amount": 1200.0, "currency": "USD"},
                "compliance_check": "EU-AI-ACT-ARTICLE-14"
            }
        )

        # 5. Verification of Decision
        decision_str = "APPROVED ✅" if approved else "REJECTED ❌"
        print(f"\n🏛️  Judiciary Response: {decision_str}")
        
        assert isinstance(approved, bool), "Judiciary must return a binary Boolean result."

    finally:
        # 6. Lifecycle Management: Cleanly stop the adapter to prevent hanging threads
        if hasattr(adapter, "stop"):
            adapter.stop()