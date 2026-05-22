## govAgent: Enterprise-Grade AI Governance Framework

**The Governance-First Framework for Production-Grade Autonomous Systems.**

GovAgent provides a high-abstraction **Control Plane** for agentic AI. With a clear chain of accountability, this lightweight framework helps move autonomous systems from experimental sandboxes into governed, production environments.
<img width="1476" height="866" alt="govAgent drawio" src="https://github.com/user-attachments/assets/e8088984-b2e6-48c3-a7ad-02b99a1dd241" />
The **v0.6.0** "Self-Healing Swarm" release introduces automated, data-driven policy calibration and federated cross-organization audit trails, enabling multi-agent swarms to run safely across diverse enterprise infrastructures with rigorous institutional oversight.

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

## 🏗️ Core Pillars: The v0.6.0 Sovereign Architecture
GovAgent utilizes a highly modular package structure to enforce strict "Separation of Duties" across any application vertical:

1.  **`govagent.context` (The State):** Manages thread-safe session isolation and Recursive TCO cost tracking across decentralized swarms.

2.  **`govagent.registry` (The Law):** A centralized, type-safe ledger where all tools must be explicitly legislated before execution to eliminate "Shadow IT".

3.  **`govagent.telemetry` (The Evidence):** Forensic-grade audit trails dispatched to multi-cloud SOC sinks (AWS/Azure) or segregated multi-tenant paths.

4.  **`govagent.guards` (The Enforcement):** Real-time Stage 0 (Privacy), Stage 1 (Semantic), and Stage 2 (Fiscal) circuit breakers.

5.  **`govagent.governance.meta` (The Optimization):** Self-healing anomaly loop parsing that safely mitigates workflow friction without manual operator interference.

---

## ⚖️ Comparative Analysis: Governance Superiority

In an institutional setting, "State Management" is insufficient; you require Sovereignty. GovAgent v0.6.0 is engineered horizontally to transform "Black Box" multi-agent workflows into transparent, compliance-vetted execution lifecycles across all commercial sectors.

| Feature | **GovAgent v0.6.0** | LangGraph | CrewAI |
| :--- | :--- | :--- | :--- |
| **Architectural Scope** | ✅ **Modular Control Plane** | ⚠️ Local State Graph | ❌ Role Play Swarm |
| **State Management** | ✅ **Isolated Fiscal Ledger** | ⚠️ Shared Thread State | ❌ Global context |
| **Tool Legislation** | ✅ **Global Registry Singleton** | ⚠️ Function Decorators | ❌ String-based Tools |
| **Forensic Audit** | ✅ **Federated Cross-Org Trails** | ❌ Per-run only | ❌ Console Prints |
| **Policy Calibration** | ✅ **Self-Healing Optimization** | ❌ Hardcoded Boundaries | ❌ Manual Intervention |
| **Regulatory Status** | ✅ **EU AI Act Regulation Ready** | ❌ Experimental | ❌ Experimental |

> **Strategic Directive:** While traditional frameworks focus heavily on graph-based execution paths or simple task delegation, GovAgent v0.6.0 operates as the Sovereign Governance Infrastructure. It ensures that every action across an autonomous network is centrally legislated, evaluated by isolated quantitative guards, and forensically recorded for cross-enterprise auditing..

---


## ⚖️ Regulatory Compliance: EU AI Act (Regulation 2024/1689)

GovAgent satisfies key mandates for **High-Risk AI Systems**:

* **Article 9: Risk Management & Privacy:** Automated Stage 0 PII redaction and proactive semantic intent interception.
* **Article 12: Record-Keeping & Traceability:** Immutable Forensic Telemetry with local failover (DLQ) for 100% audit continuity.
* **Article 14: Human Oversight:** Physical gating of high-risk actions through Federated M-of-N Consensus.
    
---

## 🛠️ Key Capabilities (v0.6.0 Production Standard)
* **🔄 Automated Policy Tuning:** The MetaGovernor scans forensic logs for systemic circuit-breaker friction and generates non-hallucinated POLICY_AMENDMENT_PROPOSAL structures for executive sign-off.
* **⚖️ Role-Weighted Quorum Board:** Enforces role-based authority scoring (e.g., C-Suite: 3.0, Director: 2.0, Lead: 1.0) and assigns actions to escalating risk tiers (Operational, High, Critical) to eliminate identity cloning.
* **📡 Cross-Org Telemetry:** Universal FederatedTelemetryExporter routing engine that isolates forensic records into secure tenant-bounded payloads for distinct corporate nodes or partners.
* **💸 Recursive Fiscal Ceilings:** Aggregated Total Cost of Operation (TCO) tracking across multi-agent boundaries to completely prevent budget fragmentation.
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
### 2. The Institutional session (v0.6.0 standard)

```python
import asyncio
from govagent import ExecutiveAgent

async def run_governed_swarm():
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
    print(f"🏁 Swarm Status: {report.status.upper()}")
    print(f"💰 Recursive Swarm TCO: ${report.recursive_tco_usd:.4f}")
```
---

### 📊 Forensic Telemetry: Article 12 Readiness
Every session generates an immutable snapshot routed directly to external cloud SOC sinks, local repositories, or isolated cross-org tenants.

```python

{
  "timestamp": "2026-05-22T13:00:00Z",
  "trace_id": "exec-882-9934",
  "parent_trace_id": "director-main-771", 
  "organization_id": "ENTERPRISE_TENANT_ALPHA",
  "agent_id": "SovereignControlAgent",
  "task_input": "Execute cross-border logistics audit",
  "status": "SUCCESS: TRANSACTION FINALIZED",
  "guards_evaluated": ["privacy", "semantic", "fiscal", "judiciary"],
  "metrics": {
    "tokens": 850,
    "individual_cost_usd": 0.012,
    "recursive_tco_usd": 0.045
  },
  "judiciary_audit": {
    "compiled_signatures": [
      {"voter_id": "U111", "voter_role": "Director", "decision": "APPROVED"},
      {"voter_id": "U222", "voter_role": "Lead", "decision": "APPROVED"}
    ],
    "final_status": "✅ QUORUM MET: Authorized at a weight of 3.0/2.5"
  }
}
```

## 🗺️ Strategic Roadmap

### ✅ v0.5.0 / v0.5.1: The Federated Judiciary (Current)
* **M-of-N Consensus:** Multi-party board approvals.
* **Semantic Alignment:** Vector-based qualitative guardrails.
* **Modular Namespace Migration:** Decoupled context, registry, and telemetry sub-packages.

### ✅ v0.6.0: The Self-Healing Swarm (GA Baseline Release)
* **Automated Policy Tuning:** AI-assisted guardrail calibration and friction log mitigation.
* **Cross-Org Telemetry:** Horizontal, vendor-agnostic multi-tenant forensic routing logs.
* **Role-Weighted Oversight:** Cumulative weight tallies and anti-cloning security matrices.

### 🚀 v0.7.0: The Decentralized Mesh (Next)
* **Autonomous Cross-Swarm Delegation:** Secure handshakes between entirely disconnected agent meshes.
* **Zero-Knowledge Privacy Guards:** Advanced cryptographic parsing for Stage 0 inputs.

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
*   **Framework: GovAgent v0.6.0 (Federated)
*   **Compliance: Designed for Article 9, 12, and 14 Accountability
*   **Status:** Active / Open-Source Standard
