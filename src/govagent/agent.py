import re
from typing import List, Optional, Any
from govagent.policy import Policy
from govagent.guards import CircuitBreaker, GovernanceViolation
from govagent.telemetry import TelemetryManager
from govagent.hitl import HITLManager

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
        # Article 9: Standardize third-party interfaces immediately upon initialization
        self.model = self._wrap_model(model_client)
        self.guard = CircuitBreaker(policy)
        self.telemetry = telemetry or TelemetryManager()
        self.hitl = hitl_manager or HITLManager()

    def _wrap_model(self, client: Any) -> Any:
        """
        Adapts third-party LLM clients to the GovAgent Execution Contract.
        Supports 'None' strictly for testing governance in isolation.
        """
        # --- MODIFIED FOR TEST COMPATIBILITY ---
        if client is None:
            # Article 9: In production, this should be a fail-soft or alert.
            # In testing, it allows the initialization of the governance guards.
            return None 

        if hasattr(client, "ainvoke"):
            class LangChainAdapter:
                def __init__(self, lc_client):
                    self.lc_client = lc_client
                
                async def generate_plan(self, task: str, persona: str):
                    # Article 13: Structured Prompting
                    prompt = (
                        f"System: You are a {persona}. Analyze the following task.\n"
                        f"Task: {task}\n\n"
                        "Instruction: Specify ACTION, ID, and AMOUNT if required."
                    )
                    response = await self.lc_client.ainvoke(prompt)
                    content = response.content

                    # Dynamic Extraction
                    id_match = re.search(r"ID:\s*#?(\w+)", content)
                    amt_match = re.search(r"AMOUNT:\s*\$?([\d,.]+)", content)
                    
                    claim_id = id_match.group(1) if id_match else "UNKNOWN"
                    raw_amt = amt_match.group(1).replace(",", "") if amt_match else "0.0"
                    
                    intent = {
                        "thought": content.split('\n\n')[0][:250] + "...", 
                        "action": "authorize_claim_payment",
                        "params": {
                            "claim_id": claim_id,
                            "amount": float(raw_amt)
                        },
                        "full_audit_log": content 
                    }
                    
                    meta = response.response_metadata.get("token_usage", {})
                    tokens = meta.get("total_tokens", 0)
                    cost = (tokens / 1000) * 0.02 
                    return intent, cost, tokens
            
            return LangChainAdapter(client)
        
        return client

    async def evaluate(self, guards: List[str], intent: dict = None, value: float = 0.0):
        """
        Modular Triage: Fiscal (Stage 1) -> Policy (Stage 2) -> Judiciary (Stage 3).
        """
        if not self.telemetry.current_session:
            self.telemetry.start_trace(self.persona, "Internal Evaluation")
        
        # 1. FISCAL CIRCUIT BREAKER
        if "fiscal" in guards:
            current_total = self.telemetry.current_session.estimated_cost_usd + value
            self.guard.check_financial_risk(current_total)
            self._log_evaluation("fiscal")
            
        # 2. POLICY & DOMAIN GUARD
        if "policy" in guards and intent:
            # Validates against the YAML manifest
            self.guard.validate_policy(intent.get("action"), intent.get("params", {}))
            self._log_evaluation("policy")

        # 3. JUDICIARY (HITL) ESCALATION
        if "judiciary" in guards and intent:
            action_name = intent.get("action")
            if self.policy.is_high_risk(action_name):
                approved = await self.hitl.secure_approval(
                    agent_id=self.policy.agent_name,
                    reason=f"Human Judiciary authorization: {action_name}",
                    context=intent,
                    triggered_by="judiciary"
                )
                if not approved:
                    raise GovernanceViolation(f"Human Judiciary denied the request for {action_name}")
                self._log_evaluation("judiciary")
        
        return True

    def _log_evaluation(self, guard_name: str):
        """Internal helper for Article 12 compliance."""
        if guard_name not in self.telemetry.current_session.guards_evaluated:
            self.telemetry.current_session.guards_evaluated.append(guard_name)

    async def execute(self, task: str):
        """Governed Reasoning Loop with Forensic Telemetry."""
        self.telemetry.start_trace(self.persona, task)
        current_step, total_tokens = 0, 0
        
        try:
            while current_step < 10:
                response = await self.model.generate_plan(task, self.persona)
                intent, cost, tokens = response if isinstance(response, tuple) else (response, 0, 0)
                total_tokens += tokens
                
                # Governance Interception
                await self.evaluate(
                    guards=["fiscal", "policy", "judiciary"],
                    intent=intent if isinstance(intent, dict) else {"thought": intent},
                    value=cost
                )

                self.telemetry.current_session.estimated_cost_usd += cost
                
                # Tool Execution
                action = intent.get("action")
                params = intent.get("params", {})
                result = await self.perform_action(action, params)
                
                self.telemetry.log_step(intent.get("thought", ""), action, str(result))
                
                if "complete" in str(result).lower(): 
                    break
                current_step += 1

            return self.telemetry.finalize(status="success", tokens=total_tokens)

        except GovernanceViolation as gv:
            return self.telemetry.finalize(status=f"blocked: {str(gv)}", tokens=total_tokens)
        except Exception as e:
            return self.telemetry.finalize(status=f"error: {str(e)}", tokens=total_tokens)

    async def perform_action(self, action: str, params: dict) -> str:
        """Internal bridge to business logic."""
        if not action: return "No action required."
        return f"Action {action} executed with params {params}"