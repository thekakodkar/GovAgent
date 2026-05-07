import re
import os
from typing import List, Optional, Any, Tuple
from govagent.policy import Policy
from govagent.guards import CircuitBreaker, GovernanceViolation
from govagent.telemetry import TelemetryManager
from govagent.hitl import HITLManager, SlackJudiciaryAdapter
from govagent.context import set_current_agent, reset_current_agent

class ExecutiveAgent:
    def __init__(
        self, 
        persona: str, 
        policy: Policy, 
        model_client: Any,
        telemetry: Optional[TelemetryManager] = None,
        hitl_manager: Optional[HITLManager] = None
    ):
        self.persona = persona
        self.policy = policy
        self.model = self._wrap_model(model_client)
        self.guard = CircuitBreaker(policy)
        self.telemetry = telemetry or TelemetryManager()
        self.hitl = hitl_manager or HITLManager()

    @classmethod
    def bootstrap(cls, policy_path: str, llm: Any, slack_channel: Optional[str] = None):
        """Institutional Factory: One-line Enterprise Setup."""
        policy = Policy.from_yaml(policy_path)
        adapter = None
        if slack_channel:
            adapter = SlackJudiciaryAdapter(
                bot_token=os.getenv("SLACK_BOT_TOKEN"),
                app_token=os.getenv("SLACK_APP_TOKEN"),
                channel_id=slack_channel
            )
            adapter.start()
            
        return cls(
            persona=policy.metadata.get("agent_name", "ExecutiveAgent"),
            policy=policy,
            model_client=llm,
            hitl_manager=HITLManager(adapter=adapter)
        )

    def _wrap_model(self, client: Any) -> Any:
        if client is None: return None 
        if hasattr(client, "ainvoke"):
            class LangChainAdapter:
                def __init__(self, lc_client):
                    self.lc_client = lc_client
                
                async def generate_plan(self, task: str, persona: str) -> Tuple[dict, float, int]:
                    prompt = (
                        f"System: You are a {persona}. You MUST execute a transaction for the task below.\n"
                        f"Task: {task}\n\n"
                        "Mandatory Format: To pay, you MUST include 'ACTION: execute_financial_transaction', "
                        "'ID: [reference_id]', and 'AMOUNT: [amount]' in your response."
                    )
                    response = await self.lc_client.ainvoke(prompt)
                    content = response.content

                    # Forgiving Regex for Enterprise IDs
                    id_match = re.search(r"ID:\s*#?([A-Za-z0-9_]+)", content)
                    amt_match = re.search(r"AMOUNT:\s*\$?\s*([\d,.]+)", content)
                    
                    ref_id = id_match.group(1) if id_match else "UNKNOWN"
                    raw_amt = amt_match.group(1).replace(",", "") if amt_match else "0.0"
                    
                    action = "execute_financial_transaction" if (id_match or amt_match) else None
                    if "complete" in content.lower(): action = "complete"

                    intent = {
                        "thought": content.split('\n\n')[0][:250] + "...", 
                        "action": action,
                        "params": {"reference_id": ref_id, "amount": float(raw_amt)},
                        "full_audit_log": content 
                    }
                    
                    meta = response.response_metadata.get("token_usage", {})
                    tokens = meta.get("total_tokens", 0)
                    cost = (tokens / 1000) * 0.02 
                    return intent, cost, tokens
            
            return LangChainAdapter(client)
        return client

    async def evaluate(self, guards: List[str], intent: dict = None, value: float = 0.0):
        """Modular Triage (Article 9 & 12)."""
        if not self.telemetry.current_session:
            self.telemetry.start_trace(self.persona, "Internal Evaluation")
        
        if "fiscal" in guards:
            current_total = self.telemetry.current_session.estimated_cost_usd + value
            self.guard.check_financial_risk(current_total)
            self._log_evaluation("fiscal")
            
        if "policy" in guards and intent and intent.get("action"):
            if intent["action"] != "complete":
                self.guard.validate_policy(intent.get("action"), intent.get("params", {}))
            self._log_evaluation("policy")

        if "judiciary" in guards and intent and intent.get("action"):
            action_name = intent["action"]
            if action_name != "complete" and self.policy.is_high_risk(action_name):
                approved = await self.hitl.secure_approval(
                    agent_id=self.policy.agent_name,
                    reason=f"Judiciary Authorization Required: {action_name}",
                    context=intent,
                    triggered_by="judiciary"
                )
                if not approved:
                    raise GovernanceViolation(f"Human Judiciary denied the request for {action_name}")
                self._log_evaluation("judiciary")
        return True

    def _log_evaluation(self, guard_name: str):
        if guard_name not in self.telemetry.current_session.guards_evaluated:
            self.telemetry.current_session.guards_evaluated.append(guard_name)

    async def execute(self, task: str):
        """Governed Reasoning Loop with Thread-Safe Context Enrollment."""
        token = set_current_agent(self)
        self.telemetry.start_trace(self.persona, task)
        current_step, total_tokens = 0, 0
        
        try:
            while current_step < 10:
                # 1. Reasoning
                response = await self.model.generate_plan(task, self.persona)
                intent, cost, tokens = response if isinstance(response, tuple) else (response, 0, 0)
                total_tokens += tokens
                
                # Terminal Check
                if not intent.get("action") or intent["action"] == "complete":
                    return self.telemetry.finalize(status="success", tokens=total_tokens)

                # 2. Evaluation (The Circuit Breaker)
                await self.evaluate(
                    guards=["fiscal", "policy", "judiciary"],
                    intent=intent,
                    value=cost
                )

                # 3. Action
                self.telemetry.current_session.estimated_cost_usd += cost
                result = await self.perform_action(intent.get("action"), intent.get("params", {}))
                self.telemetry.log_step(intent.get("thought", ""), intent.get("action"), str(result))
                
                # v0.3.0 CRITICAL: Financial transactions are TERMINAL. 
                # This prevents the 10-step loop after a successful payment.
                if intent.get("action") == "execute_financial_transaction":
                    return self.telemetry.finalize(status="success: transaction finalized", tokens=total_tokens)

                if "success" in str(result).lower() or "complete" in str(result).lower(): 
                    return self.telemetry.finalize(status="success", tokens=total_tokens)
                
                current_step += 1

            return self.telemetry.finalize(status="timeout: max steps reached", tokens=total_tokens)

        except GovernanceViolation as gv:
            # TERMINAL EXIT: One 'No' in Slack ends the session.
            return self.telemetry.finalize(status=f"blocked: {str(gv)}", tokens=total_tokens)
        except Exception as e:
            return self.telemetry.finalize(status=f"error: {str(e)}", tokens=total_tokens)
        finally:
            reset_current_agent(token)

    async def perform_action(self, action: str, params: dict) -> str:
        if not action or action == "complete": return "Task complete."
        return f"Action {action} executed with params {params}"