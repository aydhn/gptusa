"""Dated report package (markdown + CSV only) from the LOCAL SIMULATED paper ledger and the hypothesis log.

Reuses ``decision.reporting`` (journal, daily active-risk, weekly summary). Every file carries the disclaimer.
No orders, no broker, no dashboard; nothing here activates anything.
"""

from __future__ import annotations

import json
from datetime import date as _date
from pathlib import Path
from typing import Callable, Dict, List, Optional, Union

import numpy as np
import pandas as pd

from usa_signal_bot.decision.ledger import PaperLedger
from usa_signal_bot.decision.pipeline import DecisionConfig
from usa_signal_bot.decision.reporting import (
    RiskBudget, daily_active_report, explain_positions, latest_evidence_note, weekly_summary, write_decision_journal,
)
from usa_signal_bot.decision.simulate import simulate_paper
from usa_signal_bot.evidence.costs import CostModel
from usa_signal_bot.evidence.hypothesis_log import HypothesisLog
from usa_signal_bot.evidence.metrics import summarize
from usa_signal_bot.evidence.rates import real_cagr
from usa_signal_bot.evidence.universe import PointInTimeUniverse

DISCLAIMER = "Yerel simüle ledger; emir/broker yok. Araştırma çıktısıdır, yatırım tavsiyesi değildir."


def hypothesis_summary(path: Optional[Path]) -> Dict[str, object]:
    """Families, total distinct trials and the best logged Sharpe per family (annualised from per-period values).

    The log stores each trial's own Sharpe (not benchmark-relative); the benchmark-relative figures of the package
    come from the simulated book in ``active_vs_benchmark``.
    """
    entries = HypothesisLog(Path(path), clock=lambda: "").entries() if path and Path(path).exists() else []
    fams: Dict[str, Dict[str, object]] = {}
    for e in entries:
        f = fams.setdefault(e.family, {"entries": 0, "best_sharpe": float("-inf"), "n_obs": 0, "labels": set()})
        f["entries"] += 1
        f["n_obs"] = max(int(f["n_obs"]), e.n_obs)
        f["labels"].add(e.data_label)
        f["best_sharpe"] = max(float(f["best_sharpe"]), e.sharpe_per_period * np.sqrt(252))
    labels = sorted({e.data_label for e in entries})
    n_trials = sum(HypothesisLog(Path(path), clock=lambda: "").n_trials(lb) for lb in labels) if entries else 0
    return {"n_entries": len(entries), "n_trials": n_trials, "labels": labels,
            "families": {k: {**v, "labels": sorted(v["labels"])} for k, v in sorted(fams.items())}}


def _hyp_markdown(h: Dict[str, object], active: Dict[str, float]) -> str:
    lines = ["# Hipotez günlüğü özeti", "", f"> {DISCLAIMER}", "",
             f"- Kayıt sayısı: {h['n_entries']} | farklı deneme (N): {h['n_trials']} | veri etiketleri: {', '.join(h['labels']) or '-'}",
             "- Çoklu deneme: N büyüdükçe en iyi Sharpe'ın anlamı azalır (DSR/SPA bunun içindir).", "",
             "| Aile | Kayıt | En iyi yıllık Sharpe (günlükteki, kıyassız) | Maks. gözlem |", "|---|---|---|---|"]
    for fam, v in h["families"].items():
        lines.append(f"| {fam} | {v['entries']} | {v['best_sharpe']:.2f} | {v['n_obs']} |")
    if not h["families"]:
        lines.append("| (günlük yok/boş) | 0 | - | - |")
    lines += ["", "## Kıyasa göre (simüle defter vs eşit ağırlık)", "",
              f"- Aktif getiri CAGR farkı: {active['cagr_diff']:+.1%} | aktif Sharpe: {active['active_sharpe']:.2f} | izleme hatası: {active['tracking_error']:.1%}",
              "- Kıyası anlamlı biçimde geçen kanıtlı bir edge bu paketle iddia edilmez.", ""]
    return "\n".join(lines)


def _real_and_cash_markdown(daily: pd.DataFrame, inflation: float, interest: float) -> str:
    perf, bperf = summarize(daily["ret"]), summarize(daily["benchmark_ret"])
    return "\n".join([
        "# Reel getiri ve nakit faizi", "", f"> {DISCLAIMER}", "",
        f"- Varsayılan/ölçülen yıllık enflasyon (CPI): {inflation:.2%}",
        f"- Portföy: nominal CAGR {perf.cagr:.1%} -> reel CAGR {real_cagr(perf.cagr, inflation):.1%}",
        f"- Kıyas: nominal CAGR {bperf.cagr:.1%} -> reel CAGR {real_cagr(bperf.cagr, inflation):.1%}",
        f"- Boştaki nakit faizi birikimi: {interest:,.2f}; son yıllık nakit faizi {daily['cash_rate_annual'].iloc[-1]:.2%}",
        f"- Reel öz sermaye endeksi (son): {daily['real_equity_index'].iloc[-1]:.3f}", ""])


def build_package(
    prices: pd.DataFrame, members: pd.DataFrame, out_root: Path, *, as_of: Optional[Union[str, _date]] = None,
    hypothesis_log: Optional[Path] = None, evidence_report: Optional[Path] = None, cash_rate: Union[float, pd.Series] = 0.02,
    inflation: float = 0.025, cash: float = 100000.0, cost: Optional[CostModel] = None, budget: Optional[RiskBudget] = None,
    clock: Callable[[], _date] = _date.today,
) -> Path:
    """Write ``<out_root>/<date>/`` and return that folder. Files: journal, why, active-risk CSV, hypothesis, real/cash, weekly."""
    day = str(as_of) if as_of else clock().isoformat()
    out = Path(out_root) / day
    out.mkdir(parents=True, exist_ok=True)
    ledger = PaperLedger(initial_cash=cash, cost=cost or CostModel(1.0, 5.0),
                         cash_rate_annual=float(cash_rate.iloc[-1]) if hasattr(cash_rate, "iloc") else float(cash_rate))
    decisions = simulate_paper(prices, members, DecisionConfig(), ledger)
    write_decision_journal(decisions, prices.index[: len(decisions)], out / "decision_journal.jsonl")
    jp = out / "decision_journal.jsonl"  # first line is a disclaimer record so the file carries the notice too
    jp.write_text(json.dumps({"disclaimer": DISCLAIMER}, ensure_ascii=False) + "\n" + jp.read_text(encoding="utf-8"), encoding="utf-8")

    bench = prices.pct_change(fill_method=None).where(members).mean(axis=1).fillna(0.0)
    daily = daily_active_report(pd.Series(ledger.equity_curve), bench, cash_rate, inflation, budget)
    csv = out / "daily_active_risk.csv"
    csv.write_text(f"# {DISCLAIMER}\n", encoding="utf-8")
    daily.to_csv(csv, index_label="date", mode="a")

    last = len(decisions) - 1
    score = (prices.shift(21) / prices.shift(126) - 1.0).where(members & prices.notna())
    vol = prices.pct_change(fill_method=None).rolling(20, min_periods=20).std()
    why = explain_positions(decisions[last], {s: float(v) for s, v in score.iloc[last].dropna().items()},
                            {s: float(v) for s, v in vol.iloc[last].dropna().items()})
    (out / "why_positions.md").write_text(f"# Neden bu pozisyon ({prices.index[last].date()} kararı)\n\n> {DISCLAIMER}\n\n{why}\n", encoding="utf-8")

    act = daily["active_ret"]
    perf, bperf = summarize(daily["ret"]), summarize(daily["benchmark_ret"])
    active = {"cagr_diff": float(perf.cagr - bperf.cagr),
              "active_sharpe": float(act.mean() / act.std(ddof=1) * np.sqrt(252)) if act.std(ddof=1) > 0 else 0.0,
              "tracking_error": float(daily["tracking_error"].iloc[-1]) if daily["tracking_error"].notna().any() else float("nan")}
    (out / "hypothesis_summary.md").write_text(_hyp_markdown(hypothesis_summary(hypothesis_log), active), encoding="utf-8")
    (out / "real_returns_cash.md").write_text(_real_and_cash_markdown(daily, inflation, ledger.interest_earned), encoding="utf-8")
    note = latest_evidence_note(evidence_report)
    wk = weekly_summary(daily, inflation, note, interest_earned=ledger.interest_earned)
    (out / "weekly_summary.md").write_text(wk if "yatırım tavsiyesi değildir" in wk else wk + f"\n> {DISCLAIMER}\n", encoding="utf-8")
    return out
