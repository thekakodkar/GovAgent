# tests/test_harbor_registry.py
import pytest
from govagent.registry.manager import GlobalRegistry, tool
from govagent.guards.circuit_breaker import GovernanceViolation

def test_registry_legislation_blocks_unauthorized_tool():
    """Asserts that the framework instantly drops execution on completely unlegislated capabilities."""
    registry = GlobalRegistry()
    registry.tools.clear() # Reset singleton state space
    
    with pytest.raises(GovernanceViolation) as excinfo:
        registry.verify_and_resolve_tool("unregistered_arbitrary_shell_script")
        
    assert "REGISTRY EXCEPTION" in str(excinfo.value)

def test_registry_legislation_intercepts_malicious_cve_container():
    """Asserts that tools hosted inside contaminated images trigger a strict global circuit breaker drop."""
    registry = GlobalRegistry()
    registry.tools.clear()

    @tool(
        name="database_wipe",
        oci_repository="bizzteq/malicious-db-utils",
        artifact_digest="sha256:corrupted-hash"
    )
    def payload_tool():
        return "Executing..."
        
    with pytest.raises(GovernanceViolation) as excinfo:
        registry.verify_and_resolve_tool("database_wipe")
        
    assert "HARBOR REGISTRY BLOCK" in str(excinfo.value)
    print("✅ Harbor Realigned Supply Chain circuit breaker verified successfully.")