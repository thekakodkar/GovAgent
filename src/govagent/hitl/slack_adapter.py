import asyncio
from slack_sdk.web import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest
from .manager import ApprovalRequest

class SlackJudiciaryAdapter:
    """
    Enterprise Slack Adapter for mobile-first human oversight.
    Implements Article 14 (Human Oversight) for EU AI Act compliance.
    """
    def __init__(self, bot_token: str, app_token: str, channel_id: str):
        self.channel_id = channel_id
        self.client = WebClient(token=bot_token)
        
        # Map to track pending requests and their corresponding asyncio Futures
        self.pending_requests = {} 
        
        # Initialize the Socket Mode client
        self.socket_client = SocketModeClient(
            app_token=app_token,
            web_client=self.client
        )

    def start(self):
        """Establishes the persistent WebSocket connection and registers listeners."""
        print("🏛️ Judiciary Layer: Establishing Socket Mode connection...")
        self.socket_client.socket_mode_request_listeners.append(self.handle_interaction)
        self.socket_client.connect()

    async def notify(self, request: ApprovalRequest) -> bool:
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        self.pending_requests[request.request_id] = future

        blocks = self._generate_blocks(request)
        
        # Simplified dispatch: Assumes manual invitation to the 'Courtroom' channel
        self.client.chat_postMessage(
            channel=self.channel_id, 
            blocks=blocks,
            text=f"🔴 GovAgent Intervention Required: {request.reason}" 
        )

        try:
            return await future
        finally:
            if request.request_id in self.pending_requests:
                del self.pending_requests[request.request_id]
                
    def _generate_blocks(self, request: ApprovalRequest):
        """Generates the Block Kit UI for the Slack notification."""
        return [
            {"type": "header", "text": {"type": "plain_text", "text": "🛡️ GovAgent: Intervention Required"}},
            {"type": "section", "text": {"type": "mrkdwn", "text": f"*Agent:* `{request.agent_id}`\n*Reason:* {request.reason}"}},
            {"type": "section", "text": {"type": "mrkdwn", "text": f"*Context:* \n```\n{request.context}\n```"}},
            {"type": "actions", "elements": [
                {"type": "button", "text": {"type": "plain_text", "text": "Approve ✅"}, "style": "primary", "action_id": "approve", "value": request.request_id},
                {"type": "button", "text": {"type": "plain_text", "text": "Reject ❌"}, "style": "danger", "action_id": "reject", "value": request.request_id}
            ]}
        ]

    def handle_interaction(self, client: SocketModeClient, req: SocketModeRequest):
        """Processes the button click event from the Slack WebSocket."""
        if req.type == "interactive":
            payload = req.payload
            action = payload["actions"][0]["action_id"]
            request_id = payload["actions"][0]["value"]

            # Standard Socket Mode acknowledgment
            client.send_socket_mode_response(SocketModeResponse(envelope_id=req.envelope_id))

            if request_id in self.pending_requests:
                decision = (action == "approve")
                
                # Resolve the future safely across threads
                loop = self.pending_requests[request_id].get_loop()
                loop.call_soon_threadsafe(self.pending_requests[request_id].set_result, decision)
                
                # Update Slack UI for audit traceability
                self.client.chat_update(
                    channel=payload["container"]["channel_id"],
                    ts=payload["container"]["message_ts"],
                    text=f"⚖️ *Decision:* {'APPROVED ✅' if decision else 'REJECTED ❌'} by <@{payload['user']['id']}>"
                )