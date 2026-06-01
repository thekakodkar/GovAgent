import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from govagent import ExecutiveAgent, tool
from govagent.context import set_current_agent, reset_current_agent

load_dotenv()

@tool(name="get_customer_data", risk_level="low")
async def get_customer_data(customer_id: str):
    """Fetches verified customer accounts ledger fields out of memory space securely."""
    return {"name": "John Doe", "balance": 12450.75}

async def main():
    print("👥 RUNNING ALIGNED MULTI-AGENT SWARM TRACEABILITY DEMO\n" + "="*60)
    
    # 1. Initialize Parent Authority Node (The Orchestration Director)
    director = ExecutiveAgent.bootstrap(
        policy_path="policies/team_policy.yaml",
        llm=ChatOpenAI(model="gpt-4o", temperature=0)
    )
    director.telemetry.start_trace("Director", "Master Credit Analysis Prompt")
    parent_trace_id = director.telemetry.current_session.trace_id
    
    print(f"🏢 [Parent Director] Established Master Anchor Trace ID: {parent_trace_id}")
    
    # 2. Enroll Parent into Context to simulate a secure delegation chain
    context_token = set_current_agent(director)
    
    try:
        print("🤖 [Director] Delegating tasks downstream to child sub-agents...")
        
        # 3. Instantiate Child Sub-Agents (They automatically inherit the tracking state)
        researcher = ExecutiveAgent.bootstrap(policy_path="policies/team_policy.yaml", llm=None)
        researcher.telemetry.start_trace("Researcher", "Granular Balance Extraction")
        
        print(f"└─ 📡 [Child Researcher] Inherited Parent Reference ID: {researcher.telemetry.current_session.parent_trace_id}")
        
        # Assert structural synchronization tracking for verification
        assert researcher.telemetry.current_session.parent_trace_id == parent_trace_id
        print("✅ Swarm Traceability Verification: Article 12 context chain matches perfectly.")
        
    finally:
        # Gracefully release the execution slot
        reset_current_agent(context_token)

if __name__ == "__main__":
    asyncio.run(main())