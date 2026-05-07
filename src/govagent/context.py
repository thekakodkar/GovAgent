import contextvars
from typing import Optional, TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from govagent.agent import ExecutiveAgent

# Enhanced Context Variable for v0.4.0 Swarm Support
_active_agent: contextvars.ContextVar[Optional["ExecutiveAgent"]] = contextvars.ContextVar(
    "active_agent", default=None
)

# Shared Fiscal state across the current async thread
_shared_fiscal_state: contextvars.ContextVar[Dict[str, float]] = contextvars.ContextVar(
    "shared_fiscal_state", default={"cumulative_spend": 0.0, "tco_ceiling": 0.0}
)

def set_current_agent(agent: "ExecutiveAgent") -> contextvars.Token:
    return _active_agent.set(agent)

def reset_current_agent(token: contextvars.Token) -> None:
    _active_agent.reset(token)

def get_current_agent() -> Optional["ExecutiveAgent"]:
    return _active_agent.get()

def update_shared_spend(amount: float):
    """Penny-accurate update across the recursive swarm."""
    state = _shared_fiscal_state.get().copy()
    state["cumulative_spend"] += amount
    _shared_fiscal_state.set(state)

def get_shared_fiscal_metrics() -> Dict[str, float]:
    return _shared_fiscal_state.get()