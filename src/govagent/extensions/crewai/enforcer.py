import functools
import yaml
from typing import Any, Dict, Optional
from crewai import Crew, Agent
from crewai.llm import LLM  # Natively wrap strings into structured LLM instances

# Import core framework packages exactly as verified by your demo scripts
from govagent import Policy, PolicyBasedRouter, RouterConfig
from govagent.registry import GlobalRegistry

class GovAgentEnforcer:
    """
    Non-invasive Enterprise Guardrail Middleware Wrapper for CrewAI.
    Uses clean method-level interception to bypass Pydantic model state validation.
    """
    def __init__(self, crew: Crew, policy_path: str):
        self.crew = crew
        
        # 1. Parse using your factory method to keep core dependencies synchronized
        self.policy = Policy.from_yaml(policy_path)
        
        # 2. Safely load the raw configuration to read custom parameters natively
        with open(policy_path, "r") as f:
            self.raw_config = yaml.safe_load(f) or {}
            
        default_provider = getattr(self.policy, "default_provider", "local_ollama")
        
        # 3. Reconstruct your standard RouterConfig mapping
        router_cfg = RouterConfig(
            routing_mode=getattr(self.policy, "routing_mode", "LOCAL_ONLY"),
            default_provider=default_provider,
            rules=getattr(self.policy, "routing_rules", [])
        )
        
        placeholder_clients = {default_provider: object()}
        self.router = PolicyBasedRouter(clients=placeholder_clients, config=router_cfg)
        self.registry = GlobalRegistry()
        
        # 4. Apply class-level execution interceptors
        self._apply_execution_interceptors()

    def _apply_execution_interceptors(self) -> None:
        """
        Intercepts internal execution boundaries safely by monkeypatching the class method 
        context out-of-band, avoiding Pydantic instance-level assignment restrictions.
        """
        orig_execute_task = Agent.execute_task

        @functools.wraps(orig_execute_task)
        def wrapped_execute_task(agent_self: Agent, task: Any, context: Optional[Any] = None, tools: Optional[Any] = None, *args, **kwargs):
            # A. Evaluate Agent Tools against the raw policy configuration
            gov_rules = self.raw_config.get("governance_rules", {})
            authorized_tools = gov_rules.get("authorized_tools", [])

            active_tools = tools or agent_self.tools or []
            for tool in active_tools:
                # Extract the underlying string name from CrewAI's wrapper model properties safely
                tool_name = getattr(tool, "name", None) or getattr(tool, "__name__", str(tool))
                
                # Strict Tool Gating Block
                if authorized_tools and tool_name not in authorized_tools:
                    raise PermissionError(
                        f"[govAgent Security Violation] Unauthorized tool invocation blocked: '{tool_name}'"
                    )

            # B. Out-of-Band Policy-Based Model Routing Evaluation
            payload_sample = f"{getattr(task, 'description', '')} {context or ''}"
            
            dynamic_target_model = None
            routing_profiles = self.raw_config.get("routing_profiles", {})
            
            if routing_profiles and any(kw in payload_sample.lower() for kw in ["payroll", "ledger"]):
                dynamic_target_model = routing_profiles.get("default_local_slm")
            
            if not dynamic_target_model:
                # Fallback to a string layout format CrewAI understands
                dynamic_target_model = "ollama/llama3"

            if dynamic_target_model:
                # 💡 CRITICAL FIX: Wrap the target string into an authentic CrewAI LLM instance
                # This satisfies `isinstance(self.llm, BaseLLM)` checking perfectly
                validated_llm = LLM(model=dynamic_target_model)
                object.__setattr__(agent_self, "llm", validated_llm)

            return orig_execute_task(agent_self, task, context, tools, *args, **kwargs)

        # Apply to the Class structure cleanly
        Agent.execute_task = wrapped_execute_task