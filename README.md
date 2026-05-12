## govAgent: Enterprise-Grade AI Governance Framework

**The Governance-First Framework for Production-Grade Autonomous Systems.**

GovAgent provides a high-abstraction **Control Plane** for agentic AI. With a clear chain of accountability, this lightweight framework helps move autonomous systems from experimental sandboxes into governed, production environments.

<img width="769" height="336" alt="ImagegoV" src="https://github.com/user-attachments/assets/3690aff2-68c7-4f9e-90eb-c73389809ac1" />

The **v0.5.0** "Federated Judiciary" update introduces M-of-N Multi-Signature Approval and Vector-Based Semantic Guardrails, allowing for the deployment of ultra-high-risk agent swarms with absolute institutional consensus and self-healing forensic audit trails.

---

## ⚡ 60-Second Quickstart: Institutional Sovereignty
Achieve Article 12 and 14 compliance in three commands. This setup orchestrates a containerized environment with native support for AWS CloudWatch, Pydantic V2 validation, and Recursive TCO tracking.

1. **Initialize the Control Plane**
Ensure your .env file contains your OPENAI_API_KEY and Slack credentials in the root directory.

```bash
# Clone the Sovereign Repository
git clone https://github.com/thekakodkar/govagent.git
cd govagent

# Launch the Governed Container Stack
docker-compose up -d
```
2. **Verify the Governance Loop**
Execute the Institutional Demo to witness real-time PII redaction and fiscal gating.

```bash
docker-compose exec govagent-demo python examples/demo.py
```
---

## 🏗️ Core Pillars: The Chain of Accountability
GovAgent replaces "Black Box" reasoning with a transparent, governed loop:

1.  **Policy (The Law):** Declarative boundaries and "Rules of Engagement" defined by stakeholders in `policy.yaml`.
2.  **Guards (The Enforcement):** Real-time circuit breakers that intercept agent intent *before* API execution to prevent budget or security breaches.
3.  **HITL (The Judiciary):** **Synchronous** Human-in-the-Loop escalation. High-risk actions are physically blocked until an explicit "Approve" or "Reject" signal is received via Slack or CLI.
4.  **Telemetry (The Evidence):** Forensic-grade audit trails providing an immutable ledger of compliance and real-world ROI.

---

## ⚖️ Comparative Analysis: Governance Superiority

In an institutional setting, "State Management" is insufficient—you need **Sovereignty**. GovAgent is engineered to meet the specific requirements of Big 4 audit and compliance, transforming "Black Box" reasoning into a transparent, governed lifecycle.

| Feature | **GovAgent** | LangGraph | CrewAI |
| :--- | :--- | :--- | :--- |
| **Policy Enforcement** | ✅ **Deterministic & Semantic** | ⚠️ Partial / Manual | ❌ None |
| **Federated Judiciary** | ✅ **M-of-N Consesus** | ⚠️ Local / LangSmith | ❌ Console Logs |
| **Human Approval Gates** | ✅ **Synchronous & Blocking** | ⚠️ Manual Interrupts | ❌ Optional |
| **Forensic Resilience** | ✅ **Self Healing Local DLQ** | ❌ Per-run only | ❌ None |
| **Regulatory Status** | ✅ **EU AI Act Article 9,12,14 Ready** | ❌ Experimental | ❌ Experimental |

> **Strategic Directive:** While LangGraph and CrewAI focus on agent capability and roleplay, GovAgent operates as the **Institutional Control Plane** that ensures every action is legislated, evaluated, and forensically recorded.

---


## ⚖️ Regulatory Compliance: EU AI Act (Regulation 2024/1689)

GovAgent satisfies key mandates for **High-Risk AI Systems**:

* **Article 9: Risk Management & Privacy:** Automated Stage 0 PII redaction and proactive semantic intent interception.
* **Article 12: Record-Keeping & Traceability:** Immutable Forensic Telemetry with local failover (DLQ) for 100% audit continuity.
* **Article 14: Human Oversight:** Physical gating of high-risk actions through Federated M-of-N Consensus.
    
---

## 🛠️ Key Capabilities (v0.5.0)
* **⚖️Federated M-of-N Quorum:** Require $M$ approvals from a board of $N$ reviewers before high-risk execution.
* **🧠 Semantic Alignment Judge:** Vector-based Similarity Checks to ensure agent reasoning adheres to qualitative "Mission Statements".
* **💸 Recursive Fiscal Ceilings:** Aggregate TCO tracking across parent and sub-agents to prevent budget fragmentation.
* **📡 Self-Healing Telemetry:** Automated local buffering (DLQ) if Cloud SOC sinks (AWS/Azure) are unreachable.

---
## 📖 Advanced Usage: High-Abstraction Governance
In an enterprise environment, GovAgent acts as your digital "Control Plane" for high-stakes workflows like healthcare claim processing.

### 1. Define a Legislated Tool (Pillars 2 & 3)
```python
from govagent import tool

@tool(name="execute_financial_transaction", guards=["fiscal", "judiciary"], risk_level="high")
async def process_payment(amount: float, reference_id: str):
    """
    Executes a financial disbursement. 
    Injected guards handle Recursive TCO and M-of-N Judiciary gating automatically.
    """
    return f"SUCCESS: Paid ${amount} for Ref: {reference_id}"
```
### 2. The Institutional session (v0.5.0 standard)

```python
import asyncio
from govagent import ExecutiveAgent

async def run_governed_session():
    # 1. Bootstrap: Loads Policy & Federated Judiciary Adapters
    agent = ExecutiveAgent.bootstrap(
        policy_path="policies/finance_policy.yaml",
        llm=ChatOpenAI(model="gpt-4o"),
        slack_channel="C082PBLPN9X" # Federated Slack Courtroom
    )

    # 2. Execution (Stage 0 Privacy, Stage 1 Semantic Alignment, Stage 2 Fiscal)
    task = "Process a reimbursement for Marko P at 123 Main St ($1200.00)."
    report = await agent.execute(task)
    
    # 3. Institutional Audit Report (Article 12)
    print(f"🏁 Session Status: {report.status.upper()}")
    print(f"💰 Recursive Swarm TCO: ${report.recursive_tco_usd:.4f}")
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

### ✅ v0.5.0: The Federated Judiciary (Current)
* **M-of-N Consensus:** Multi-party board approvals.
* **Semantic Alignment:** Vector-based qualitative guardrails.
* **Self-Healing Telemetry:** Local DLQ for forensic resilience.

### 🚀 v0.6.0: The Self-Healing Swarm (Next)
* **Automated Policy Tuning:** AI-assisted guardrail calibration.
* **Cross-Org Telemetry:** Federated audit trails across different corporate entities.---

## ⚙️ Installation

GovAgent is designed to be lightweight and modular. You can install the core framework or include specific integrations as needed.

### 1. Core Installation (Lightweight)
Recommended for users building custom agents or those who only require the Judiciary and Policy layers.
```bash
pip install govagent
```
### 2. Full Integration (With LangChain & PII Protection)
Includes all dependencies required to run governed LangChain sessions, including the langchain_tool wrappers and OpenAI clients.

```bash
pip install "govagent[full]"
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
*   **Framework: GovAgent v0.5.0 (Federated)
*   **Compliance: Designed for Article 9, 12, and 14 Accountability
*   **Status:** Active / Open-Source Standard