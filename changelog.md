## [0.1.5] - 2026-05-03
### Added
- **Synchronous HITL Enforcement**: The agent now treats a human 'Reject' signal as a terminal event, physically breaking the execution loop.
- **Governance Test Suite**: Added `test_governance.py` to verify policy enforcement and guardrail reliability.
- **ExecutionSnapshots**: Enhanced telemetry reporting for forensic-grade audit trails.

### Changed
- **Loop Hardening**: Refactored `ExecutiveAgent` to prioritize governance checks over tool execution.
- **Telemetry Mapping**: Standardized attribute names (e.g., `reasoning_steps`) across the framework.

### Fixed
- Fixed a critical bypass where the agent would continue execution after an intervention request was denied.