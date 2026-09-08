// src/app/components/CFOExecutivePanel.tsx
"use client";

import React, { useState, useEffect } from "react";
import { DollarSign, FileText, TrendingUp, CheckCircle, AlertTriangle } from "lucide-react";

interface CostCenterAllocation {
  cost_center_id: string;
  gl_account: string;
  allocated_spend_usd: number;
  transaction_count: number;
  token_usage_total: number;
}

interface CFORiskReport {
  total_realized_spend_usd: number;
  value_at_risk_prevented_usd: number;
  burn_rate_anomaly_detected: boolean;
  average_cost_per_work_unit: number;
  allocations_by_center: Record<string, CostCenterAllocation>;
}

export default function CFOExecutivePanel() {
  const [report, setReport] = useState<CFORiskReport | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [exporting, setExporting] = useState<boolean>(false);

  const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";
  const AUTH_TOKEN = process.env.NEXT_PUBLIC_GOVAGENT_TOKEN || "gov-secret-key-100x";

  const fetchCFOData = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/v1/governance/financials/risk-overview`, {
        headers: { Authorization: `Bearer ${AUTH_TOKEN}` },
      });
      if (res.ok) {
        const data = await res.json();
        setReport(data);
      }
    } catch (err) {
      console.error("Failed to load CFO analytics:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCFOData();
    const interval = setInterval(fetchCFOData, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleExportDossier = async () => {
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
      }
    } catch (err) {
      console.error("Dossier export failed:", err);
    } finally {
      setExporting(false);
    }
  };

  if (loading) {
    return <div className="p-4 text-slate-400 font-mono text-xs animate-pulse">Loading financial ledgers...</div>;
  }

  return (
    <div className="space-y-6">
      {/* Top Header & 1-Click Regulatory Export */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
            <DollarSign className="w-5 h-5 text-emerald-400" />
            CFO Capital Risk &amp; Ledger Allocation
          </h2>
          <p className="text-xs text-slate-400">EU AI Act (Art. 9, 12, 14) &amp; NIST AI RMF Financial Control</p>
        </div>
        <button
          onClick={handleExportDossier}
          disabled={exporting}
          className="flex items-center gap-2 px-3 py-2 bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-800 text-white rounded-lg text-xs font-semibold transition-all border border-indigo-400/30 shadow-lg shadow-indigo-950/50"
        >
          <FileText className="w-4 h-4" />
          {exporting ? "Sealing Dossier..." : "Export EU AI Act Evidence"}
        </button>
      </div>

      {/* KPI Value-at-Risk Metric Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4">
          <div className="text-xs text-slate-400 font-medium flex items-center justify-between">
            Realized TCO Spend
            <TrendingUp className="w-4 h-4 text-sky-400" />
          </div>
          <div className="text-2xl font-black text-slate-100 mt-2 font-mono">
            ${(report?.total_realized_spend_usd ?? 0).toFixed(4)}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Aggregated across all runtimes</div>
        </div>

        <div className="bg-slate-900/80 border border-emerald-950/60 rounded-xl p-4">
          <div className="text-xs text-emerald-400 font-medium flex items-center justify-between">
            Value-at-Risk Prevented
            <CheckCircle className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-black text-emerald-400 mt-2 font-mono">
            ${(report?.value_at_risk_prevented_usd ?? 0).toFixed(2)}
          </div>
          <div className="text-[11px] text-emerald-600/80 mt-1">Halted by Fiscal &amp; Quorum Guards</div>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4">
          <div className="text-xs text-slate-400 font-medium flex items-center justify-between">
            Cost / Unit Work
            <DollarSign className="w-4 h-4 text-slate-400" />
          </div>
          <div className="text-2xl font-black text-slate-200 mt-2 font-mono">
            ${(report?.average_cost_per_work_unit ?? 0).toFixed(4)}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Normalized execution unit price</div>
        </div>

        <div className={`border rounded-xl p-4 ${report?.burn_rate_anomaly_detected ? "bg-rose-950/20 border-rose-800" : "bg-slate-900/80 border-slate-800"}`}>
          <div className="text-xs font-medium flex items-center justify-between">
            <span className={report?.burn_rate_anomaly_detected ? "text-rose-400" : "text-slate-400"}>Burn Rate Anomaly</span>
            {report?.burn_rate_anomaly_detected ? (
              <AlertTriangle className="w-4 h-4 text-rose-400 animate-pulse" />
            ) : (
              <CheckCircle className="w-4 h-4 text-slate-500" />
            )}
          </div>
          <div className="text-lg font-bold mt-2">
            {report?.burn_rate_anomaly_detected ? (
              <span className="text-rose-400 font-mono">RECURSION SPIRAL</span>
            ) : (
              <span className="text-emerald-400 font-mono">NOMINAL</span>
            )}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">&gt; $0.50 per-task circuit breaker</div>
        </div>
      </div>

      {/* Enterprise Cost Center Allocations Table */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl overflow-hidden">
        <div className="p-3 border-b border-slate-800 bg-slate-900/90 flex justify-between items-center">
          <h3 className="text-xs font-semibold text-slate-200">ERP GL Account &amp; Cost Center Allocations</h3>
          <span className="text-[11px] text-slate-500 font-mono">P&amp;L Mapping</span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950/60 text-slate-400 border-b border-slate-800 uppercase tracking-wider font-mono">
              <tr>
                <th className="py-2.5 px-4">Cost Center ID</th>
                <th className="py-2.5 px-4">GL Account</th>
                <th className="py-2.5 px-4 text-right">Transactions</th>
                <th className="py-2.5 px-4 text-right">Total Tokens</th>
                <th className="py-2.5 px-4 text-right">Allocated Spend</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-300 font-mono">
              {Object.values(report?.allocations_by_center || {}).length === 0 ? (
                <tr>
                  <td colSpan={5} className="py-6 text-center text-slate-500 italic">No ledger allocations recorded yet.</td>
                </tr>
              ) : (
                Object.values(report?.allocations_by_center || {}).map((item) => (
                  <tr key={item.cost_center_id} className="hover:bg-slate-800/40">
                    <td className="py-2.5 px-4 text-indigo-300 font-bold">{item.cost_center_id}</td>
                    <td className="py-2.5 px-4 text-slate-400">{item.gl_account}</td>
                    <td className="py-2.5 px-4 text-right">{item.transaction_count}</td>
                    <td className="py-2.5 px-4 text-right">{item.token_usage_total.toLocaleString()}</td>
                    <td className="py-2.5 px-4 text-right font-bold text-emerald-400">${item.allocated_spend_usd.toFixed(5)}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}