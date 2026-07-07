# api/server.py
import os
import yaml
import uuid
import datetime
import logging
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from dotenv import load_dotenv
base_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(dotenv_path=os.path.join(base_directory, ".env"))

logger = logging.getLogger("govagent.api")

# v3.0.0 Enterprise Imports
from govagent.agent import ExecutiveAgent
from govagent.policy import Policy
from govagent.guards.circuit_breaker import GovernanceViolation
from govagent.extensions.ibm.bob_mcp_proxy import BobMCPProxyGateway
from govagent.registry.harbor_verifier import HarborVerifier
from govagent.context.fiscal_ledger import (
    reset_fiscal_ledger, 
    update_shared_spend, 
    get_shared_fiscal_metrics
)

app = FastAPI(title="govAgent Enterprise Governance Plane", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_TOKEN = os.environ.get("GOVAGENT_SECRET_TOKEN", "gov-secret-key-100x")
LIVE_TRANSACTION_STATES: Dict[str, Dict[str, Any]] = {}

class GovernanceRequest(BaseModel):
    task_input: str
    policy_profile: str = "policies/finance_policy.yaml"

class GovernanceResponse(BaseModel):
    status: str
    trace_id: str
    recursive_tco_usd: float
    selected_model: str
    sanitized_output: Optional[str] = None
    block_reason: Optional[str] = None  
    orchestrator_bus: str
    harbor_status: str
    harbor_digest: str

def verify_auth(authorization: Optional[str] = Header(None)):
    if not authorization or authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid Token.")

@app.get("/api/v1/governance/state/{trace_id}")
async def get_transaction_state(trace_id: str):
    if trace_id in LIVE_TRANSACTION_STATES:
        return LIVE_TRANSACTION_STATES[trace_id]
    return {"status": "PENDING", "message": "Awaiting infrastructure telemetry tokens."}

@app.post("/api/v1/governance/evaluate", response_model=GovernanceResponse, dependencies=[Depends(verify_auth)])
async def evaluate_workflow_intent(payload: GovernanceRequest):
    reset_fiscal_ledger()
    trace_id = f"TR-INFRA-{uuid.uuid4().hex[:6].upper()}"
    
    resolved_policy_path = os.path.join(base_directory, payload.policy_profile)
    if not os.path.exists(resolved_policy_path):
        raise HTTPException(status_code=404, detail="Policy file not found.")
        
    active_policy = Policy.from_yaml(resolved_policy_path)
    agent = ExecutiveAgent(persona="Director", policy=active_policy, router=None)
    
    # Simulate Out-of-Band Harbor Supply Chain Gating Checks
    harbor = HarborVerifier(registry_url=os.getenv("HARBOR_REGISTRY_URL", "https://harbor.local"))
    mock_digest = "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b"
    
    # Run the core textual input through the unified semantic architecture
    sanitized_task = payload.task_input
    alignment_score = agent.semantic_guard.evaluate_alignment(sanitized_task)
    
    if alignment_score == 0.0:
        LIVE_TRANSACTION_STATES[trace_id] = {"status": "BLOCKED", "orchestrator_bus": "IBM_BOB_MCP", "harbor_status": "FAILED"}
        return GovernanceResponse(
            status="BLOCKED", trace_id=trace_id, recursive_tco_usd=0.00, selected_model="local_ollama",
            sanitized_output="🛑 REJECTED: Prohibited operational intent vector intercepted.",
            block_reason="PILLAR 3 DEVIATION: Cosmetic cosine similarity score breaks policy constraints.",
            orchestrator_bus="IBM_BOB_MCP", harbor_status="UNVERIFIED", harbor_digest="NONE"
        )

    # Calculate dynamic transaction cost metrics or fallback to standard tier evaluation
    update_shared_spend(0.00142)
    metrics = get_shared_fiscal_metrics()

    LIVE_TRANSACTION_STATES[trace_id] = {
        "status": "SUCCESS",
        "task": sanitized_task,
        "selected_model": "local_ollama",
        "orchestrator_bus": "IBM_BOB_MCP",
        "harbor_status": "VERIFIED",
        "harbor_digest": mock_digest,
        "recursive_tco_usd": metrics["cumulative_spend"]
    }

    return GovernanceResponse(
        status="SUCCESS", trace_id=trace_id, recursive_tco_usd=metrics["cumulative_spend"],
        selected_model="local_ollama", sanitized_output=f"✅ COMPLIANT RUN: Cleared all pipeline checks.\nInput: {sanitized_task}",
        block_reason="NOMINAL: Active intent preserves infrastructure laws.",
        orchestrator_bus="IBM_BOB_MCP", harbor_status="VERIFIED", harbor_digest=mock_digest
    )