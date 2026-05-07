import pytest
from unittest.mock import AsyncMock
from govagent.telemetry import TelemetryManager

@pytest.mark.asyncio
async def test_cloud_exporter_dispatch():
    """Verifies Phase 3: Telemetry is dispatched to all registered cloud sinks."""
    tm = TelemetryManager()
    mock_exporter = AsyncMock()
    tm.add_exporter(mock_exporter)
    
    tm.start_trace("Director", "Cloud Test")
    await tm.finalize(status="success")
    
    # Ensure the cloud sink received the forensic data
    assert mock_exporter.export.called