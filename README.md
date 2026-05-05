## govAgent: Enterprise-Grade AI Governance Framework

**The Governance-First Framework for Production-Grade Autonomous Systems.**

GovAgent provides a high-abstraction **Control Plane** for agentic AI. With a clear chain of accountability, this lightweight framework helps move autonomous systems from experimental sandboxes into governed, production environments.

<img width="1097" height="479" alt="ImagegoV" src="https://github.com/user-attachments/assets/4e05d505-63d6-4f14-9475-cc00b4f20d73" />

The v0.2.2 Update introduces a standardized LangChain Integration Layer and hardened Slack Socket Mode connectivity, ensuring that high-risk AI actions are always subject to verified human oversight.

---

## 🏗️ Core Pillars: The Chain of Accountability
GovAgent replaces "Black Box" reasoning with a transparent, governed loop:

1.  **Policy (The Law):** Declarative boundaries and "Rules of Engagement" defined by stakeholders in `policy.yaml`.
2.  **Guards (The Enforcement):** Real-time circuit breakers that intercept agent intent *before* API execution to prevent budget or security breaches.
3.  **HITL (The Judiciary):** **Synchronous** Human-in-the-Loop escalation. High-risk actions are physically blocked until an explicit "Approve" or "Reject" signal is received via Slack or CLI.
4.  **Telemetry (The Evidence):** Forensic-grade audit trails providing an immutable ledger of compliance and real-world ROI.

---

## ⚖️ Regulatory Compliance: EU AI Act (Regulation 2024/1689)

GovAgent is engineered to facilitate compliance for **High-Risk AI Systems** as defined under the EU AI Act. The framework provides the technical primitives required to satisfy key transparency and oversight mandates:

*   **Article 14: Human Oversight**  
    Native **Synchronous HITL** (Human-in-the-Loop) adapters ensure that high-risk tool execution is physically gated by natural persons in real-time.
    
*   **Article 9: Risk Management System**  
    Automated, policy-driven enforcement (via `policy.yaml`) identifies and mitigates operational and financial risks *prior* to tool deployment.
    
*   **Article 12: Record-Keeping & Traceability**  
    Immutable **Forensic Telemetry** captures the full "Chain of Accountability," including agent reasoning, tool parameters, and the identity of the human overseer who authorized the action.

*   **Article 13: Transparency & Provision of Information**  
    Automated generation of Execution Snapshots allows for the clear explanation of AI-driven outputs to end-users and regulators.
    
---

## 🛠️ Key Capabilities (v0.2.2)
* **🔗 LangChain Bridge:** Standardized `@langchain_tool` wrappers for seamless interception of LangChain agent intents.
* **🔌 Socket Mode Judiciary:** Secure, persistent WebSocket connections for Slack oversight without exposing public endpoints (No Ngrok required).
* **📦 Pydantic Telemetry:** Hardened serialization of agent tasks to ensure audit logs meet strict enterprise data schemas.
* **⚠️ Constitutional Startup Check:** Refuses to boot if tool registry and policy permissions do not match, eliminating "Shadow AI."
* **🛡️ Zero-Trust Guardrails:** Hardened whitelisting for all agent actions and financial disbursements.

---
## 🗺️ Strategic Roadmap

### ✅ v0.2.2: Operational Stability (Current)
* **LangChain Integration:** Standardized tool-guarding for LangChain ecosystems.
* **Synchronous HITL:** Stabilized Slack Socket Mode and CLI adapters for real-time intervention.
* **Intent Serialization:** Resolved telemetry validation errors via JSON-based intent snapshots.

### 🚀 v0.3.0: Enterprise Connectivity (Next)
* **Fiscal Ceilings:** Recursive approval for multi-agent sub-tasks and "Total Cost of Operation" (TCO) guardrails.
* **Cloud Exporters:** Native integrations for enterprise logging stacks (AWS CloudWatch / Azure Monitor).
* **Dynamic Budgeting:** Real-time API pricing integration for penny-accurate cost tracking.
---

## 📖 Usage Example: Governed LangChain Tool (Simplified API)

GovAgent v0.2.2 introduces a streamlined import structure and native support for LangChain tool interception. The following example demonstrates how to gate a high-risk financial transaction with a synchronous Slack Judiciary.

```python
import os
import asyncio
from langchain_core.tools import tool as langchain_tool
from govagent import ExecutiveAgent, Policy, HITLManager, SlackJudiciaryAdapter

@langchain_tool
async def healthcare_payment_tool(amount: float) -> str:
    """Authorizes payments for healthcare claims. Input: amount."""
    
    # 1. Initialize the Judiciary Adapter (Slack Socket Mode)
    # This establishes a secure, persistent connection for real-time oversight.
    adapter = SlackJudiciaryAdapter(
        bot_token=os.getenv("SLACK_BOT_TOKEN"),
        app_token=os.getenv("SLACK_APP_TOKEN"),
        channel_id=os.getenv("SLACK_CHANNEL_ID")
    )
    adapter.start() 
    
    # 2. Initialize Governance Layer via Flat API
    manager = HITLManager(adapter=adapter)
    policy = Policy.from_yaml("policies/healthcare_policy.yaml")
    
    # 3. ARTICLE 14: Synchronous Human Oversight
    # Execution physically pauses here until a signal is received from Slack.
    print(f"⚖️ [GovAgent] Intercepting request for ${amount}...")
    
    approved = await manager.secure_approval(
        agent_id="Healthcare-Director-v0.2.2",
        reason=f"High-risk authorization required for GuardedPayment (${amount}).",
        context={
            "amount": f"${amount}",
            "compliance_check": "EU-AI-ACT-HIGH-RISK"
        }
    )

    if approved:
        # Business logic proceeds only after explicit human authorization
        return f"SUCCESS: Payment of ${amount} authorized via Slack."
    
    return "REJECTED: Transaction denied by Human Judiciary."

# Example Invocation
async def main():
    result = await healthcare_payment_tool.ainvoke({"amount": 1200.0})
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```
---

**"Governance is not a constraint; it is the catalyst for enterprise AI adoption."**

---

### Author Stamp
*   **Framework:** GovAgent v0.2.2 (Stable)
*   **Status:** Active / Open-Source Standard
*   **Compliance:** Designed for Enterprise-Grade Accountability
