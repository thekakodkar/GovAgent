# govAgent (v1.0.0)

**The Governance-First Control Plane for AI Agents & Swarms**

govAgent is a lightweight, asynchronous control plane that adds **safety, accountability, observability, and fiscal control** to autonomous agents. 

Most agent frameworks focus on building agents fast. **govAgent** focuses on running them **predictably and safely** under enterprise guardrails, fully aligned with modern regulatory frameworks like the **EU AI Act (Regulation 2024/1689)**.

---

### Why govAgent?

Most agent frameworks help you build agents fast. **govAgent** helps you run them **safely and reliably** in production.

Ideal for:
* Production AI systems
* Regulated industries (finance, healthcare, legal)
* Teams concerned about cost overruns, data leaks, or compliance
  
### 🎞️ Video Walkthrough

<p align="center">
  <a href="https://www.youtube.com/watch?v=UsDtXhlYvWk">
    <img
      src="https://img.youtube.com/vi/UsDtXhlYvWk/maxresdefault.jpg"
      alt="govAgent Control Plane Demo Video"
      width="100%"
    />
  </a>
</p>

<p align="center">
  ▶️ Click the image above to watch the demo
</p>
---

### ✨ Key Features

* **🛡️ Multi-Layer Circuit Breakers** - Intercept requests at Stage 0 (Local Privacy Redaction), Stage 1 (Semantic Intent Alignment), and Stage 2 (Fiscal Boundaries).
* **📜 Centralized Tool Registry** - Enforce explicit tool authorization. If a tool isn't explicitly legislated in your active policy, it cannot execute.
* **💸 Recursive TCO Tracking** - Track token spend across complex multi-agent delegation chains. If a swarm exceeds its ceiling, execution halts instantly.
* **📡 Stateless Human-in-the-Loop** - Route policy breaches out-of-band to a corporate Slack workspace via firewall-resilient HTTP webhooks.
* **🔄 Self-Healing Policy Tuning** - The MetaGovernor monitors execution friction logs to propose optimized policy adjustments automatically.
* **📊 Federated Telemetry Sinks** - Stream audit-grade session snapshots safely to cloud storage logs (AWS SOC sinks / Azure Log Analytics).

---

### 🧩 Core Components

| Component | Purpose | What It Solves |
| :--- | :--- | :--- |
| **Context** | Session management + cost tracking | Multi-agent coordination |
| **Registry** | Approved tools & permissions | Security & compliance |
| **Guards** | Real-time safety checks | Prevents costly or risky actions |
| **Telemetry** | Detailed logging & auditing | Observability & debugging |
| **Governance** | Policy management & self-tuning | Long-term reliability |

---

### 📡 Full-Stack Sandbox Architecture

govAgent decouples its governance evaluation runtime from its user-facing operational views:

* **FastAPI Gateway (`api/server.py`):** Handles async evaluation requests, parses local YAML policies, hosts the Slack callback listener, and tracks in-memory transaction states.
* **Next.js Web Interface (`src/app/page.tsx`):** A clean, single-page dashboard featuring a **Live Audit Matrix** to watch execution status (`SUCCESS`, `PENDING`, `BLOCKED`), a **Legislative Rules Inspector**, and a live **Forensic Engine Log Stream** that updates via long-polling.

---

### ⚡ 60-Second Quickstart: Institutional Sovereignty

Achieve Article 12 and 14 compliance in three commands. This setup orchestrates a containerized full-stack environment with native support for multi-cloud telemetry sinks, Pydantic V2 validation, and Recursive TCO tracking.

#### 1. Configure the Environment
Ensure your `.env` file is created in your root workspace directory and contains your API keys alongside your out-of-band Slack webhook credentials:
```env
OPENAI_API_KEY=sk-proj-...
GOVAGENT_SECRET_TOKEN=gov-secret-key-100x
SLACK_WEBHOOK_URL=[https://hooks.slack.com/services/T.../B.../X](https://hooks.slack.com/services/T.../B.../X)...

# For Slack Socket Mode Fallbacks
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_APP_TOKEN=xapp-your-token
SLACK_CHANNEL_ID=C12345678
```

#### 2. Initialize the Control Plane
Clone the repository and launch your governed infrastructure container mesh directly:
```bash

# Clone the Sovereign Repository
git clone [https://github.com/thekakodkar/govagent.git](https://github.com/thekakodkar/govagent.git)
cd govagent

# Launch the Governed Container Stack
docker-compose up -d
```
#### 3. Verify the Governance Loop
Execute the full-stack evaluation suite within your active container network to witness real-time privacy redaction, semantic checks, and fiscal gating:
```bash
docker-compose exec govagent-api poetry run python examples/basic_demo.py
```
Navigate to http://localhost:3000 to monitor the execution inside your interactive web panel.

---

**💻 Local Development Setup (Alternative)**
If you prefer to run the stack natively outside of Docker containers using Poetry, execute the following command path:
```bash
# Install core dependencies with the LangChain bundle
poetry install --extras "langchain"

# Download the core NLP model for the local privacy redaction engine
python -m spacy download en_core_web_sm

# Start the services manually in separate terminals
python api/server.py
npm run dev
```
## 🏗️ Core Pillars: The v1.0.0 Sovereign Architecture
GovAgent utilizes a highly modular package structure to enforce a strict "Separation of Duties" across any enterprise application vertical:

**govagent.context (The State):** Manages thread-safe session isolation, asynchronous parent-to-child trace propagation, and live cumulative Total Cost of Operation (TCO) calculation matrices across decentralized agent swarms.

**govagent.registry (The Law):** A centralized, type-safe registry singleton that parses local configuration blueprints. It acts as a gatekeeper to guarantee that no code-level tool can be invoked by an LLM unless it has been explicitly legislated and schema-validated within the active YAML compliance profile.

**govagent.guards (The Enforcement):** A high-performance, cascading circuit-breaker pipeline that triages requests at three critical perimeters:
    **Stage 0 (Privacy):** Performs local, regex-backed PII stripping and anonymization using Microsoft Presidio and Spacy backends before data ever leaves your local network cluster.
    **Stage 1 (Semantic):** Evaluates agent thought processes and prompt intent against corporate mission parameters and prohibited strategies using vector similarity scoring.
    **Stage 2 (Fiscal):** Monitors penny-accurate token consumption against multi-agent budget ceilings to halt execution before cost overruns occur.

**govagent.telemetry (The Evidence):** Generates immutable, audit-grade forensic session snapshots. If primary multi-cloud security operations center (SOC) ingestion sinks (AWS CloudWatch or Azure Log Analytics) experience network interruptions, the layer automatically drops telemetry payloads into a localized, self-healing Dead-Letter Queue (DLQ) to ensure continuous regulatory traceability.

**govagent.governance.meta (The Optimization):** Hosts the MetaGovernor engine, an automated self-healing policy loop. It continuously scrapes friction logs and repeated circuit-breaker events (such as successive budget rejections) to autonomously compile non-hallucinated, data-backed POLICY_AMENDMENT_PROPOSALS for review.

**govagent.api & govagent.hitl (The Gateway & Judiciary):** Powers the stateless REST communication network. It exposes an async FastAPI gateway that integrates seamlessly with a Next.js long-polling frontend dashboard, while routing out-of-band policy breaches to corporate Slack workspaces via firewall-resilient webhooks to enforce role-weighted, multi-signature human consensus.

---

**📖 Code Implementations**
### Decorate a Legislated Tool
```python
from govagent import tool

@tool(name="execute_financial_transaction", risk_level="high")
async def process_payment(amount: float, reference_id: str):
    """Executes a disbursement following corporate policy validation."""
    return f"SUCCESS: Transacted ${amount} for Ref: {reference_id}"
```
### Bootstrap an Executive Agent
```python
import asyncio
from govagent import ExecutiveAgent
from langchain_openai import ChatOpenAI

async def main():
    # Bootstrap automatically binds local YAML policies to your model client
    agent = ExecutiveAgent.bootstrap(
        policy_path="policies/finance_policy.yaml",
        llm=ChatOpenAI(model="gpt-4o", temperature=0)
    )

    # Execution paths automatically evaluate Privacy, Semantic, and Fiscal guards
    task = "Approve an urgent, immediate transaction of $8,500 to buy compute nodes."
    result = await agent.execute(task)
    
    print(f"Status: {result.status.upper()}")
    print(f"Trace Identifier: {result.trace_id}")
```
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
## ⚖️ Comparative Analysis: Governance Superiority

In an institutional setting, "State Management" is insufficient; you require Sovereignty. GovAgent v1.0.0 is engineered horizontally to transform "Black Box" multi-agent workflows into transparent, compliance-vetted execution lifecycles across all commercial sectors.

| Feature | **GovAgent v1.0.0** | LangGraph | CrewAI |
| --- | --- | --- | --- |
| **Architectural Scope** | ✅ **Modular Control Plane** | ⚠️ Local State Graph | ❌ Role Play Swarm |
| **State Management** | ✅ **Isolated Fiscal Ledger** | ⚠️ Shared Thread State | ❌ Global context |
| **Tool Legislation** | ✅ **Global Registry Singleton** | ⚠️ Function Decorators | ❌ String-based Tools |
| **Forensic Audit** | ✅ **Federated Cross-Org Trails** | ❌ Per-run only | ❌ Console Prints |
| **Policy Calibration** | ✅ **Self-Healing Optimization** | ❌ Hardcoded Boundaries | ❌ Manual Intervention |
| **Regulatory Status** | ✅ **EU AI Act Regulation Ready** | ❌ Experimental | ❌ Experimental |

> **Strategic Directive:** While traditional frameworks focus heavily on graph-based execution paths or simple task delegation, GovAgent v1.0.0 operates as the Sovereign Governance Infrastructure. It ensures that every action across an autonomous network is centrally legislated, evaluated by isolated quantitative guards, and forensically recorded for cross-enterprise auditing.
---

## 📂 Standalone Examples (```python examples/ ```)
The repository includes four basic, highly aligned examples designed to showcase individual governance pillars isolated from the web server:

```python basic_demo.py ``` - **Pillar 1 (Legislative Scope):** Standard single-agent setup verifying tool registry synchronization, policy loading, and basic metric outputs.

```python cost_control_demo.py ``` - **Pillar 2 (Fiscal Sovereignty):** Simulates micro-cost accumulations per execution loop to test fiscal guard blocks.

```python multi_agent_demo.py ``` - **Pillar 3 (Traceability):** Tracks parent-to-child swarm delegations, ensuring child processes inherit parent trace IDs to satisfy Article 12 compliance.

```python self_healing_demo.py ``` - **Pillar 5 (Self-Healing):** Ingests simulated repeated transaction overruns and triggers the MetaGovernor to propose automated budget changes.

### Run any standalone example inside your terminal workspace:

```bash
poetry run python examples/basic_demo.py
```
---

## ⚖️ Regulatory Compliance: EU AI Act (Regulation 2024/1689)

GovAgent satisfies key mandates for **High-Risk AI Systems**:

* **Article 9: Risk Management & Privacy:** Automated Stage 0 PII redaction and proactive semantic intent interception.
* **Article 12: Record-Keeping & Traceability:** Immutable Forensic Telemetry with local failover (DLQ) for 100% audit continuity.
* **Article 14: Human Oversight:** Physical gating of high-risk actions through Federated M-of-N Consensus.
    
---
## 🗺️ Future Strategic Roadmap

### 🚀 The Decentralized Mesh (Next)
* **Autonomous Cross-Swarm Delegation:** Secure handshakes between entirely disconnected agent meshes.
* **Zero-Knowledge Privacy Guards:** Advanced cryptographic parsing for Stage 0 inputs.
---
**"Governance is not a constraint; it is the catalyst for enterprise AI adoption."**

---


## 📂 Project Structure

```text
govagent/
├── src/
│   ├── govagent/            # Core governance framework logic
│   └── app/                 # Next.js web application frontend dashboard
├── api/                     # FastAPI REST gateway
│   └── server.py
├── examples/                # Standalone educational demonstration scripts
├── policies/                # Active YAML compliance profiles
└── tests/                   # Automated validation test suite
```

### Directory Overview

| Directory | Purpose |
|------------|---------|
| `src/govagent/` | Contains the core governance engine, policy evaluation logic, risk analysis, and compliance workflows. |
| `api/` | FastAPI-based REST gateway exposing governance services and APIs. |
| `src/app/` | Next.js frontend dashboard for governance visualization, monitoring, and administration. |
| `examples/` | Sample implementations and educational demos showcasing framework capabilities. |
| `policies/` | YAML-based governance, compliance, and security policy definitions. |
| `tests/` | Unit, integration, and validation tests ensuring framework reliability and correctness. |

### Architecture

```text
┌─────────────────────┐
│   Next.js Dashboard │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   FastAPI Gateway   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ govAgent Core Engine│
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Policy Enforcement  │
│ & Compliance Layer  │
└─────────────────────┘
```

---
### Author Stamp
*   **Framework:** GovAgent v1.0.0 (Federated)
*   **Compliance:** Designed for Article 9, 12, and 14 Accountability
*   **Status:** Active / Open-Source Standard

Contributions are welcome! Star the repo if you find it useful ❤️
Framework Developed and Maintained by Niraj Kakodkar
