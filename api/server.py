import os
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
from govagent import ExecutiveAgent
from govagent.context import reset_fiscal_ledger

app = FastAPI(title="govAgent Enterprise Governance Plane", version="0.6.0")

# Security Matrix: Simple token validation for enterprise tenants
API_TOKEN = os.environ.get("GOVAGENT_SECRET_TOKEN", "gov-secret-key-100x")

class GovernanceRequest(BaseModel):
    task_input: str
    policy_profile: str = "policies/corporate_policy.yaml"
    organization_id: str = "GLOBAL_HOLDING"
    context_data: Optional[Dict[str, Any]] = None

class GovernanceResponse(BaseModel):
    status: str
    trace_id: str
    recursive_tco_usd: float
    sanitized_output: Optional[str] = None
    error_log: Optional[str] = None

def verify_auth(authorization: Optional[str] = Header(None)):
    if not authorization or authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid Institutional Token.")

@app.post("/api/v1/governance/evaluate", response_model=GovernanceResponse, dependencies=[Depends(verify_auth)])
async def evaluate_workflow_intent(payload: GovernanceRequest):
    """
    HTTP Entry Point: Intercepts workflow parameters and evaluates them 
    against strict multi-stage quantitative and qualitative guardrails.
    """
    # Isolate fiscal states for clean api execution contexts
    reset_fiscal_ledger()
    
    try:
        # 1. Bootstrap the agent dynamically based on policy guidelines
        agent = ExecutiveAgent.bootstrap(
            policy_path=payload.policy_profile,
            model_client=None  # Set up your active LLM runtime mapping client here
        )
        
        # 2. Inject structural organization data tracking markers
        agent.telemetry.start_trace(agent_id="n8n-Gateway-Agent", task=payload.task_input)
        
        # 3. Process execution across guards (Privacy, Fiscal, Semantic)
        report = await agent.execute(payload.task_input)
        
        return GovernanceResponse(
            status=report.status.upper(),
            trace_id=report.trace_id,
            recursive_tco_usd=report.recursive_tco_usd,
            sanitized_output=report.steps[-1].get("result") if report.steps else payload.task_input
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Governance Circuit Breaker Error: {str(e)}")