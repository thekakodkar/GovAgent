from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseExporter(ABC):
    """Institutional Exporter Interface v0.4.0."""
    @abstractmethod
    async def export(self, snapshot_data: Dict[str, Any]) -> bool:
        """Standardized contract for Cloud-Native Sinks."""
        pass