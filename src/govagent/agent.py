from typing import List, Optional, Any
from govagent.policy import Policy
from govagent.guards import CircuitBreaker, GovernanceViolation
from govagent.telemetry import TelemetryManager
from govagent.hitl import HITLManager

class ExecutiveAgent:
    """
    The core execution engine. Orchestrates reasoning while 
    enforcing governance constraints in real-time.
    """
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
        self.model = model_client
        self.guard = CircuitBreaker(policy)
        self.telemetry = telemetry or TelemetryManager()
        self.hitl = hitl_manager or HITLManager()

    async def execute(self, task: str):
        """
        The 'Governed Reasoning' Loop: Think -> Guard -> Act -> Record.
        Strictly enforces a Hard-Stop on human rejection.
        """
        self.telemetry.start_trace(self.persona, task)
        current_step = 0
        max_steps = 10 
        
        try:
            while current_step < max_steps:
                # 1. Financial Guard Check
                self.guard.check_financial_risk(self.telemetry.current_session.estimated_cost_usd)
                
                # 2. Reasoning Phase
                thought, action, params = await self.model.generate_plan(task, self.persona)
                
                # 3. Action Validation Guard (Policy Enforcement)
                self.guard.validate_action(action, params)
                
                # 4. Synchronous HITL Check (The Judiciary)
                confidence = 0.9 
                
                if self.policy.is_high_risk(action) or confidence < self.policy.confidence_threshold:
                    print(f"⚠️ Intervention required for action: {action}")
                    
                    approved = await self.hitl.secure_approval(
                        agent_id=self.policy.agent_name,
                        reason=f"High-risk action: {action}" if self.policy.is_high_risk(action) else "Low confidence",
                        context={"action": action, "params": params, "thought": thought}
                    )

                    # DEFENSIVE GATE: Only proceed if approved is explicitly True
                    if approved is not True:
                        print(f"🛑 HALTING: Rejection or timeout for {action}")
                        return self.telemetry.finalize(
                            status=f"rejected: Human denied {action}", 
                            tokens=current_step * 100
                        )

                # 5. Execution (ONLY reachable if step 4 passed)
                result = await self.perform_action(action, params)
                
                # 6. Logging & Completion check
                self.telemetry.log_step(thought, action, result)
                
                if self.is_task_complete(result):
                    break
                
                current_step += 1

            return self.telemetry.finalize(status="success", tokens=current_step * 150)

        except GovernanceViolation as gv:
            return self.telemetry.finalize(status=f"blocked: {str(gv)}", tokens=current_step * 50)
        except Exception as e:
            return self.telemetry.finalize(status=f"error: {str(e)}", tokens=0)

    async def perform_action(self, action: str, params: dict):
        """Standard tool execution simulation."""
        return f"Executed {action} with success. Task complete."

    def is_task_complete(self, result: str) -> bool:
        """Determines if the session objectives are met."""
        return "complete" in result.lower()