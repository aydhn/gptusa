"""Trader-style research reports from the LOCAL SIMULATED paper ledger (markdown / CSV / JSONL; no dashboard, no orders).

* decision journal  - every decision with regime, exposure, picks, exits and the pipeline trace;
* "why this position" - per held name: weight, signal rank, volatility, and the rule trace;
* daily active-risk CSV - portfolio vs equal-weight benchmark, tracking error vs a risk budget, cash interest, real return;
* weekly research summary - last weeks' numbers plus the honest evidence verdict.
Cash interest and inflation-adjusted (real) return appear in every report. Not investment advice.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import numpy as np
import pandas as pd

from usa_signal_bot.decision.pipeline import Decision
from usa_signal_bot.evidence.metrics import summarize
from usa_signal_bot.evidence.rates import real_cagr

NOTICE = "Yerel simüle ledger; emir/broker yok. Araştırma çıktısıdır, yatırım tavsiyesi değildir."


@dataclass(frozen=True)
class RiskBudget:
    max_tracking_error: float = 0.04  # annualised active risk the research book may use
    max_drawdown: float = 0.20


def write_decision_journal(decisions: Sequence[Decision], dates: Sequence[pd.Timestamp], path: Path) -> int:
    """JSONL, one line per decision (decided at the close of ``dates[i]``, filled next close)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for d, dec in zip(dates, decisions):
            fh.write(json.dumps({
                "decided_on": pd.Timestamp(d).strftime("%Y-%m-%d"), "regime": dec.regime, "exposure": round(dec.exposure, 4),
                "target_weights": {k: round(v, 5) for k, v in dec.target_weights.items()},
                "exits": dec.exits, "trace": dec.trace,
            }, sort_keys=True, ensure_ascii=False) + "\n")
    return len(decisions)


def explain_positions(decision: Decision, signals: Dict[str, float], vols: Dict[str, float]) -> str:
    """Markdown table: why each target position exists (signal rank, vol, sizing) + the pipeline trace."""
    ranked = sorted(signals, key=lambda s: -signals[s])
    rank = {s: i + 1 for i, s in enumerate(ranked)}
    lines = [f"Rejim: **{decision.regime}** (hedef maruziyet {decision.exposure:.0%}); çıkışlar: {decision.exits or 'yok'}", "",
             "| Sembol | Hedef ağırlık | Momentum sırası | Sinyal | Günlük vol | Neden |", "|---|---|---|---|---|---|"]
    for sym, w in sorted(decision.target_weights.items(), key=lambda kv: -kv[1]):
        v = vols.get(sym)
        lines.append(f"| {sym} | {w:.1%} | {rank.get(sym, '-')}/{len(ranked)} | {signals.get(sym, float('nan')):+.1%} | "
                     f"{(f'{v:.2%}' if v else '-')} | momentum üst sıra, ters-vol boyut, risk limiti sonrası |")
    lines += ["", "İz:"] + [f"- {t}" for t in decision.trace]
    return "\n".join(lines)


def daily_active_report(
    equity: pd.Series, benchmark_returns: pd.Series, cash_rate: pd.Series | float, inflation: float,
    budget: Optional[RiskBudget] = None, te_window: int = 63,
) -> pd.DataFrame:
    budget = budget or RiskBudget()
    eq = equity.copy()
    eq.index = pd.to_datetime(eq.index)
    ret = eq.pct_change().fillna(0.0)
    bench = benchmark_returns.reindex(ret.index).fillna(0.0)
    active = ret - bench
    te = active.rolling(te_window, min_periods=te_window // 2).std() * np.sqrt(252)
    dd = eq / eq.cummax() - 1.0
    if isinstance(cash_rate, pd.Series):
        cr = cash_rate.reindex(ret.index.union(cash_rate.index)).ffill().reindex(ret.index).fillna(0.0)
    else:
        cr = pd.Series(float(cash_rate), index=ret.index)
    cum_real = (1.0 + ret).cumprod() / ((1.0 + inflation) ** (np.arange(len(ret)) / 252.0))
    return pd.DataFrame({
        "equity": eq, "ret": ret, "benchmark_ret": bench, "active_ret": active,
        "cum_active": (1.0 + ret).cumprod() - (1.0 + bench).cumprod(),
        "tracking_error": te, "risk_budget_used": te / budget.max_tracking_error,
        "drawdown": dd, "drawdown_budget_used": (-dd) / budget.max_drawdown,
        "cash_rate_annual": cr, "real_equity_index": cum_real,
    })


def weekly_summary(daily: pd.DataFrame, inflation: float, evidence_note: str, weeks: int = 4, interest_earned: float = 0.0) -> str:
    wk = (1.0 + daily[["ret", "benchmark_ret"]]).resample("W-FRI").prod() - 1.0
    wk["active"] = wk["ret"] - wk["benchmark_ret"]
    last = wk.tail(weeks)
    perf = summarize(daily["ret"])
    bperf = summarize(daily["benchmark_ret"])
    lines = ["# Haftalık araştırma özeti (yerel simüle ledger)", "", f"> {NOTICE}", "",
             f"- Dönem: {daily.index[0].date()} → {daily.index[-1].date()} ({len(daily)} gün)",
             f"- Portföy CAGR {perf.cagr:.1%} (reel {real_cagr(perf.cagr, inflation):.1%}) | Kıyas CAGR {bperf.cagr:.1%} "
             f"(reel {real_cagr(bperf.cagr, inflation):.1%}) | Sharpe {perf.sharpe:.2f} vs {bperf.sharpe:.2f}",
             f"- Maks. düşüş {perf.max_drawdown:.1%}; son izleme hatası {daily['tracking_error'].iloc[-1]:.1%} "
             f"(risk bütçesi kullanımı {daily['risk_budget_used'].iloc[-1]:.0%})",
             f"- Boştaki nakit faizi birikimi: {interest_earned:,.2f}; güncel nakit faizi yıllık {daily['cash_rate_annual'].iloc[-1]:.2%}",
             f"- Kanıt durumu: {evidence_note}", "", "| Hafta | Portföy | Kıyas | Aktif |", "|---|---|---|---|"]
    for d, r in last.iterrows():
        lines.append(f"| {d.date()} | {r['ret']:+.2%} | {r['benchmark_ret']:+.2%} | {r['active']:+.2%} |")
    return "\n".join(lines) + "\n"


def latest_evidence_note(report_md: Optional[Path]) -> str:
    """One-line honest verdict pulled from an evidence report (the **Sonuç:** line), else a neutral default."""
    if report_md and report_md.exists():
        for line in report_md.read_text(encoding="utf-8").splitlines():
            if line.startswith("**Sonuç:**"):
                return line.replace("**", "")
    return "kanıt raporu verilmedi; kıyası geçen edge kanıtlanmış sayılmaz"
