import contextvars
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from govagent.agent import ExecutiveAgent

# The Context Variable: A thread-local storage for the active Governance Agent
_active_agent: contextvars.ContextVar[Optional["ExecutiveAgent"]] = contextvars.ContextVar(
    "active_agent", default=None
)

def set_current_agent(agent: "ExecutiveAgent") -> contextvars.Token:
    """
    Institutional Enrollment: Binds an agent to the current async context.
    Returns a token required to reset the context later.
    """
    return _active_agent.set(agent)

def reset_current_agent(token: contextvars.Token) -> None:
    """
    Session Finalization: Clears the agent from the context to prevent leakage.
    """
    _active_agent.reset(token)

def get_current_agent() -> Optional["ExecutiveAgent"]:
    """
    The 'Governor' Finder: Used by decorators to locate the active evaluator.
    """
    return _active_agent.get()