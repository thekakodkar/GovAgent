# src/govagent/context/fiscal_ledger.py
import contextvars
from typing import Dict
from pydantic import BaseModel, Field

class FiscalStateSnapshot(BaseModel):
    """Immutable representation of live swarm resource matrices to avoid async bleeding."""
    cumulative_spend: float = 0.0
    task_counter: int = 0

# Enforce a strict type-safe structural ContextVar definition
_shared_spend: contextvars.ContextVar[FiscalStateSnapshot] = contextvars.ContextVar(
    "shared_spend", 
    default=FiscalStateSnapshot(cumulative_spend=0.0, task_counter=0)
)

def reset_fiscal_ledger() -> None:
    """Institutional Cleanup: Atomically resets the shared spend matrices back to baseline."""
    _shared_spend.set(FiscalStateSnapshot(cumulative_spend=0.0, task_counter=0))

def get_shared_fiscal_metrics() -> Dict[str, float]:
    """Retrieves standard flat metric maps for cascading circuit breakers."""
    state = _shared_spend.get()
    return {
        "cumulative_spend": state.cumulative_spend,
        "task_counter": float(state.task_counter)
    }

def update_shared_spend(amount: float) -> None:
    """
    Atomically updates aggregate swarm expenditures.
    Generates a fresh state snapshot out-of-band to guarantee thread-safe isolation.
    """
    current_snapshot = _shared_spend.get()
    
    # Instantiate a completely pristine copy with mutated metrics to protect async boundaries
    updated_snapshot = FiscalStateSnapshot(
        cumulative_spend=round(current_snapshot.cumulative_spend + amount, 6),
        task_counter=current_snapshot.task_counter + 1
    )
    
    _shared_spend.set(updated_snapshot)