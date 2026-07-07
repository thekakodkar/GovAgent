# tests/test_slack_hitl.py
import pytest
import asyncio
import os
from dotenv import load_dotenv 
from govagent.hitl.manager import HITLManager
from govagent.hitl.slack_adapter import SlackJudiciaryAdapter
from unittest.mock import AsyncMock

load_dotenv()

@pytest.mark.asyncio
async def test_federated_quorum_logic():
    """
    v0.6.0 Validation: Verifies M-of-N role-based weighted quorum without live Slack connectivity.
    """
    mock_adapter = AsyncMock()
    
    # Simulate a Director (+2.0) and a Lead (+1.0) signing off = 3.0 aggregate score
    mock_adapter.notify.return_value = [
        {"voter_id": "U111", "voter_role": "Director", "decision": "APPROVED"},
        {"voter_id": "U222", "voter_role": "Lead", "decision": "APPROVED"}
    ]
    
    manager = HITLManager(adapter=mock_adapter)
    
    # Context payload simulating a mid-tier financial transaction ($1500 maps to Tier 2: 2.5 Target Score)
    context_payload = {"params": {"amount": 1500.0}}
    
    # Aligned parameter signature matching manager.py contract
    approved = await manager.secure_approval(
        agent_id="GovAgent-v3.0.0-Alpha",
        reason="High-value disbursement ($1500.00)",
        triggered_by="judiciary",
        context=context_payload,
        config={}
    )

    assert approved is True
    assert mock_adapter.notify.called

@pytest.mark.asyncio
async def test_slack_interaction():
    """
    v3.0.0 Integration Test: Verifies the Slack Judiciary interactive escalation path.
    """
    bot_token = os.getenv("SLACK_BOT_TOKEN")
    app_token = os.getenv("SLACK_APP_TOKEN")
    channel_id = os.getenv("SLACK_CHANNEL_ID")

    if not all([bot_token, app_token, channel_id]):
        pytest.skip("⚠️ Skipping Slack integration test: Credentials missing from .env")

    adapter = SlackJudiciaryAdapter(
        bot_token=bot_token,
        app_token=app_token,
        channel_id=channel_id
    )
    
    try:
        adapter.start()
        manager = HITLManager(adapter=adapter)
        
        print(f"\n⚖️ ESCALATION TEST: Dispatching weighted approval request to {channel_id}...")

        # Request exceeds $5000.00, triggering TIER_3_CRITICAL (4.0 target weight score required)
        approved = await manager.secure_approval(
            agent_id="GovAgent-v3.0.0-Live",
            reason="Institutional sign-off required for critical infrastructure budget allocation.",
            triggered_by="judiciary",
            context={
                "params": {"amount": 5500.0, "currency": "USD"},
                "compliance_check": "EU-AI-ACT-ARTICLE-14"
            },
            config={}
        )

        decision_str = "APPROVED ✅" if approved else "REJECTED ❌"
        print(f"\n🏛️ Judiciary Response: {decision_str}")
        
        assert isinstance(approved, bool)

    finally:
        if hasattr(adapter, "stop"):
            adapter.stop()