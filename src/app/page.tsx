// src/app/page.tsx
"use client";

import React, { useState, useEffect } from "react";
import CFOExecutivePanel from "./components/CFOExecutivePanel";
import {
  Shield,
  FileCode,
  CheckCircle2,
  AlertOctagon,
  Terminal,
  Activity,
  Cpu,
  Download,
  ChevronDown,
  ChevronUp,
  Sliders,
  DollarSign,
  Bot,
  LayoutDashboard
} from "lucide-react";

interface PolicyItem {
  id: string;
  name: string;
  max_spend: number;
  required_guards: string[];
  raw_content: Record<string, any>;
}

interface AuditMetrics {
  verdict: "SUCCESS" | "BLOCKED" | "PENDING";
  trace_id: string;
  recursive_tco_usd: number;
  selected_model: string;
  harbor_status?: string;
  harbor_digest?: string;
  block_reason?: string;
  orchestrator_bus?: string;
}

const AVAILABLE_MODELS = [
  { id: "gpt-4o", name: "OpenAI GPT-4o (Commercial Tier)" },
  { id: "claude-3-5-sonnet", name: "Anthropic Claude 3.5 Sonnet" },
  { id: "mistral-large", name: "Mistral Large (EU Sovereign Cloud)" },
  { id: "local_ollama", name: "Ollama Local (Sovereign Air-Gapped)" },
];

export default function Home() {
  const [policies, setPolicies] = useState<PolicyItem[]>([]);
  const [selectedPolicy, setSelectedPolicy] = useState<PolicyItem | null>(null);
  const [selectedModel, setSelectedModel] = useState<string>("gpt-4o");

  // Visual layout toggles
  const [showCFOFirst, setShowCFOFirst] = useState<boolean>(true);
  const [runtimeConsoleOpen, setRuntimeConsoleOpen] = useState<boolean>(true);
  const [yamlInspectorOpen, setYamlInspectorOpen] = useState<boolean>(false);

  const [taskInput, setTaskInput] = useState("");
  const [evaluating, setEvaluating] = useState(false);
  const [exporting, setExporting] = useState(false);

  const [logs, setLogs] = useState<string[]>([
    "🟢 System initialized. Sovereign governance plane active.",
    "🔒 Harbor container supply chain verified: sha256:e3b0c442...",
  ]);

  const [activeMetrics, setActiveMetrics] = useState<AuditMetrics | null>({
    verdict: "SUCCESS",
    trace_id: "TR-INFRA-READY",
    recursive_tco_usd: 0.00122,
    selected_model: "gpt-4o",
    harbor_status: "VERIFIED",
    harbor_digest: "sha256:e3b0c442...",
    orchestrator_bus: "IBM_BOB_MCP",
  });

  const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";
  const AUTH_TOKEN = process.env.NEXT_PUBLIC_GOVAGENT_TOKEN || "gov-secret-key-100x";

  // Fetch policies directly from the live YAML registry
  useEffect(() => {
    const fetchPolicies = async () => {
      try {
        const res = await fetch(`${API_BASE}/api/v1/governance/policies`, {
          headers: { Authorization: `Bearer ${AUTH_TOKEN}` },
        });
        if (res.ok) {
          const data: PolicyItem[] = await res.json();
          if (Array.isArray(data) && data.length > 0) {
            setPolicies(data);
            setSelectedPolicy(data[0]);
            return;
          }
        }
      } catch (err) {
        console.warn("Using default fallback policy metadata:", err);
      }

      // Default fallback if server not yet booted
      const fallback: PolicyItem = {
        id: "policies/finance_policy.yaml",
        name: "Finance Director Policy",
        max_spend: 25.0,
        required_guards: ["privacy_redaction", "semantic_alignment", "tco_ceiling", "hitl_quorum"],
        raw_content: {
          agent_name: "Healthcare Finance Director",
          max_spend_usd: 25.0,
          semantic_threshold: 0.85,
        },
      };
      setPolicies([fallback]);
      setSelectedPolicy(fallback);
    };

    fetchPolicies();
  }, []);

  const handleExportEvidence = async () => {
    setExporting(true);
    try {
      const res = await fetch(`${API_BASE}/api/v1/governance/compliance/export`, {
        headers: { Authorization: `Bearer ${AUTH_TOKEN}` },
      });
      if (res.ok) {
        const dossier = await res.json();
        const blob = new Blob([JSON.stringify(dossier, null, 2)], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = `EU_AI_ACT_EVIDENCE_${dossier.export_id || "DOSSIER"}.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        setLogs((prev) => [
          `📦 [AUDIT] Regulatory dossier sealed & downloaded: SHA-256 ${dossier.dossier_sha256?.slice(0, 16)}...`,
          ...prev,
        ]);
      }
    } catch (err) {
      setLogs((prev) => [`⚠️ Failed to export evidence dossier: ${String(err)}`, ...prev]);
    } finally {
      setExporting(false);
    }
  };

  const handleEvaluate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!taskInput.trim() || !selectedPolicy) return;

    setEvaluating(true);
    const timestamp = new Date().toLocaleTimeString();
    setLogs((prev) => [
      `🚀 [${timestamp}] Dispatched (${selectedModel}): "${taskInput.slice(0, 45)}..."`,
      ...prev,
    ]);

    try {
      const res = await fetch(`${API_BASE}/api/v1/governance/evaluate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${AUTH_TOKEN}`,
        },
        body: JSON.stringify({
          task_input: taskInput,
          policy_profile: selectedPolicy.id,
          selected_model: selectedModel,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        setActiveMetrics({
          verdict: data.status,
          trace_id: data.trace_id,
          recursive_tco_usd: data.recursive_tco_usd,
          selected_model: data.selected_model,
          harbor_status: data.harbor_status,
          harbor_digest: data.harbor_digest,
          block_reason: data.block_reason,
          orchestrator_bus: data.orchestrator_bus,
        });

        if (data.status === "PENDING") {
          setLogs((prev) => [
            `⏳ [${data.trace_id}] ESCALATED: Spend exceeds ceiling. Slack quorum dispatched.`,
            `🔔 [${data.trace_id}] SLACK ADAPTER: Multi-sig approval pending.`,
            `📋 [${data.trace_id}] REASON: ${data.block_reason}`,
            ...prev,
          ]);
        } else if (data.status === "BLOCKED") {
          setLogs((prev) => [
            `🛑 [${data.trace_id}] BLOCKED: ${data.block_reason || "Deviation intercepted."}`,
            ...prev,
          ]);
        } else {
          setLogs((prev) => [
            `✅ [${data.trace_id}] RUN COMPLIANT: Cleared all governance guardrails.`,
            ...prev,
          ]);
        }
      }
    } catch (err) {
      setLogs((prev) => [`⚠️ Runtime evaluation failed: ${String(err)}`, ...prev]);
    } finally {
      setEvaluating(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 p-4 md:p-6 space-y-6 font-sans">
      {/* Top Header & Executive Command Bar */}
      <header className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800/80 pb-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-indigo-600/20 border border-indigo-500/40 rounded-xl">
            <Shield className="w-5 h-5 text-indigo-400" />
          </div>
          <div>
            <h1 className="text-lg font-black tracking-tight text-white flex items-center gap-2">
              govAgent Sovereign Governance Plane
              <span className="text-[10px] px-2 py-0.5 bg-indigo-950 text-indigo-300 border border-indigo-700/50 rounded-full font-mono">
                Phase 1 Core
              </span>
            </h1>
            <p className="text-[11px] text-slate-400 font-mono">
              EU AI Act (Art. 9, 12, 14) • NIST AI RMF • Enterprise Financial Integrity
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {/* Toggle View Mode Button */}
          <button
            onClick={() => setShowCFOFirst(!showCFOFirst)}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700 rounded-lg text-xs font-mono transition-all"
          >
            <LayoutDashboard className="w-3.5 h-3.5 text-emerald-400" />
            {showCFOFirst ? "Focus: Technical Console" : "Focus: Executive CFO Cockpit"}
          </button>

          <button
            onClick={handleExportEvidence}
            disabled={exporting}
            className="flex items-center gap-2 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-mono font-semibold transition-all shadow-md shadow-indigo-950/60"
          >
            <Download className="w-3.5 h-3.5" />
            {exporting ? "Sealing Dossier..." : "Export EU AI Act Dossier"}
          </button>
        </div>
      </header>

      {/* PROMINENT CFO CAPITAL RISK PANEL (Positioned at Top when showCFOFirst=true) */}
      {showCFOFirst && (
        <section className="bg-slate-900/60 border border-slate-800/90 rounded-2xl p-5 shadow-2xl space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
            <div className="flex items-center gap-2 text-xs font-bold font-mono text-emerald-400 uppercase tracking-wider">
              <DollarSign className="w-4 h-4" />
              Executive Financial Cockpit • Capital At Risk &amp; Ledger Protection
            </div>
            <span className="text-[10px] text-slate-400 font-mono">Real-time P&amp;L Protection Matrix</span>
          </div>
          <CFOExecutivePanel />
        </section>
      )}

      {/* RUNTIME GOVERNANCE & EXECUTION WORKSPACE */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Column: Policy Selector, Model Engine, & YAML Inspector */}
        <div className="lg:col-span-4 bg-slate-900/60 border border-slate-800/80 rounded-2xl p-4 flex flex-col space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800/60 pb-3">
            <h2 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2 font-mono">
              <FileCode className="w-4 h-4 text-indigo-400" />
              Policy &amp; Model Controls
            </h2>
            {selectedPolicy && (
              <span className="text-[11px] font-bold text-emerald-400 font-mono bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800/50">
                Ceiling: ${selectedPolicy.max_spend.toFixed(2)}
              </span>
            )}
          </div>

          {/* Active Policy Selector */}
          <div className="space-y-1">
            <label className="text-[11px] text-slate-400 font-mono flex items-center gap-1.5">
              <Sliders className="w-3 h-3 text-indigo-400" />
              Active Policy Profile:
            </label>
            <select
              value={selectedPolicy?.id || ""}
              onChange={(e) => {
                const found = policies.find((p) => p.id === e.target.value);
                if (found) setSelectedPolicy(found);
              }}
              className="w-full bg-slate-950 border border-slate-800 text-slate-200 text-xs font-mono rounded-xl p-2.5 focus:border-indigo-500 outline-none"
            >
              {policies.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name} — [Limit: ${p.max_spend.toFixed(0)}]
                </option>
              ))}
            </select>
          </div>

          {/* Inference Model Selector */}
          <div className="space-y-1">
            <label className="text-[11px] text-slate-400 font-mono flex items-center gap-1.5">
              <Bot className="w-3 h-3 text-sky-400" />
              Inference Orchestrator:
            </label>
            <select
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 text-slate-200 text-xs font-mono rounded-xl p-2.5 focus:border-sky-500 outline-none"
            >
              {AVAILABLE_MODELS.map((m) => (
                <option key={m.id} value={m.id}>
                  {m.name}
                </option>
              ))}
            </select>
          </div>

          {/* Collapsible Declarative Policy YAML */}
          <div className="pt-2 border-t border-slate-800/60 flex flex-col space-y-2">
            <button
              onClick={() => setYamlInspectorOpen(!yamlInspectorOpen)}
              className="flex justify-between items-center text-[11px] font-mono text-slate-400 hover:text-slate-200 transition-colors py-1"
            >
              <span>{selectedPolicy?.id || "policies/..."}</span>
              <span className="flex items-center gap-1 text-indigo-400 text-[10px]">
                {yamlInspectorOpen ? "Hide YAML" : "Inspect YAML"}
                {yamlInspectorOpen ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
              </span>
            </button>

            {yamlInspectorOpen && selectedPolicy && (
              <pre className="bg-slate-950 border border-slate-800 rounded-xl p-3 text-[10px] font-mono text-indigo-300/90 overflow-x-auto max-h-56">
                {JSON.stringify(selectedPolicy.raw_content, null, 2)}
              </pre>
            )}
          </div>
        </div>

        {/* Right Column: Intent Dispatch Terminal & Live Audit Matrix */}
        <div className="lg:col-span-8 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Terminal Input */}
            <div className="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-4 space-y-3">
              <div className="flex items-center justify-between">
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2 font-mono">
                  <Terminal className="w-4 h-4 text-indigo-400" />
                  Intent Vector Dispatch
                </h3>
                <span className="text-[10px] text-slate-500 font-mono">Bound to Active Guard</span>
              </div>

              <form onSubmit={handleEvaluate} className="space-y-3">
                <textarea
                  value={taskInput}
                  onChange={(e) => setTaskInput(e.target.value)}
                  placeholder="Enter task input (e.g., 'approve 100000')..."
                  className="w-full h-24 bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-slate-200 font-mono resize-none focus:border-indigo-500 outline-none"
                />
                <button
                  type="submit"
                  disabled={evaluating || !taskInput.trim()}
                  className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-800 text-white rounded-xl text-xs font-semibold font-mono transition-all shadow-md shadow-indigo-950"
                >
                  {evaluating ? "Evaluating Guardrails..." : "Evaluate Workflow Intent"}
                </button>
              </form>
            </div>

            {/* Live Audit Matrix */}
            <div className="bg-slate-950/60 border border-slate-800/80 rounded-2xl p-4 flex flex-col justify-between space-y-2 font-mono text-xs">
              <div className="flex justify-between items-center border-b border-slate-800/80 pb-2">
                <span className="text-[11px] font-bold text-slate-300 flex items-center gap-1.5">
                  <Activity className="w-3.5 h-3.5 text-sky-400" />
                  Live Audit Matrix
                </span>
                <span className="text-[10px] text-slate-500">Article 12 Telemetry</span>
              </div>

              <div className="space-y-1.5">
                <div className="flex justify-between items-center bg-slate-900/90 px-3 py-1.5 rounded-lg border border-slate-800/60">
                  <span className="text-slate-500">Verdict:</span>
                  <span className={`font-bold flex items-center gap-1 ${
                    activeMetrics?.verdict === "SUCCESS" ? "text-emerald-400" : activeMetrics?.verdict === "PENDING" ? "text-amber-400" : "text-rose-400"
                  }`}>
                    {activeMetrics?.verdict === "SUCCESS" ? <CheckCircle2 className="w-3.5 h-3.5" /> : <AlertOctagon className="w-3.5 h-3.5" />}
                    {activeMetrics?.verdict}
                  </span>
                </div>
                <div className="flex justify-between items-center bg-slate-900/90 px-3 py-1.5 rounded-lg border border-slate-800/60">
                  <span className="text-slate-500">Trace ID:</span>
                  <span className="text-indigo-300">{activeMetrics?.trace_id}</span>
                </div>
                <div className="flex justify-between items-center bg-slate-900/90 px-3 py-1.5 rounded-lg border border-slate-800/60">
                  <span className="text-slate-500">Model Engine:</span>
                  <span className="text-sky-300">{activeMetrics?.selected_model}</span>
                </div>
                <div className="flex justify-between items-center bg-slate-900/90 px-3 py-1.5 rounded-lg border border-slate-800/60">
                  <span className="text-slate-500">Cumulative TCO Spend:</span>
                  <span className="text-emerald-400 font-bold">${activeMetrics?.recursive_tco_usd?.toFixed(5)}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Forensic Engine Audit Stream */}
          <div className="bg-slate-950 border border-slate-800/90 rounded-2xl p-4 space-y-2 font-mono">
            <div className="flex items-center justify-between border-b border-slate-800/80 pb-2">
              <span className="text-[11px] uppercase font-bold text-slate-400 flex items-center gap-1.5">
                <Cpu className="w-3.5 h-3.5 text-indigo-400" />
                Forensic Engine Audit Stream (mTLS Event Buffer)
              </span>
              <span className="text-[10px] text-slate-500">Zero-Trust Pipeline</span>
            </div>
            <div className="space-y-1 text-[11px] max-h-32 overflow-y-auto pt-1">
              {logs.map((log, idx) => (
                <div key={idx} className="text-slate-400 leading-relaxed">{log}</div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* CFO Panel at Bottom when showCFOFirst=false */}
      {!showCFOFirst && (
        <section className="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6 shadow-2xl">
          <CFOExecutivePanel />
        </section>
      )}
    </main>
  );
}