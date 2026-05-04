## govAgent: Enterprise-Grade AI Governance Framework

**The Governance-First Framework for Production-Grade Autonomous Systems.**

GovAgent provides a high-abstraction **Control Plane** for agentic AI. With a clear chain of accountability, this lightweight framework helps move autonomous systems from experimental sandboxes into governed, production environments.

<img width="1097" height="479" alt="ImagegoV" src="https://github.com/user-attachments/assets/4e05d505-63d6-4f14-9475-cc00b4f20d73" />


The **v0.2.0 Stable Release** introduces a persistent, bi-directional Judiciary layer, ensuring that high-risk AI actions are always subject to human verification before execution.

---

## 🏗️ Core Pillars: The Chain of Accountability
GovAgent replaces "Black Box" reasoning with a transparent, governed loop:

1.  **Policy (The Law):** Declarative boundaries and "Rules of Engagement" defined by stakeholders in `policy.yaml`.
2.  **Guards (The Enforcement):** Real-time circuit breakers that intercept agent intent *before* API execution to prevent budget or security breaches.
3.  **HITL (The Judiciary):** **Synchronous** Human-in-the-Loop escalation. High-risk actions are physically blocked until an explicit "Approve" or "Reject" signal is received via Slack or CLI.
4.  **Telemetry (The Evidence):** Forensic-grade audit trails providing an immutable ledger of compliance and real-world ROI.

---

## 🇪🇺 EU AI Act Alignment
GovAgent is architected to meet the rigorous transparency and oversight standards for **High-Risk AI Systems**:

*   **Human Oversight (Article 14):** Native HITL adapters ensure high-risk systems are overseen by natural persons in real-time.
*   **Risk Management (Article 9):** Automated policy enforcement identifies and mitigates operational risks before they manifest.
*   **Traceability (Article 12):** Forensic telemetry captures who approved an action and when, satisfying the "Chain of Accountability" required for regulatory audits.

---

## 🛠️ Key Capabilities (v0.2.0 Stable)
*   **@tool Registry:** A type-safe decorator that auto-maps Python functions to policy permissions (risk level, category, signature).
*   **Socket Mode Handshake:** Secure, persistent WebSocket connections for judiciary oversight without exposing public endpoints.
*   **Financial Circuit Breakers:** Real-time monitoring of session spend with automated halting when budget caps are reached.
*   **Constitutional Startup Check:** Refuses to boot if tool code and policy permissions do not match, eliminating "Shadow AI".
*   **Zero-Trust Guardrails:** Hardened whitelisting for all agent actions and web domain access.

---

## 🗺️ Strategic Roadmap

### ✅ v0.2.0: Operational Safety (Current Stable)
*   **Synchronous HITL:** Full implementation of Slack and CLI adapters for real-time intervention.
*   **Legislative Registry:** Stabilized @tool decorator for type-safe permission mapping.
*   **Forensic Telemetry:** Real-time ROI and audit trail generation.

### 🚀 v0.3.0: Enterprise Connectivity (Next)
*   **Fiscal Ceilings:** Recursive approval for multi-agent sub-tasks and "Total Cost of Operation" (TCO) guardrails.
*   **Cloud Exporters:** Native integrations for enterprise logging stacks like AWS CloudWatch and Azure Monitor.
*   **Dynamic Budgeting:** Real-time API pricing integration for penny-accurate cost tracking.

---

## 📖 Usage Example: Controlled Execution

```python
from govagent.agent import ExecutiveAgent
from govagent.policy import Policy

# Load Hardened Policy (The Law)
policy = Policy.from_yaml("policies/enterprise_audit_policy.yaml")

# Initialize Executive Agent
agent = ExecutiveAgent(
    persona="Technology Director",
    policy=policy,
    model_client=YourModelClient()
)

# Execute Governed Task
# High-risk tools (e.g., payments) will pause and alert Slack.
report = await agent.execute("Analyze Q4 market shifts and authorize $5k payment.")
print(f"Status: {report.status} | ROI: ${report.estimated_cost_usd}")
```

---

**"Governance is not a constraint; it is the catalyst for enterprise AI adoption."**

---

### Author Stamp
*   **Framework:** GovAgent v0.2.0 (Stable)
*   **Status:** Active / Open-Source Standard
*   **Compliance:** Designed for Enterprise-Grade Accountability
