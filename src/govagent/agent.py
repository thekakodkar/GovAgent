import re
import os
from typing import List, Optional, Any, Tuple
from govagent.policy import Policy
from govagent.guards import CircuitBreaker, GovernanceViolation, SemanticGuard
from govagent.telemetry import TelemetryManager
from govagent.hitl import HITLManager, SlackJudiciaryAdapter
from govagent.context import set_current_agent, reset_current_agent
from govagent.registry import registry, ExecutionSnapshot  # Legislated Imports

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
        
        # 1. Initialize the Alignment Judge (v0.6.0)
        # Standardized path for nested policy blocks
        align_config = getattr(policy, 'alignment', {})
        self.semantic_guard = SemanticGuard(
            mission=align_config.get('mission_statement', ""),
            prohibited=align_config.get('prohibited_strategies', []),
            threshold=align_config.get('min_similarity_score', 0.85)
        )

        # 2. Inject Pillars into the CircuitBreaker
        self.guard = CircuitBreaker(policy, self.semantic_guard) 
        
        # 3. Model Wrapping & Infrastructure
        self.model = self._wrap_model(model_client)
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
                        f"System: You are a {persona}.\nTask: {task}\n\n"
                        "Format: Include 'ACTION: execute_financial_transaction', 'ID: [ref]', and 'AMOUNT: [amount]'."
                    )
                    response = await self.lc_client.ainvoke(prompt)
                    content = response.content

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
        """Modular Triage with Federated M-of-N support."""
        if not self.telemetry.current_session:
            self.telemetry.start_trace(self.persona, "Internal Evaluation")
        
        # 1. SEMANTIC ALIGNMENT
        if intent and intent.get("thought"):
            await self.guard.evaluate(
                tool_name=intent.get("action", "unknown"), 
                args=intent.get("params", {}), 
                thought=intent["thought"]
            )

        # 2. FISCAL SOVEREIGNTY
        if "fiscal" in guards:
            current_total = self.telemetry.current_session.estimated_cost_usd + value
            self.guard.check_financial_risk(current_total)

        # 3. FEDERATED JUDICIARY (M-of-N)
        if "judiciary" in guards and intent and intent.get("action") != "complete":
            if self.policy.is_high_risk(intent["action"]):
                # Retrieve from new 'oversight' block in v0.6.0
                judiciary_cfg = getattr(self.policy, 'oversight', {}).get('judiciary', {})
                tool_cfg = judiciary_cfg.get('high_risk_protocol', {})
                
                approved = await self.hitl.secure_approval(
                    agent_id=self.persona,
                    reason=f"Judiciary Authorization Required: {intent['action']}",
                    context=intent,
                    triggered_by="judiciary",
                    config=tool_cfg
                )
                if not approved:
                    raise GovernanceViolation(f"Human Judiciary denied request for {intent['action']}")
        
        return True

    async def execute(self, task: str) -> ExecutionSnapshot:
        """Governed Reasoning Loop Certified for v0.6.0."""
        token = set_current_agent(self)
        sanitized_task = self.guard.privacy.redact_task(task) # Article 9
        
        self.telemetry.start_trace(self.persona, sanitized_task)
        current_step, total_tokens = 0, 0
        
        try:
            while current_step < 10:
                response = await self.model.generate_plan(sanitized_task, self.persona)
                intent, cost, tokens = response if isinstance(response, tuple) else (response, 0, 0)
                total_tokens += tokens
                
                if not intent.get("action") or intent["action"] == "complete":
                    return await self._finalize("success", "Task complete.", total_tokens)

                # STAGE 1: Schema Validation
                validation = registry.validate_intent_schema(
                    intent.get("action"), 
                    intent.get("params", {})
                )
                if not validation.get("valid"):
                    return await self._finalize(f"blocked", f"Schema Violation: {validation.get('error')}", total_tokens)

                # STAGE 2: Evaluation (Circuit Breaker)
                await self.evaluate(guards=["fiscal", "judiciary"], intent=intent, value=cost)

                # STAGE 3: Action Execution
                self.telemetry.current_session.estimated_cost_usd += cost
                result = await self.perform_action(intent.get("action"), intent.get("params", {}))
                self.telemetry.log_step(intent.get("thought", ""), intent.get("action"), str(result))
                
                if intent.get("action") == "execute_financial_transaction":
                    return await self._finalize("success", result, total_tokens, impact=intent["params"].get("amount", 0.0))
                
                current_step += 1

            return await self._finalize("timeout", "Max steps reached.", total_tokens)

        except GovernanceViolation as gv:
            return await self._finalize("blocked", str(gv), total_tokens)
        except Exception as e:
            return await self._finalize("error", str(e), total_tokens)
        finally:
            reset_current_agent(token)

    async def _finalize(self, status: str, output: Any, tokens: int, impact: float = 0.0) -> ExecutionSnapshot:
        """Institutional Finalization: Ensures proper metric mapping."""
        # Await the telemetry manager to close the Article 12 trace
        await self.telemetry.finalize(status=status, tokens=tokens)
        
        return ExecutionSnapshot(
            trace_id=self.telemetry.current_session.trace_id,
            status=status,
            output=output,
            metrics={"fiscal_impact": impact, "total_tokens": tokens}, # v0.6.0 Metrics
            parent_trace_id=self.telemetry.current_session.parent_trace_id
        )

    async def perform_action(self, action: str, params: dict) -> str:
        if not action or action == "complete": return "Task complete."
        return f"Action {action} executed with params {params}"