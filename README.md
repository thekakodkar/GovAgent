## govAgent: Enterprise-Grade AI Governance Framework

**The Governance-First Framework for Production-Grade Autonomous Systems.**

GovAgent provides a high-abstraction **Control Plane** for agentic AI. With a clear chain of accountability, this lightweight framework helps move autonomous systems from experimental sandboxes into governed, production environments.

<img width="1097" height="479" alt="ImagegoV" src="https://github.com/user-attachments/assets/4e05d505-63d6-4f14-9475-cc00b4f20d73" />

The v0.2.3 Update transforms the framework into a proactive Triage Engine, introducing Modular Guards that intercept risky or expensive actions at the earliest possible stage, significantly increasing the Business ROI of autonomous sessions.

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

## 🛠️ Key Capabilities (v0.2.3)
* **🛡️ Modular Guard Engine:** Cascading triage (fiscal -> policy -> judiciary) to stop invalid or over-budget requests at zero token cost.
* **🔗 Automated Model Adapter:** Standardizes ChatOpenAI patterns to the GovAgent contract, ensuring ROI and token telemetry are captured automatically.
* **🔍 Dynamic Intent Extraction:** Replaces hardcoded parameters with regex-based parsing to identify Tool IDs and financial amounts directly from LLM reasoning.
* **📂 Self-Healing Telemetry:** Automated management of the /logs directory and audit_trail.jsonl persistence for forensic-grade audit readiness.
* **⚖️ High-Signal Judiciary:** Slack notifications are automatically summarized to provide executives with clear "Decision Support".
---
## 📖 Advanced Usage: High-Abstraction Governance
In an enterprise environment, GovAgent acts as your digital "Control Plane" for high-stakes workflows like healthcare claim processing.

### 1. Autonomous "Billing Director" Workflow
Bridge the gap between LLM reasoning and financial policy:
```python

import asyncio
from langchain_openai import ChatOpenAI
from govagent import ExecutiveAgent, Policy, HITLManager, SlackJudiciaryAdapter

async def run_governed_session():
    # Load Enterprise Policy (Article 9 Compliance)
    policy = Policy.from_yaml("policies/healthcare_ops_policy.yaml")
    
    # Initialize the Slack Judiciary (Article 14 Compliance)
    judiciary = SlackJudiciaryAdapter(
        bot_token="xoxb-...", 
        app_token="xapp-...", 
        channel_id="C12345"
    )
    judiciary.start()

    # The Executive Agent: Your digital 'Control Plane'
    agent = ExecutiveAgent(
        persona="Healthcare Finance Director",
        policy=policy,
        model_client=ChatOpenAI(model="gpt-4o"), # Auto-wrapped by v0.2.3 Adapter
        hitl_manager=HITLManager(adapter=judiciary)
    )

    # Task triggers cascading triage: Fiscal -> Policy -> Judiciary
    task = "Process claim #7742 for $1,250.00 for the outpatient procedure."
    report = await agent.execute(task)
    
    print(f"🏁 Session Status: {report.status}")
```
 
´### 2. The Cascading Triage Engine
The v0.2.3 core intercepts intent through three distinct layers of defense:

* **Stage 1:** Fiscal Guard: Blocks the action if the amount exceeds the max_per_transaction limit.
* **Stage 2:** Policy Guard: Validates the tool (e.g., authorize_claim_payment) against the approved manifest for the persona.
* **Stage 3:** Judiciary Guard: Escalates "High Risk" actions to Slack for synchronous human approval.

---

### 📊 Forensic Telemetry: Article 12 Readiness
Every session generates an immutable JSONL snapshot in /logs/audit_trail.jsonl.

```python

{
  "timestamp": "2026-05-06T12:24:25",
  "persona": "Healthcare Finance Director",
  "task": "Process claim #7742 for $1,250.00",
  "guards_evaluated": ["fiscal", "policy", "judiciary"],
  "decision": "Approved by Judiciary (Slack)",
  "metadata": {
    "tokens": 450,
    "cost_usd": 0.009,
    "intent": {"action": "authorize_claim_payment", "params": {"amount": 1250.0}}
  }
}

```

## 🗺️ Strategic Roadmap

### ✅ v0.2.3: Modular Enforcement (Current)
* **Cascading Triage:** Tiered guards to protect LLM budget and human attention.
* **Dynamic Extraction:** Automated parsing of claim metadata from conversation strings.
* **Forensic JSONL:** Ready-to-audit logs for Enterprise SOCs.

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
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool as langchain_tool
from govagent import ExecutiveAgent, Policy, HITLManager, SlackJudiciaryAdapter

@langchain_tool
async def healthcare_payment_tool(amount: float) -> str:
    """Authorizes payments for healthcare claims. Input: amount."""
    
    # 1. UNIVERSAL INTERCEPTOR (v0.2.3 Modular Guard)
    # This single call evaluates Fiscal limits, Policy rules, and triggers Slack Judiciary.
    # Execution physically raises a GovernanceViolation if any guard fails.
    await agent.evaluate(
        guards=["fiscal", "judiciary"],
        value=amount,
        intent={"action": "healthcare_payment_tool", "params": {"amount": amount}},
        reason=f"Processing healthcare disbursement of ${amount}"
    )

    # 2. Business logic proceeds ONLY if all guards pass
    return f"SUCCESS: Payment of ${amount} authorized and processed."

# Example Invocation
async def main():
    result = await healthcare_payment_tool.ainvoke({"amount": 1200.0})
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```
---
## ⚙️ Installation

GovAgent is designed to be lightweight and modular. You can install the core framework or include specific integrations as needed.

### 1. Core Installation (Lightweight)
Recommended for users building custom agents or those who only require the Judiciary and Policy layers.
```bash
pip install govagent
```
### 2. Full Integration (With LangChain)
Includes all dependencies required to run governed LangChain sessions, including the langchain_tool wrappers and OpenAI clients.

```bash
pip install "govagent[langchain]"
```
### 3. Development Installation
If you are contributing to the framework or running the examples in this repository, install in editable mode:

```bash
git clone [https://github.com/thekakodkar/govagent.git](https://github.com/thekakodkar/govagent.git)
cd govagent
pip install -e ".[langchain]"

```
### 🚀 Quick Setup
Ensure your .env file is configured with the necessary tokens for the Judiciary Layer to function:

Code snippet
# Slack Credentials (Socket Mode)
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_APP_TOKEN=xapp-your-token
SLACK_CHANNEL_ID=C12345678

# Model Provider
OPENAI_API_KEY=sk-your-key

---
**"Governance is not a constraint; it is the catalyst for enterprise AI adoption."**
---
### Author Stamp
*   **Framework:** GovAgent v0.2.3 (Stable)
*   **Status:** Active / Open-Source Standard
*   **Compliance:** Designed for Enterprise-Grade Accountability
