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

## [0.1.6] - 2026-05-03
### Added
- [x] **Hardened Core**: Explicit Intent Validation & Telemetry Contract.
- [x] **Financial Circuit Breaker**: Real-time spend tracking and budget enforcement.
- [x] **Path Independence**: Absolute resolution for Policies.

## [0.1.7] - 2026-05-04
### Added
- **Legislative Tool Registry**: Introduced the `@tool` decorator to auto-map Python functions to governance permissions.
- **Strict Risk Parity Audit**: Implemented `Policy.validate_registry()` to prevent "Risk Downgrading" between code and YAML.
- **Shadow Tool Prevention**: The system now halts at startup if a code-level tool is not explicitly authorized in the Policy YAML.
- **Interface Reflection**: Capture of function signatures and docstrings for future automated prompt engineering.

### Fixed
- **Policy Attribute Sync**: Standardized naming for `max_spend_usd` and `require_human_approval` to ensure internal Guard compatibility.
- **Cross-Walk Validation**: Resolved the gap where code and policy could drift out of alignment without triggering a failure.