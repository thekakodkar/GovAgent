# src/govagent/context/fiscal_ledger.py
import contextvars
from typing import Dict

_shared_spend = contextvars.ContextVar("shared_spend", default={"cumulative_spend": 0.0})

def reset_fiscal_ledger():
    """Institutional Cleanup: Resets the shared spend to zero."""
    _shared_spend.set({"cumulative_spend": 0.0})

def get_shared_fiscal_metrics() -> Dict[str, float]:
    return _shared_spend.get()

def update_shared_spend(amount: float):
    current = _shared_spend.get()
    current["cumulative_spend"] += amount
    _shared_spend.set(current)
    