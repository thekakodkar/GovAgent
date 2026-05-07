## govAgent: Enterprise-Grade AI Governance Framework

**The Governance-First Framework for Production-Grade Autonomous Systems.**

GovAgent provides a high-abstraction **Control Plane** for agentic AI. With a clear chain of accountability, this lightweight framework helps move autonomous systems from experimental sandboxes into governed, production environments.

<img width="1097" height="479" alt="ImagegoV" src="https://github.com/user-attachments/assets/4e05d505-63d6-4f14-9475-cc00b4f20d73" />

The v0.3.0 "Institutional Scaling" update transforms the framework into an automated gatekeeper, introducing thread-safe context management and declarative tool protection, allowing for the rapid deployment of governed "AI Swarms."

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

## 🛠️ Key Capabilities (v0.3.0)
*   **🛡️ Invisible Governance:** Declarative tool protection via the @tool decorator. Guards are injected automatically at runtime.
*   **🏢 Institutional Bootstrap:** Single-line initialization (ExecutiveAgent.bootstrap()) for rapid enterprise setup.
*   **🧵 Thread-Safe Scaling:** contextvars support enables multi-agent swarms without identity or budget leakage.
*   **🛑 Terminal Integrity:** Built-in "Hard Stop" logic prevents infinite reasoning loops after a rejection or fiscal breach.

---
## 📖 Advanced Usage: High-Abstraction Governance
In an enterprise environment, GovAgent acts as your digital "Control Plane" for high-stakes workflows like healthcare claim processing.

### 1. Define a Governed tool (Pillars 2 & 3)
```python
from govagent import tool

@tool(name="execute_financial_transaction", guards=["fiscal", "judiciary"], risk_level="high")
async def process_payment(amount: float, reference_id: str):
    """Executes a financial disbursement. Injected guards handle Pillar 2 & 3 automatically."""
    return f"SUCCESS: Paid ${amount} for Ref: {reference_id}"
```
### 2. The Institutional session (Pillars 1 & 4)
```python
import asyncio
from langchain_openai import ChatOpenAI
from govagent import ExecutiveAgent

async def run_governed_session():
    # Load Policy (Pillar 1) & Initialize Session
    agent = ExecutiveAgent.bootstrap(
        policy_path="policies/finance_policy.yaml",
        llm=ChatOpenAI(model="gpt-4o"),
        slack_channel="C12345" # Judiciary Link
    )

    # Telemetry (Pillar 4) is captured automatically during execution
    task = "Process a reimbursement for claim #882 in the amount of $1200."
    report = await agent.execute(task)
    
    print(f"🏁 Session Status: {report.status}")
```

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

### ✅ v0.3.0: Institutional Scaling (Current)
* **Automated Interception:** Declarative tool protection via decorators.
* **Context Management:** Thread-safe multi-agent session tracking.
* **Terminal Logic:** Loop-breaking safety for judiciary rejections.

### 🚀 v0.4.0: The "Sovereign Swarm" (Next)
* **Recursive Fiscal Ceilings:** Multi-agent TCO (Total Cost of Operation) guardrails.
* **Cloud Exporters:** Native integration for AWS CloudWatch and Azure Monitor.
* **Dynamic Budgeting:** Real-time API pricing for penny-accurate cost tracking.---
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
