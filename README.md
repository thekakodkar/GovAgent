## govAgent: Enterprise-Grade AI Governance Framework

**The Governance-First Framework for Production-Grade Autonomous Systems.**

GovAgent provides a high-abstraction **Control Plane** for agentic AI. With a clear chain of accountability, this lightweight framework helps move autonomous systems from experimental sandboxes into governed, production environments.

<img width="1097" height="479" alt="ImagegoV" src="https://github.com/user-attachments/assets/4e05d505-63d6-4f14-9475-cc00b4f20d73" />

The v0.2.3 Update transforms the framework into a proactive Triage Engine, introducing Modular Guards that intercept risky or expensive actions at the earliest possible stage, significantly increasing the Business ROI of autonomous sessions.

---

🚀 v0.2.3 New Feature: Zero-Config LangChain Integration
The v0.2.3 update introduces Dynamic Model Adaptation. You no longer need to manually wrap every tool; the ExecutiveAgent now automatically intercepts and governs standard LangChain clients.

```python

from langchain_openai import ChatOpenAI
from govagent.agent import ExecutiveAgent
from govagent.policy import Policy

# 1. Setup your standard LangChain client
llm = ChatOpenAI(model="gpt-4o")

# 2. GovAgent automatically wraps the model with a Governance Layer
agent = ExecutiveAgent(
    persona="Healthcare Billing Director",
    policy=Policy.from_yaml("healthcare_policy.yaml"),
    model_client=llm  # Auto-detected and Governed
)

# 3. Execute with built-in Triage (Fiscal -> Policy -> Judiciary)
report = await agent.execute("Process reimbursement for claim #882 for $1200.00")
```

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
*   **🛡️ Modular Guard Engine:** Cascading triage (fiscal -> policy -> judiciary) to stop invalid requests at zero token cost.
*   **🔗 Unified Interceptor:** A single agent.evaluate() call replaces complex manual branching logic in your tool definitions.
*   **🔌 Context-Aware Judiciary:** Slack notifications now include the specific guard that triggered the intervention (e.g., "Fiscal Ceiling Exceeded").
*   **⚠️ Declarative Tool Guarding:** Map safety protocols directly in Python code using the @tool(guards=["fiscal", "judiciary"]) decorator.
*   **📊 JSONL Telemetry:** Forensic-grade logs designed for Big 4 audit standards and enterprise log aggregators.
---
## 🗺️ Strategic Roadmap

### ✅ v0.2.3: Modular Enforcement (Current)
*   **Cascading Triage:** Tiered guards to protect LLM budget and human attention.
*   **Unified API:** The evaluate() method for minimalist tool integration.
*   **JSONL Export:** Forensic data readiness for enterprise SOCs.

### 🚀 v0.3.0: Institutional Scaling (Next)
*   **TCO Guardrails:** Total Cost of Operation limits for autonomous agent swarms.
*   **Multi-Agent Governance:** Shared policy enforcement across collaborative agent workflows.
*   **Cloud Native Exporters:** Direct telemetry streaming to AWS CloudWatch and Azure Monitor.
---

## 📖 Usage Example: Governed LangChain Tool (Simplified API)

The v0.2.3 API is designed for Minimalist Integration. You no longer need manual if/else checks for approval; the evaluate method handles the circuit-breaking logic automatically.

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
    llm = ChatOpenAI(model="gpt-4o")
    # Setup Agent, Policy, and HITLManager...
    agent = ExecutiveAgent(persona="Billing Director", model_client=llm, ...)
    
    result = await agent.execute("Pay claim #123 for $1200.00")
    print(result.status)
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
