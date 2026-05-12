## CHANGELOG.md

All notable changes to the **GovAgent** framework are documented in this file. This project adheres to a "Governance-First" versioning strategy, prioritizing human oversight and fiscal accountability.

### [0.5.0] - 2026-05-12
### "Federated Judiciary" Release: Consensus-Driven Governance & Forensic Resilience
### ⚖️ Added: Phase 1 - Federated M-of-N Consensus
- **Federated Quorum Logic:** Introduced the ApprovalRequest model with min_approvals support, requiring multiple human stakeholders to reach consensus before high-risk execution.
- **M-of-N Quorum Extraction:** Enhanced ExecutiveAgent and HITLManager to dynamically extract quorum requirements from the institutional policy manifest.
- **Threaded Slack Judiciary:** Implemented message_ts tracking in the SlackJudiciaryAdapter to support persistent, threaded voting within Slack channels.

### 🧠 Added: Phase 2 - Qualitative Semantic Guardrails
- **Semantic Alignment Judge:** Integrated a vector-based SemanticGuard that evaluates agent "Thoughts" against institutional mission statements and prohibited strategies.
- **Intent Alignment Scoring:** Implemented a similarity-threshold check (default 0.85) to block predatory or non-compliant reasoning before tool selection.

### 📡 Added: Phase 3 - Forensic Self-Healing (DLQ)
- **Local Dead Letter Queue (DLQ):** Developed a self-healing mechanism in TelemetryManager that automatically buffers forensic snapshots to logs/audit_buffer.jsonl if cloud sinks (AWS/Azure) are unreachable.
- **Execution Snapshot Hardening:** Expanded the ExecutionSnapshot schema to include guards_evaluated, ensuring a deterministic record of which triage stages (Fiscal, Semantic, Judiciary) were passed.

### 🛡️ Fixed: Privacy & Logic Integrity
- **Stage 0 Address Redaction:** Hardened the PrivacyGuard with a custom regex-based Pattern Recognizer to successfully scrub street-level PII (e.g., "123 Main St"), resolving an Article 9 compliance gap.
- **Safe Policy Accessors:** Refactored CircuitBreaker and ExecutiveAgent to use getattr for policy configuration, preventing AttributeError crashes during partial policy loads.
- **Indentation & Syntax:** Resolved critical indentation errors in the ExecutiveAgent.evaluate method that previously blocked institutional test suites.

## [0.4.0] - 2026-05-07
### "Sovereign Swarm" Release: Cloud-Native Governance & Recursive Fiscal Control

### 💸 Added: Phase 2 - Recursive Fiscal Sovereignty
- **Recursive TCO Tracking**: Introduced an institutional context that aggregates **Total Cost of Operation (TCO)** across parent and sub-agents, preventing "Budget Fragmentation" in complex swarms.
- **Shared Fiscal Metrics**: Implemented `get_shared_fiscal_metrics` and `update_shared_spend` to provide a single source of truth for financial ceilings across async threads.
- **Penny-Accurate Pricing**: Integrated a dedicated pricing engine in `telemetry.py` to calculate exact token costs before finalization.

### ☁️ Added: Phase 3 - Institutional Evidence (Cloud SOC)
- **Multi-Sink Dispatch**: Refactored `TelemetryManager.finalize` as an asynchronous engine capable of broadcasting forensic snapshots to multiple destinations simultaneously.
- **AWS CloudWatch Exporter**: Launched native integration for real-time log ingestion into AWS, supporting enterprise-grade security monitoring.
- **Azure Monitor Exporter**: Provided architectural support for Azure Data Collection Rules (DCR) for long-term regulatory record-keeping.
- **Mock Forensic Sink**: Developed a high-fidelity `MockSOCExporter` for local validation of telemetry dispatch without requiring cloud credentials.

### 🛡️ Added: Phase 1 - Structural Hardening
- **Article 9 Privacy Guard**: Integrated an automated **Stage 0** defense using Microsoft Presidio to redact PII (Personally Identifiable Information) before tasks reach the LLM.
- **Type-Safe Intent Validation**: Replaced regex-based extraction with **Pydantic V2 Schema Enforcement** in the tool registry to ensure deterministic integrity of all tool parameters.

### 🛠️ Fixed: Async Lifecycle & Finalization
- **Coroutine Resolution**: Patched `ExecutiveAgent.execute` to fully `await` all telemetry paths, resolving a critical `AttributeError` where audit reports were returned as unresolved coroutines.
- **Address Leakage Patch**: Hardened the `PrivacyGuard` with a regex-based "Safety Net" to ensure physical addresses (e.g., "123 Main St") are successfully captured as `LOCATION` entities.

## [0.3.0] - 2026-05-07
### Major Release: Institutional Scaling & Terminal Integrity

### 🏛️ Added: Invisible Governance Layer
- **Context-Aware Execution**: Implemented `contextvars` in `govagent.context` to track active `ExecutiveAgent` sessions across async threads, eliminating the need for global variables.
- **Unified Tool Decorator**: Introduced `@tool` in `govagent.registry` which automatically intercepts tool calls to perform governance evaluation via the active context.
- **Institutional Factory Pattern**: Added `ExecutiveAgent.bootstrap()` for one-line initialization of governed sessions, inclusive of policy loading and Slack adapter attachment.

### ⚖️ Added: Judiciary & Compliance Enhancements
- **Synchronous HITL**: Enhanced `HITLManager` and `SlackJudiciaryAdapter` to provide blocking, real-time human oversight for high-risk tools.
- **Article 9/14 Compliance**: Standardized tool manifests to ensure no "Shadow IT" tools can execute without explicit YAML authorization.

### 🛡️ Fixed: Loop & Terminal Stability
- **Terminal Transaction Logic**: Refactored `ExecutiveAgent.execute` loop to force a hard return after any `execute_financial_transaction`, preventing "Reasoning Loops" and duplicate approval requests.
- **Rejection Circuit Breaker**: Ensured that a **Human Judiciary Rejection** acts as a terminal event, instantly killing the agent loop and preventing Slack notification spam.
- **Indentation & Syntax Integrity**: Resolved logic errors in the reasoning loop that previously caused agents to ignore safety thresholds.

### ⚙️ Changed: Generic Architectural Pivot
- **Industry-Agnostic Schema**: Renamed specific tools (e.g., `healthcare_payment_tool`) to generic counterparts like `execute_financial_transaction` to support horizontal scaling across Fintech, Supply Chain, and Audit sectors.
- **Forensic Telemetry**: Updated `TelemetryManager` to log every stage of the cascading triage (Fiscal -> Policy -> Judiciary).

## [0.2.3] - 2026-05-06
### Added
- **LangChain Integration Adapter**: Automated wrapper in `ExecutiveAgent` to standardize LangChain `ChatOpenAI` clients to the GovAgent contract.
- **Dynamic Intent Extraction**: Replaced hardcoded parameters with Regex-based extraction for `claim_id` and `amount` within the model adapter.
- **Self-Healing Telemetry**: Automatic creation of `/logs` directory and `audit_trail.jsonl` persistence.

### Changed
- **Modular Evaluation Engine**: Refactored `evaluate()` to follow a cascading triage: Fiscal (Cheap) -> Policy (Automated) -> Judiciary (High-Risk/HITL).
- **HITL Interface**: Streamlined Slack context messages to provide "Executive Summaries" rather than raw LLM thought-logs.

### Fixed
- Resolved `NoneType` and `AttributeError` issues during agent initialization.
- Fixed namespace exports in `govagent.hitl` for `SlackJudiciaryAdapter`.

## [0.2.2] - 2026-05-05
### Added
- **LangChain Integration**: Standardized @langchain_tool bridging logic for GovAgent interception.
- **Socket Mode Support**: Transitioned Slack Judiciary to persistent Socket Mode for increased security.
- **Intent Serialization**: JSON-based serialization for tool inputs to ensure telemetry data integrity.

### Fixed
- **Validation Schema**: Resolved Pydantic string-type constraints in ExecutionSnapshot.
- **Registry Mapping**: Fixed namespace mismatches between Python tool decorators and YAML policy names.

---

## [0.2.0] - 2026-05-04 (Stable)

### 🏛️ Added: The Judiciary Pillar
*   **Synchronous HITL Manager**: Introduced a core orchestration layer to manage Human-in-the-Loop (HITL) requests across multiple communication adapters.
*   **Slack Socket Mode Adapter**: Implemented a real-time, mobile-first intervention bridge using secure WebSockets, enabling remote executive oversight without public endpoint exposure.
*   **Stateful Execution Blocking**: Developed a mechanism using `asyncio.Future` patterns that physically pauses the agent's logic thread until a human "Approve" or "Reject" signal is received.
*   **Interactive Block Kit UI**: Added rich, structured Slack message templates providing forensic context (Agent ID, Reason, Parameters) for executive decision-making.

### 🛠️ Improvements & Refactoring
*   **EU AI Act Compliance**: Mapped code-level functionality to **Article 14 (Human Oversight)** and **Article 12 (Traceability)** requirements.
*   **Legislative Registry Hardening**: Stabilized the `@tool` decorator to ensure strict type-safety and parity between Python signatures and YAML policy permissions.
*   **Self-Healing Handshake**: Added intelligent detection for common Slack errors (e.g., `not_in_channel`) with automated join attempts where permitted by scopes.
*   **Executive Audit Logging**: Interaction handlers now capture and log the specific Slack User ID of the human overseer to maintain the "Chain of Accountability".

### 🛡️ Security & Integrity
*   **Zero-Trust Identity**: Standardized the dual-token system using `SLACK_APP_TOKEN` (`xapp-`) for connection and `SLACK_BOT_TOKEN` (`xoxb-`) for privileged communication.
*   **Thread-Safe Callbacks**: Integrated `loop.call_soon_threadsafe` to bridge background WebSocket threads with the main asynchronous execution loop.
*   **Constitutional Startup Check**: Enhanced the boot-up sequence to refuse execution if tool code and policy permissions do not align.

---

## [0.1.7] - 2026-05-04

### 📜 Added: Legislative Tool Registry
*   **Legislative Tool Registry**: Introduced the `@tool` decorator to auto-map Python functions to governance permissions.
*   **Strict Risk Parity Audit**: Implemented `Policy.validate_registry()` to prevent "Risk Downgrading" between code and YAML.
*   **Shadow Tool Prevention**: The system now halts at startup if a code-level tool is not explicitly authorized in the Policy YAML.
*   **Interface Reflection**: Captures function signatures and docstrings for automated prompt engineering.

### 🛠️ Fixed
*   **Policy Attribute Sync**: Standardized naming for `max_spend_usd` and `require_human_approval` to ensure internal Guard compatibility.
*   **Cross-Walk Validation**: Resolved the gap where code and policy could drift out of alignment without triggering a failure.

---

## [0.1.6] - 2026-05-03

### ✅ Added
*   **Hardened Core**: Implemented explicit Intent Validation and a Telemetry Contract.
*   **Financial Circuit Breaker**: Real-time spend tracking and budget enforcement.
*   **Path Independence**: Absolute resolution for Policies.

---

## [0.1.5] - 2026-05-03

### 🏛️ Added
*   **Synchronous HITL Enforcement**: The agent now treats a human 'Reject' signal as a terminal event, physically breaking the execution loop.
*   **Governance Test Suite**: Added `test_governance.py` to verify policy enforcement and guardrail reliability.
*   **ExecutionSnapshots**: Enhanced telemetry reporting for forensic-grade audit trails.

### 🛠️ Changed
*   **Loop Hardening**: Refactored `ExecutiveAgent` to prioritize governance checks over tool execution.
*   **Telemetry Mapping**: Standardized attribute names (e.g., `reasoning_steps`) across the framework.

### 🛠️ Fixed
*   **Bypass Resolution**: Fixed a critical bypass where the agent would continue execution after an intervention request was denied.