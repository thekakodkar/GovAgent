## govAgent: Enterprise-Grade AI Governance Framework

**The Governance-First Framework for Production-Grade Autonomous Systems.**

GovAgent provides a high-abstraction **Control Plane** for agentic AI. With a clear chain of accountability, this lightweight framework helps move autonomous systems from experimental sandboxes into governed, production environments.

<img width="769" height="336" alt="ImagegoV" src="https://github.com/user-attachments/assets/3690aff2-68c7-4f9e-90eb-c73389809ac1" />

The **v0.4.0 "Sovereign Swarm"** update introduces **Recursive Fiscal Control** and **Cloud SOC Integration**, allowing for the deployment of multi-agent swarms with penny-accurate cost tracking and immutable forensic audit trails.

---

## 🏗️ Core Pillars: The Chain of Accountability
GovAgent replaces "Black Box" reasoning with a transparent, governed loop:

1.  **Policy (The Law):** Declarative boundaries and "Rules of Engagement" defined by stakeholders in `policy.yaml`.
2.  **Guards (The Enforcement):** Real-time circuit breakers that intercept agent intent *before* API execution to prevent budget or security breaches.
3.  **HITL (The Judiciary):** **Synchronous** Human-in-the-Loop escalation. High-risk actions are physically blocked until an explicit "Approve" or "Reject" signal is received via Slack or CLI.
4.  **Telemetry (The Evidence):** Forensic-grade audit trails providing an immutable ledger of compliance and real-world ROI.

---

## ⚖️ Regulatory Compliance: EU AI Act (Regulation 2024/1689)

GovAgent satisfies key transparency and oversight mandates for **High-Risk AI Systems**:

* **Article 9: Risk Management & Privacy** Automated PII redaction (Stage 0) and policy-driven intent interception.
* **Article 12: Record-Keeping & Traceability** Immutable **Forensic Telemetry** with native cloud exporters and recursive `parent_trace_id` tracking.
* **Article 14: Human Oversight** Physical gating of high-risk actions through synchronous human authorization.
    
---

## 🛠️ Key Capabilities (v0.4.0)
* **💸 Recursive Fiscal Ceilings:** Aggregate TCO (Total Cost of Operation) tracking across parent and sub-agents to prevent budget fragmentation.
* **☁️ Cloud-Native SOC:** Native telemetry exporters for **AWS CloudWatch** and **Azure Monitor**.
* **🛡️ Article 9 Privacy Guard:** Stage 0 PII scrubbing before tasks reach the LLM.
* **📐 Type-Safe Intent:** Pydantic-hardened tool parameters for deterministic integrity.

---
## 📖 Advanced Usage: High-Abstraction Governance
In an enterprise environment, GovAgent acts as your digital "Control Plane" for high-stakes workflows like healthcare claim processing.

### 1. Define a Governed tool (Pillars 2 & 3)
```python
from govagent import tool

@tool(name="execute_financial_transaction", guards=["fiscal", "judiciary"], risk_level="high")
async def process_payment(amount: float, reference_id: str):
    """
    Executes a financial disbursement. 
    Injected guards handle Recursive TCO and Judiciary gating automatically.
    """
    return f"SUCCESS: Paid ${amount} for Ref: {reference_id}"
```
### 2. The Institutional session (Pillars 1, 4 & Cloud SOC)
```python
import asyncio
import os
from langchain_openai import ChatOpenAI
from govagent import ExecutiveAgent
from govagent.exporters.cloudwatch import CloudWatchExporter

async def run_governed_session():
    # 1. Load Policy (Pillar 1) & Initialize Session
    agent = ExecutiveAgent.bootstrap(
        policy_path="policies/finance_policy.yaml",
        llm=ChatOpenAI(model="gpt-4o"),
        slack_channel="C12345" # Synchronous Judiciary Link
    )

    # 2. Enroll Cloud SOC (Pillar 4 - Phase 3)
    # Dispatches forensic evidence to AWS CloudWatch in real-time
    agent.telemetry.add_exporter(CloudWatchExporter(log_group="/aws/govagent/audit"))

    # 3. Execution (Stage 0 Privacy & Stage 2 Fiscal)
    task = "Process a reimbursement for John Doe in the amount of $1200."
    report = await agent.execute(task)
    
    # 4. Institutional Audit Report
    print(f"🏁 Session Status: {report.status.upper()}")
    print(f"💰 Recursive Swarm TCO: ${report.recursive_tco_usd:.4f}")
    print(f"🆔 Global Trace ID: {report.trace_id}")
```
---

### 📊 Forensic Telemetry: Article 12 Readiness
Every session generates an immutable snapshot dispatched to your enrolled cloud SOC or stored locally in /logs/audit_trail.jsonl.

```python

{
  "timestamp": "2026-05-07T15:30:00Z",
  "trace_id": "exec-882-9934",
  "parent_trace_id": "director-main-771", 
  "persona": "Healthcare Finance Director",
  "task": "Process claim #882 for $1200.00",
  "status": "SUCCESS: TRANSACTION FINALIZED",
  "guards_evaluated": ["privacy", "fiscal", "policy", "judiciary"],
  "metrics": {
    "tokens": 850,
    "individual_cost_usd": 0.012,
    "recursive_tco_usd": 0.045,
    "pii_entities_redacted": 2
  },
  "judiciary_audit": {
    "approver": "U12345 (Slack)",
    "decision": "APPROVED",
    "timestamp": "2026-05-07T15:28:45Z"
  }
}

```

## 🗺️ Strategic Roadmap

### ✅ v0.4.0: The Sovereign Swarm (Current)
* **Cloud Exporters:** AWS/Azure telemetry sinks.
* **Recursive TCO:** Shared fiscal context for multi-agent swarms.
* **Privacy Guard:** Stage 0 PII redaction.

### 🚀 v0.5.0: The Federated Judiciary (Next)
* **Multi-Party Approval:** M-of-N consensus for ultra-high-risk financial moves.
* **Semantic Policy Alignment:** Vector-based guardrails for qualitative boundaries.
* **Self-Healing Telemetry:** Automated retry logic for failed cloud SOC dispatches.
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
### Slack Credentials (Socket Mode)
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_APP_TOKEN=xapp-your-token
SLACK_CHANNEL_ID=C12345678

### Model Provider
OPENAI_API_KEY=sk-your-key

---
**"Governance is not a constraint; it is the catalyst for enterprise AI adoption."**
---
### Author Stamp
*   **Framework:** GovAgent v0.4.0 (Stable)
*   **Status:** Active / Open-Source Standard
*   **Compliance:** Designed for Enterprise-Grade Accountability
