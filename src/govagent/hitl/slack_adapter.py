import asyncio
from slack_sdk.web import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest
from .manager import ApprovalRequest, ApprovalStatus

class SlackJudiciaryAdapter:
    """
    Institutional Multi-Signature Adapter (v0.5.0).
    Implements Federated M-of-N Consensus for Article 14 Compliance.
    """
    def __init__(self, bot_token: str, app_token: str, channel_id: str):
        self.channel_id = channel_id
        self.client = WebClient(token=bot_token)
        self.pending_requests = {} # Maps request_id -> (ApprovalRequest, asyncio.Future)
        self.socket_client = SocketModeClient(app_token=app_token, web_client=self.client)

    def start(self):
        """Establishes the persistent WebSocket connection."""
        print("🏛️ Judiciary Layer: Establishing Federated Socket Mode...")
        self.socket_client.socket_mode_request_listeners.append(self.handle_interaction)
        self.socket_client.connect()

    async def notify(self, request: ApprovalRequest) -> bool:
        """
        Orchestrates a Synchronous Voting Session.
        Pauses agent execution until institutional quorum is achieved.
        """
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        self.pending_requests[request.request_id] = (request, future)

        # Dispatch the initial 'Judiciary Ballot'
        blocks = self._generate_blocks(request)
        response = self.client.chat_postMessage(
            channel=self.channel_id, 
            blocks=blocks,
            text=f"⚖️ Federated Approval Required: {request.reason}" 
        )

        # Store the thread timestamp for real-time UI updates
        request.context["message_ts"] = response["ts"]

        try:
            return await future
        finally:
            if request.request_id in self.pending_requests:
                del self.pending_requests[request.request_id]

    def _generate_blocks(self, request: ApprovalRequest):
        """Generates Dynamic Block Kit UI reflecting current quorum status."""
        approvers_list = ", ".join([f"<@{u}>" for u in request.approvers]) or "_No signatures yet_"
        
        return [
            {"type": "header", "text": {"type": "plain_text", "text": "🛡️ GovAgent: Federated Judiciary"}},
            {"type": "section", "text": {"type": "mrkdwn", "text": f"*Agent:* `{request.agent_id}`\n*Reason:* {request.reason}"}},
            {"type": "section", "text": {"type": "mrkdwn", "text": f"*Required Quorum:* `{len(request.approvers)} / {request.min_approvals}`"}},
            {"type": "section", "text": {"type": "mrkdwn", "text": f"*Authorized By:* {approvers_list}"}},
            {"type": "divider"},
            {"type": "actions", "elements": [
                {"type": "button", "text": {"type": "plain_text", "text": "Approve ✅"}, "style": "primary", "action_id": "approve", "value": request.request_id},
                {"type": "button", "text": {"type": "plain_text", "text": "Terminate ❌"}, "style": "danger", "action_id": "reject", "value": request.request_id}
            ]}
        ]

    def handle_interaction(self, client: SocketModeClient, req: SocketModeRequest):
        """Processes multi-signature logic across the distributed board."""
        if req.type != "interactive": return
        
        payload = req.payload
        action = payload["actions"][0]["action_id"]
        request_id = payload["actions"][0]["value"]
        user_id = payload["user"]["id"]

        # Acknowledge the interaction to prevent Slack timeouts
        client.send_socket_mode_response(SocketModeResponse(envelope_id=req.envelope_id))

        if request_id in self.pending_requests:
            request, future = self.pending_requests[request_id]

            if action == "approve":
                request.approvers.add(user_id) # Log the signature
                
                if len(request.approvers) >= request.min_approvals:
                    # M-of-N Met: Finalize Execution
                    self._resolve_final(request, future, True, f"✅ QUORUM MET: Approved by {len(request.approvers)} Directors.")
                else:
                    # Update Ballot UI for remaining voters
                    self.client.chat_update(
                        channel=self.channel_id,
                        ts=request.context["message_ts"],
                        blocks=self._generate_blocks(request),
                        text="Voting in progress..."
                    )

            elif action == "reject":
                # Sovereign Veto: Single rejection terminates the swarm
                self._resolve_final(request, future, False, f"❌ VETOED: Action terminated by <@{user_id}>.")

    def _resolve_final(self, request, future, decision, status_msg):
        """Closes the voting session and updates the forensic record."""
        loop = future.get_loop()
        loop.call_soon_threadsafe(future.set_result, decision)

        self.client.chat_update(
            channel=self.channel_id,
            ts=request.context["message_ts"],
            blocks=[{"type": "section", "text": {"type": "mrkdwn", "text": f"⚖️ *Final Decision:* {status_msg}"}}],
            text="Voting Closed."
        )