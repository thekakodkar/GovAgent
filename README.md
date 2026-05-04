# govAgent: The Enterprise Protocol for Agentic AI

**The Governance-First Framework for Production-Grade Autonomous Systems.**

GovAgent provides a high-abstraction 'Control Plane' for agentic AI. With a **Chain of Accountability**, this lightweight framework helps organizations move autonomous systems from sandbox to production, governed environments.

The latest update introduces a type-safe tool registry that eliminates "Shadow AI" by enforcing strict parity between code and policy.

### Key Capabilities:
- **@tool Registry**: A type-safe decorator that auto-maps Python functions to policy permissions with metadata (risk level, category, signature).
- **Synchronous Governance Audit**: The system performs a "Constitutional Check" at startup, refusing to boot if a tool exists in the code but is unauthorized in the YAML.
- **Risk Hierarchy Enforcement**: Prevents "Risk Downgrading"—if a policy defines an action as HIGH RISK, the code cannot override it to bypass human oversight.
- **Financial Circuit Breaker**: Real-time monitoring of session spend with automated halting when budget caps are reached.
- **Zero-Trust Domain Guardrails**: Hardened protection against unauthorized or unverified web domains.

## 🏗️ Architecture
1. **Executive**: The engine orchestrating the "Think -> Guard -> Act" cycle.
2. **Policy**: Structured YAML-based Digital SOPs.
3. **Registry**: The single source of truth for all governed agent capabilities.
4. **Telemetry**: Real-time auditing of spend and operational ROI.


## 🚧 Roadmap to v0.2.0
- [x] **Hardened Core**: Explicit Intent Validation & Telemetry Contract.
- [x] **Financial Circuit Breaker**: Real-time spend tracking and budget enforcement.
- [x] **Path Independence**: Absolute resolution for Policies.
- [x] **@tool Registry**: Type-safe decorator for auto-mapping permissions.
- [ ] **Decoupled HITL**: Slack & CLI adapters for Judiciary oversight.
- [ ] **Governance Test Suite**: Comprehensive "break-the-guard" testing utility.

## 🛠️ Current Status
The **Executive Engine** is now 4/4 PASSED and production-ready. The system correctly separates reasoning, execution, and telemetry.

## 🎯 Value Proposition
In high-stakes environments, the barrier to AI adoption is **reliability and control**. `govAgent` ensures every action is transparent, budget-aware, and risk-managed. Unlike standard frameworks that prioritize open-ended autonomy, GovAgent enforces a **Chain of Accountability**.

*   **Active Circuit Breakers:** Real-time enforcement of financial and operational limits.
*   **Governance-as-Code:** Human-readable permission manifests (`policy.yaml`) that align technical execution with organizational policy.
*   **Forensic Telemetry:** Standardized audit logs and ROI projections.
*   **Zero-Trust Tooling:** Strict whitelisting for agent actions and domain access.

---

## 🏗️ Core Pillars: The Chain of Accountability
In a professional services or regulated environment, autonomy without accountability is a liability. GovAgent replaces "Black Box" reasoning with a transparent, governed loop:

1.  **Policy (The Law):** Declarative boundaries and "Rules of Engagement" defined by stakeholders in `policy.yaml`.
2.  **Guards (The Enforcement):** Real-time circuit breakers that intercept agent intent *before* API execution to prevent budget or security breaches.
3.  **HITL (The Judiciary):** **Synchronous** Human-in-the-Loop escalation. High-risk actions are blocked until a human provides an explicit "Approve" or "Reject" signal.
4.  **Telemetry (The Evidence):** Forensic-grade audit trails that provide an immutable ledger of compliance and real-world ROI.

---

## 🗺️ Strategic Roadmap

### v0.1.7: Legislative Stability (Current)
*   **Legislative Registry:** Implementation of the @tool decorator for type-safe permission mapping.

*   **Hardened Executive Core:** Stabilized loop with explicit intent validation and telemetry separation.

### v0.2.0: Operational Safety (Current Focus)
*   **Synchronous HITL:** Implementation of decoupled CLI/Slack adapters for real-time intervention.
*   **The Governance Testing Suite:** Comprehensive unit testing utility to verify guardrail enforcement.
*   **The `@tool` Registry:** A type-safe decorator to auto-map Python functions to policy permissions.

### v0.3.0: Enterprise Connectivity
*   **Cloud Telemetry Adapters:** Native exporters for **AWS CloudWatch** and **Azure Monitor**.
*   **Dynamic Budgeting:** Real-time API pricing integration for penny-accurate cost tracking.
*   **SOP Templates:** A library of pre-baked policies for roles like "Legal Researcher" or "Code Auditor."

---

## 🧪 Testing & Validation
GovAgent prioritizes reliability. We maintain a dual-layer testing utility:
*   **Operational Flow (`test_flow.py`):** Ensures the "Happy Path" remains functional across library updates.
*   **Governance Verification (`test_governance.py`):** Specifically attempts to breach policy to ensure guards and HITL triggers correctly block unauthorized intent.

Run the full suite with: `pytest tests/`

---

## 🚧 Development Status (WIP)
**GovAgent is rapidly evolving.** We have successfully moved the HITL module from a passive placeholder to an active, synchronous blocking mechanism.

### ✅ Completed Modules
*   **Governance Manifest (`policy.py`):** Structured YAML-based policy enforcement with high-risk tool detection.
*   **Forensic Telemetry (`telemetry.py`):** Real-time ROI and audit trail generation.
*   **Circuit Breakers (`guards.py`):** Financial and operational risk mitigation logic.
*   **Synchronous HITL (`hitl.py`):** Multi-adapter manager (CLI/Slack-ready) for human intervention.
*   **The Executive Loop (`agent.py`):** An async orchestration engine that treats governance as a blocking priority.

---

## 📖 Usage Example: Controlled Execution

```python
from govagent.agent import ExecutiveAgent
from govagent.policy import Policy

# Load Hardened Policy
policy = Policy.from_yaml("policies/healthcare_ops_policy.yaml")

# Initialize Executive Agent
agent = ExecutiveAgent(
    persona="Technology Director",
    policy=policy,
    model_client=YourModelClient()
)

# Execute Governed Task
report = await agent.execute("Analyze Q4 market shifts.")
print(f"Status: {report.status} | ROI: ${report.estimated_cost_usd}")
```

---

## 🤝 Call for Contributions
We are building GovAgent to be the industry standard for accountable AI. I welcome collaborators from both technical and strategic backgrounds.

### 👩‍💻 Technical Contributions
*   **Slack/Teams Adapters:** Help us finalize the `SlackAdapter` for mobile-first human approvals.
*   **Cloud Exporters:** Native integrations for enterprise logging stacks (ELK, CloudWatch).

### 👔 Strategic Contributions
*   **Standard Policy Library:** Help us draft pre-built `policy.yaml` templates for regulated industries (Finance, Healthcare, Legal).

---
**"Governance is not a constraint; it is the catalyst for enterprise AI adoption."**

---

### Author Stamp
*   **Framework:** GovAgent v0.2.0 (Pre-release)
*   **Status:** Active / Open-Source Standard
*   **Compliance:** Designed for Enterprise-Grade Accountability
