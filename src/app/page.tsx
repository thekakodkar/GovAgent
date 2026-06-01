"use client";

import { useState, useEffect, useRef } from "react";

interface Message {
  role: "user" | "assistant";
  content: string;
  metrics?: {
    status: string;
    trace_id: string;
    recursive_tco_usd: number;
    block_reason?: string;
    slack_status?: string;
  };
}

interface Policy {
  id: string;
  name: string;
  max_spend: number;
  required_guards: string[];
  raw_content: any; 
}

interface ArchiveSession {
  id: string;
  timestamp: string;
  preview: string;
  messages: Message[];
}

export default function Home() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [policies, setPolicies] = useState<Policy[]>([]);
  const [selectedPolicy, setSelectedPolicy] = useState<Policy | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeMetrics, setActiveMetrics] = useState<any>(null);
  const [systemLogs, setSystemLogs] = useState<string[]>([]);
  const [archives, setArchives] = useState<ArchiveSession[]>([]);
  const [showRawPolicy, setShowRawPolicy] = useState(false);
  
  const consoleEndRef = useRef<HTMLDivElement>(null);
  const pollingIntervalRef = useRef<any>(null); // Anchor pointer holds interval context safely

  const BACKEND_URL = "http://localhost:8000";
  const AUTH_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer gov-secret-key-100x"
  };

  const pushLog = (text: string) => {
    const timestamp = new Date().toLocaleTimeString();
    setSystemLogs((prev) => [...prev, `[${timestamp}] ${text}`]);
  };

  // Cleanup active memory leaks on unmount strings
  useEffect(() => {
    return () => { if (pollingIntervalRef.current) clearInterval(pollingIntervalRef.current); };
  }, []);

  useEffect(() => {
    async function loadInitialMetadata() {
      try {
        const res = await fetch(`${BACKEND_URL}/api/v1/governance/policies`, { headers: AUTH_HEADERS });
        if (res.ok) {
          const data = await res.json();
          setPolicies(data);
          if (data.length > 0) {
            setSelectedPolicy(data[0]);
            pushLog(`Policy framework parsed: "${data[0].name}" synchronized as baseline anchor.`);
          }
        }
      } catch (err) {
        pushLog("🛑 Connection Failure: Could not locate active FastAPI backend server.");
      }
    }
    loadInitialMetadata();
  }, []);

  useEffect(() => { consoleEndRef.current?.scrollIntoView({ behavior: "smooth" }); }, [systemLogs]);

  const handleClearChat = () => {
    setMessages([]);
    setActiveMetrics(null);
    if (pollingIntervalRef.current) clearInterval(pollingIntervalRef.current);
    pushLog("Volatile Session Memory Purged.");
  };

  const handleArchiveChat = () => {
    if (messages.length === 0) return;
    const newArchive: ArchiveSession = {
      id: `ARCH-${Math.random().toString(36).substring(2, 8).toUpperCase()}`,
      timestamp: new Date().toLocaleTimeString(),
      preview: messages[0].content.substring(0, 30) + "...",
      messages: [...messages]
    };
    setArchives((prev) => [newArchive, ...prev]);
    setMessages([]);
    setActiveMetrics(null);
  };

  const handleRestoreArchive = (archive: ArchiveSession) => {
    setMessages(archive.messages);
    const lastAssistantMsg = [...archive.messages].reverse().find(m => m.role === "assistant" && m.metrics);
    if (lastAssistantMsg && lastAssistantMsg.metrics) setActiveMetrics(lastAssistantMsg.metrics);
  };

  // --- 📡 ASYNCHRONOUS POLL MECHANISM CONTROLLER ---
  const startStateSynchronizationPoll = (traceId: string, basePrompt: string) => {
    pushLog(`📡 POLLING INITIALIZED: Listening for out-of-band Slack authorization tokens...`);
    
    if (pollingIntervalRef.current) clearInterval(pollingIntervalRef.current);

    pollingIntervalRef.current = setInterval(async () => {
      try {
        const res = await fetch(`${BACKEND_URL}/api/v1/governance/state/${traceId}`);
        if (!res.ok) return;

        const remoteState = await res.json();

        if (remoteState.status === "APPROVED") {
          clearInterval(pollingIntervalRef.current);
          setLoading(false);
          pushLog(`✓ Slack Core Consensus Synchronized: APPROVED ✅ Overriding local policy thresholds.`);

          const updateMetrics = { status: "SUCCESS", trace_id: traceId, recursive_tco_usd: 0.00284 };
          setActiveMetrics(updateMetrics);

          setMessages((prev) => [
            ...prev.filter(m => m.metrics?.trace_id !== traceId), // Erase the pending card
            {
              role: "assistant",
              content: "✅ TRANSACTION SANCTIONED: Human-in-the-loop multi-sig bypass verified via Slack Workspace. Proceeding with compute swarm procurement initialization.",
              metrics: updateMetrics
            }
          ]);
        } else if (remoteState.status === "VETOED") {
          clearInterval(pollingIntervalRef.current);
          setLoading(false);
          pushLog(`❌ Slack Core Consensus Synchronized: VETOED 🛑 Execution halted.`);

          const updateMetrics = { status: "BLOCKED", trace_id: traceId, recursive_tco_usd: 0.00 };
          setActiveMetrics(updateMetrics);

          setMessages((prev) => [
            ...prev.filter(m => m.metrics?.trace_id !== traceId),
            {
              role: "assistant",
              content: "🛑 TRANSACTION TERMINATED: Operational request denied via live executive veto inside Slack.",
              metrics: updateMetrics
            }
          ]);
        }
      } catch (err) {
        console.error("Polling sync anomaly:", err);
      }
    }, 2000); // Polls memory map registers seamlessly every 2000 milliseconds
  };

  const handlePipelineSubmission = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const currentPrompt = input;
    setMessages((prev) => [...prev, { role: "user", content: currentPrompt }]);
    setLoading(true);
    setInput("");
    
    pushLog(`Evaluating transaction footprint: "${currentPrompt.substring(0, 32)}..."`);

    try {
      const response = await fetch(`${BACKEND_URL}/api/v1/governance/evaluate`, {
        method: "POST",
        headers: AUTH_HEADERS,
        body: JSON.stringify({
          task_input: currentPrompt,
          policy_profile: selectedPolicy?.id || "policies/finance_policy.yaml"
        }),
      });

      if (!response.ok) throw new Error(`Gateway status exception: ${response.status}`);

      const data = await response.json();
      setActiveMetrics(data);

      if (data.status === "PENDING") {
        pushLog(`🚨 POLICY CEILING BREACH DETECTED: Halted thread at perimeter.`);
        if (data.slack_escalation_status) pushLog(data.slack_escalation_status);

        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: `${data.sanitized_output}\n\n⏳ OUT-OF-BAND DISPATCH REFERENCE:\n${data.block_reason}`,
            metrics: {
              status: "PENDING", trace_id: data.trace_id, recursive_tco_usd: 0.00,
              slack_status: data.slack_escalation_status
            }
          }
        ]);

        // Hand over execution pipeline variables to background polling worker loop
        startStateSynchronizationPoll(data.trace_id, currentPrompt);
      } else {
        setLoading(false);
        pushLog(`✓ Verification Confirmed: Input payload cleared regulatory constraints.`);
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: data.sanitized_output,
            metrics: {
              status: data.status, trace_id: data.trace_id, recursive_tco_usd: data.recursive_tco_usd
            }
          }
        ]);
      }

    } catch (error: any) {
      pushLog(`🛑 Infrastructure Pipeline Error: ${error.message}`);
      setLoading(false);
    }
  };

  return (
    <main className="flex h-screen w-screen bg-slate-950 text-slate-100 antialiased overflow-hidden">
      
      {/* LEFT SIDEBAR PANEL COMPONENT */}
      <aside className="w-80 bg-slate-900/90 border-r border-slate-800/60 p-5 flex flex-col justify-between hidden md:flex h-full overflow-y-auto space-y-6">
        <div className="space-y-6">
          <div className="flex items-center gap-3">
            <div className="bg-emerald-500/10 border border-emerald-500/20 p-2 rounded-xl text-lg">🛡️</div>
            <div>
              <h1 className="font-bold tracking-tight text-sm">govAgent Control</h1>
              <p className="text-[11px] text-slate-500 font-medium">Sovereign Governance Plane</p>
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-[10px] font-bold uppercase text-slate-400 tracking-wider flex items-center gap-2">📜 Legislative Blueprint</label>
            <select
              value={selectedPolicy?.id || ""}
              onChange={(e) => {
                const found = policies.find(p => p.id === e.target.value);
                if (found) { setSelectedPolicy(found); pushLog(`Active frame changed to: ${found.name}`); }
              }}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs font-medium text-slate-200 focus:outline-none"
            >
              {policies.map((p) => <option key={p.id} value={p.id}>{p.name}</option>)}
            </select>
          </div>

          {selectedPolicy && (
            <div className="bg-slate-950/80 border border-slate-800/60 rounded-xl p-3 space-y-2">
              <button onClick={() => setShowRawPolicy(!showRawPolicy)} className="w-full flex justify-between items-center text-[10px] font-bold uppercase text-slate-400 focus:outline-none">
                <span>🔍 Inspect Active Rules</span><span>{showRawPolicy ? "▼" : "▶"}</span>
              </button>
              {showRawPolicy && (
                <div className="pt-2 text-[10px] font-mono text-slate-400 space-y-2 max-h-40 overflow-y-auto border-t border-slate-900 mt-2">
                  <div><span className="text-emerald-500">Agent:</span> {selectedPolicy.raw_content?.metadata?.agent_name}</div>
                  <div><span className="text-emerald-500">Ceiling:</span> ${selectedPolicy.max_spend?.toLocaleString()} USD</div>
                  <div><span className="text-emerald-500">Standard:</span> {selectedPolicy.raw_content?.metadata?.compliance_standard}</div>
                </div>
              )}
            </div>
          )}

          <div className="space-y-2 bg-slate-950/40 border border-slate-800/40 rounded-xl p-3">
            <div className="text-[10px] font-bold uppercase text-slate-400 tracking-wider">Session Controls</div>
            <div className="grid grid-cols-2 gap-2">
              <button onClick={handleClearChat} className="bg-slate-900 hover:bg-slate-800 border border-slate-800 rounded-lg py-2 text-[11px] font-medium text-rose-400">🗑️ Clear</button>
              <button onClick={handleArchiveChat} disabled={messages.length === 0} className="bg-emerald-600/10 border border-emerald-500/20 rounded-lg py-2 text-[11px] font-medium text-emerald-400 disabled:opacity-30">📦 Archive</button>
            </div>
          </div>

          <div className="space-y-2">
            <div className="text-[10px] font-bold uppercase text-slate-400 tracking-wider">🗄️ Archive Registers ({archives.length})</div>
            <div className="space-y-1.5 max-h-36 overflow-y-auto pr-1">
              {archives.length === 0 ? <div className="text-[11px] text-slate-600 italic pl-1">No session telemetry records.</div> : 
                archives.map((arch) => (
                  <button key={arch.id} onClick={() => handleRestoreArchive(arch)} className="w-full text-left bg-slate-950 border border-slate-800/40 rounded-xl p-2.5 block text-[11px]">
                    <div className="flex justify-between font-mono text-slate-400 text-[10px]"><span>{arch.id}</span><span className="text-slate-600">{arch.timestamp}</span></div>
                    <div className="text-slate-500 truncate mt-0.5">{arch.preview}</div>
                  </button>
                ))
              }
            </div>
          </div>
        </div>

        <div className="bg-slate-950/60 border border-slate-800/80 rounded-2xl p-4 space-y-3 mt-auto">
          <h3 className="text-[11px] font-bold uppercase text-slate-400 tracking-wider">📊 Live Audit Matrix</h3>
          {activeMetrics ? (
            <div className="space-y-2.5 text-xs">
              <div className="flex justify-between items-center bg-slate-900 px-3 py-1.5 rounded-xl border border-slate-800/40">
                <span className="text-slate-500 font-medium">Verdict:</span>
                <span className={`font-bold uppercase tracking-wide text-[10px] px-2 py-0.5 rounded-md ${
                  activeMetrics.status === "SUCCESS" ? "bg-emerald-500/10 text-emerald-400" : activeMetrics.status === "PENDING" ? "bg-amber-500/10 text-amber-400 animate-pulse" : "bg-rose-500/10 text-rose-400"
                }`}>{activeMetrics.status}</span>
              </div>
              <div className="space-y-1 font-medium text-[11px] text-slate-400">
                <div className="flex justify-between"><span className="text-slate-500">Recursive Cost:</span><span className="font-mono text-emerald-400">${activeMetrics.recursive_tco_usd?.toFixed(5)}</span></div>
                <div className="flex flex-col pt-2 border-t border-slate-900"><span className="text-slate-600 text-[10px]">Trace Identifier:</span><span className="font-mono text-[10px] block truncate">{activeMetrics.trace_id}</span></div>
              </div>
            </div>
          ) : <p className="text-xs text-slate-600 italic">Awaiting pipeline telemetry events...</p>}
        </div>
      </aside>

      {/* CENTER WORKSPACE CHAT PANEL CONSOLE CONTAINER */}
      <section className="flex-1 flex flex-col h-full min-w-0 bg-slate-950 relative">
        <div className="flex-1 overflow-y-auto p-6 md:p-12 space-y-6 pb-32">
          {messages.length === 0 && (
            <div className="h-full flex flex-col items-center justify-center text-center max-w-sm mx-auto space-y-4 pt-20">
              <div className="h-12 w-12 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-lg">🛡️</div>
              <div>
                <p className="text-xs font-semibold uppercase text-slate-400 tracking-wider">Autonomous Security Sandbox</p>
                <p className="text-xs text-slate-500 mt-1 leading-relaxed">Select a compliance guideline asset, inspect parameters, and evaluate boundaries live.</p>
              </div>
            </div>
          )}

          {messages.map((msg, idx) => (
            <div key={idx} className={`flex gap-4 max-w-3xl mx-auto ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
              <div className={`rounded-2xl px-4 py-3 text-sm leading-relaxed max-w-[85%] border shadow-sm ${
                msg.role === "user" ? "bg-emerald-500/10 border-emerald-500/20 text-emerald-100" : 
                msg.metrics?.status === "PENDING" ? "bg-amber-950/20 border-amber-500/20 text-amber-200" :
                msg.metrics?.status === "BLOCKED" ? "bg-rose-950/20 border-rose-500/20 text-rose-200" : "bg-slate-900 border-slate-800/80 text-slate-200"
              }`}>
                <div className="whitespace-pre-wrap font-medium">{msg.content}</div>
                {msg.metrics?.slack_status && <div className="mt-3 pt-2 border-t border-slate-800/60 text-[10px] text-amber-400 font-mono bg-amber-950/30 p-2 rounded-lg border border-amber-500/10 animate-pulse">{msg.metrics.slack_status}</div>}
              </div>
            </div>
          ))}
        </div>

        <div className="absolute bottom-0 left-0 right-0 p-6 border-t border-slate-900 bg-slate-950 z-10">
          <form onSubmit={handlePipelineSubmission} className="max-w-3xl mx-auto flex gap-3">
            <input
              type="text" value={input} onChange={(e) => setInput(e.target.value)}
              placeholder={loading ? "Polling for human-in-the-loop validation response..." : "Instruct the autonomous agent..."}
              disabled={loading}
              className="flex-1 bg-slate-900 border border-slate-800/80 rounded-xl px-4 py-3.5 text-xs text-slate-100 placeholder-slate-600 focus:outline-none focus:border-emerald-500/50"
            />
            <button type="submit" disabled={loading || !input.trim()} className="bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-900 text-slate-100 rounded-xl px-5 flex justify-center items-center font-bold">➔</button>
          </form>
        </div>
      </section>

      {/* RIGHT SIDEBAR PANEL COMPONENT */}
      <section className="w-80 bg-slate-950 border-l border-slate-900 flex flex-col hidden lg:flex h-full">
        <div className="p-4 border-b border-slate-900 flex items-center gap-2 bg-slate-900/30"><span>💻</span><h2 className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Forensic Engine Stream</h2></div>
        <div className="flex-1 overflow-y-auto p-4 font-mono text-[10px] space-y-2 text-slate-400 bg-slate-950">
          {systemLogs.map((log, idx) => <div key={idx} className="leading-relaxed border-b border-slate-900/10 pb-1 break-words">{log}</div>)}
          <div ref={consoleEndRef} />
        </div>
      </section>

    </main>
  );
}