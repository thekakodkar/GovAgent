// src/app/page.tsx (Update the interface definition and Live Audit Matrix rendering section)

interface Message {
  role: "user" | "assistant";
  content: string;
  metrics?: {
    status: string;
    trace_id: string;
    recursive_tco_usd: number;
    selected_model?: string;
    block_reason?: string;
    orchestrator_bus?: string;   // Added v3.0.0 primitive
    harbor_status?: string;       // Added v3.0.0 primitive
    harbor_digest?: string;       // Added v3.0.0 primitive
  };
}

// ... Maintain standard core helper configurations ...

{/* RE-ENGINEERED SIDEBAR BALANCES GRAPH COMPONENT */}
<div className="bg-slate-950/60 border border-slate-800/80 rounded-2xl p-4 space-y-3 mt-auto">
  <h3 className="text-[11px] font-bold uppercase text-slate-400 tracking-wider">📊 Live Audit Matrix</h3>
  {activeMetrics ? (
    <div className="space-y-2.5 text-xs">
      <div className="flex justify-between items-center bg-slate-900 px-3 py-1.5 rounded-xl border border-slate-800/40">
        <span className="text-slate-500 font-medium">Verdict:</span>
        <span className={`font-bold uppercase tracking-wide text-[10px] px-2 py-0.5 rounded-md ${
          activeMetrics.status === "SUCCESS" ? "bg-emerald-500/10 text-emerald-400" : "bg-rose-500/10 text-rose-400"
        }`}>{activeMetrics.status}</span>
      </div>
      
      <div className="space-y-1.5 font-medium text-[11px] text-slate-400">
        <div className="flex justify-between">
          <span className="text-slate-500">Middleware Bus:</span>
          <span className="font-mono text-cyan-400">{activeMetrics.orchestrator_bus || "Native Run"}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-slate-500">Harbor State:</span>
          <span className={`font-bold ${activeMetrics.harbor_status === "VERIFIED" ? "text-emerald-400" : "text-rose-400"}`}>
            {activeMetrics.harbor_status || "UNSCANNING"}
          </span>
        </div>
        {activeMetrics.harbor_digest && activeMetrics.harbor_digest !== "NONE" && (
          <div className="bg-slate-900/40 p-1.5 rounded border border-slate-900 text-[9px] font-mono block truncate text-slate-500">
            SHA: <span className="text-slate-300">{activeMetrics.harbor_digest}</span>
          </div>
        )}
        <div className="flex justify-between">
          <span className="text-slate-500">Recursive TCO:</span>
          <span className="font-mono text-emerald-400">${activeMetrics.recursive_tco_usd?.toFixed(5)}</span>
        </div>
      </div>
    </div>
  ) : <p className="text-xs text-slate-600 italic">Awaiting pipeline telemetry events...</p>}
</div>