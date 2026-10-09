"""Run the evidence pipeline end to end and render an honest markdown report."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from usa_signal_bot.evidence.corporate_actions import PriceIssue, validate_adjusted_prices
from usa_signal_bot.evidence.costs import CostModel
from usa_signal_bot.evidence.data import MarketData
from usa_signal_bot.evidence.metrics import PerformanceSummary, sharpe_ci, summarize
from usa_signal_bot.evidence.factors import (
    factor_mix_weights,
    low_vol_weights,
    quality_proxy_weights,
    regime_filtered_mix_weights,
    value_proxy_weights,
    vol_targeted_mix_weights,
)
from usa_signal_bot.evidence.stats import deflated_sharpe_ratio, pbo_cscv
from usa_signal_bot.evidence.strategies import equal_weight_benchmark, momentum_weights, sma_trend_weights
from usa_signal_bot.evidence.universe import PointInTimeUniverse
from usa_signal_bot.evidence.walk_forward import WalkForwardConfig, WalkForwardResult, run_walk_forward

DISCLAIMER = (
    "Araştırma çıktısıdır; yatırım tavsiyesi değildir, kâr garantisi yoktur. Emir/broker/canlı bağlantı yok."
)


@dataclass
class StrategyEvidence:
    name: str
    oos: PerformanceSummary
    benchmark: PerformanceSummary
    sharpe_ci: tuple
    avg_annual_turnover: float
    n_folds: int
    verdict: str
    dsr: float = float("nan")  # Deflated Sharpe (prob. true SR > expected max of all trials); nan if not computed
    dsr_excess: float = float("nan")  # DSR of (OOS - benchmark) returns: is the outperformance itself significant?
    pbo: float = float("nan")  # CSCV probability of backtest overfitting over this family's candidates
    n_candidates: int = 0


@dataclass
class EvidenceReport:
    data_label: str
    n_symbols: int
    n_days: int
    price_issues: List[PriceIssue]
    cost: CostModel
    results: List[StrategyEvidence]
    survivorship_warning: bool
    n_trials_total: int = 0
    global_pbo: float = float("nan")

    def to_markdown(self) -> str:
        lines = ["# Strateji Kanıt Raporu (walk-forward, maliyet dahil)", "", f"> {DISCLAIMER}", ""]
        if self.data_label == "SYNTHETIC":
            lines += [
                "> **UYARI: SENTETİK VERİ.** Sonuçlar piyasa kanıtı DEĞİLDİR; yalnız boru hattının",
                "> sızıntısız ve deterministik çalıştığını doğrular. Gerçek veri için `evidence-run --source csv`.",
                "",
            ]
        lines += [
            f"- Veri: `{self.data_label}`, {self.n_symbols} sembol, {self.n_days} gün",
            f"- Maliyet: komisyon {self.cost.commission_bps} bps + kayma {self.cost.slippage_bps} bps (turnover başına)",
            f"- Fiyat doğrulama sorunu: {len(self.price_issues)}",
        ]
        if self.survivorship_warning:
            lines.append("- **Uyarı:** üyelik tablosu verilmedi; statik evren hayatta kalma yanlılığı içerir.")
        lines += [
            f"- Toplam denenen aday (DSR düzeltmesi için N): {self.n_trials_total}; tüm adaylar PBO ≈ {self.global_pbo:.2f}",
            "- `value`/`quality` aileleri fiyat-türevli VEKİLDİR (temel veri yok).",
        ]
        lines += ["", "| Strateji | OOS CAGR | OOS Sharpe | Sharpe %95 GA | DSR | DSR (kıyasa göre) | PBO | MaxDD | Yıllık turnover | Kıyas CAGR | Kıyas Sharpe | Karar |",
                  "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for r in self.results:
            lo, hi = r.sharpe_ci
            lines.append(
                f"| {r.name} | {r.oos.cagr:.1%} | {r.oos.sharpe:.2f} | [{lo:.2f}, {hi:.2f}] | {r.dsr:.2f} | {r.dsr_excess:.2f} | {r.pbo:.2f} | {r.oos.max_drawdown:.1%} "
                f"| {r.avg_annual_turnover:.1f} | {r.benchmark.cagr:.1%} | {r.benchmark.sharpe:.2f} | {r.verdict} |"
            )
        lines += [
            "",
            "Karar kuralı: `POZİTİF` yalnız OOS Sharpe %95 GA alt sınırı > 0, OOS CAGR **ve** Sharpe > kıyas, **ve** kıyasa göre fazla getirinin DSR'ı (tüm denenen adaylar için düzeltilmiş) ≥ 0,95 ise; "
            "OOS Sharpe ≤ 0 veya CAGR < kıyas ise `NEGATİF`; aksi halde `BELİRSİZ`. Negatif sonuç negatif yazılır.",
        ]
        return "\n".join(lines) + "\n"


def _verdict(oos: PerformanceSummary, bench: PerformanceSummary, ci: tuple, dsr_excess: float = 1.0) -> str:
    lo = ci[0]
    if oos.sharpe <= 0 or oos.cagr < bench.cagr or oos.sharpe < bench.sharpe:
        return "NEGATİF"
    if lo == lo and lo > 0 and dsr_excess == dsr_excess and dsr_excess >= 0.95:
        return "POZİTİF"
    return "BELİRSİZ"


def run_evidence(
    data: MarketData,
    cost: Optional[CostModel] = None,
    cfg: Optional[WalkForwardConfig] = None,
    seed: int = 0,
    families: Optional[List[str]] = None,
) -> EvidenceReport:
    cost = cost or CostModel()
    cfg = cfg or WalkForwardConfig()
    prices = data.prices
    universe = PointInTimeUniverse.from_frame(data.memberships)
    members = universe.membership_matrix(prices.index, prices.columns)
    issues = validate_adjusted_prices(prices, data.splits)
    bench_w = equal_weight_benchmark(prices, members)
    strategies: Dict[str, tuple] = {
        "SMA trend": (sma_trend_weights, [{"window": w} for w in (50, 100, 150, 200)]),
        "Momentum 12-1": (
            momentum_weights,
            [{"lookback": lb, "top_frac": tf} for lb in (126, 252) for tf in (0.2, 0.4)],
        ),
        "Düşük oynaklık": (low_vol_weights, [{"window": w} for w in (63, 126, 252)]),
        "Değer (vekil)": (value_proxy_weights, [{"window": w} for w in (126, 252)]),
        "Kalite (vekil)": (quality_proxy_weights, [{"window": w} for w in (126, 252)]),
        "Faktör karışımı": (factor_mix_weights, [{"window": w, "top_frac": tf} for w in (126, 252) for tf in (0.2, 0.4)]),
        "Karışım + rejim filtresi": (regime_filtered_mix_weights, [{"window": w} for w in (126, 252)]),
        "Karışım + vol hedefi": (vol_targeted_mix_weights, [{"window": 252, "target_vol_pct": v} for v in (8, 12)]),
    }
    if families:
        strategies = {k: v for k, v in strategies.items() if k in families}
    runs = {}
    for name, (fn, grid) in strategies.items():
        runs[name] = run_walk_forward(prices, members, fn, grid, cost, cfg, bench_w)
    n_total = sum(len(g) for _fn, g in strategies.values())
    all_trials = [wf.trial_returns for wf in runs.values() if not wf.trial_returns.empty]
    pooled = pd.concat(all_trials, axis=1) if all_trials else pd.DataFrame()
    srs = (pooled.mean() / pooled.std(ddof=1).replace(0, np.nan)).dropna() if not pooled.empty else pd.Series(dtype=float)
    var_sr = float(srs.var(ddof=1)) if len(srs) > 1 else None
    ex_trials = [wf.trial_returns.sub(wf.benchmark_returns, axis=0) for wf in runs.values() if not wf.trial_returns.empty]
    ex_pool = pd.concat(ex_trials, axis=1) if ex_trials else pd.DataFrame()
    ex_srs = (ex_pool.mean() / ex_pool.std(ddof=1).replace(0, np.nan)).dropna() if not ex_pool.empty else pd.Series(dtype=float)
    var_ex = float(ex_srs.var(ddof=1)) if len(ex_srs) > 1 else None
    global_pbo = float("nan")
    if pooled.shape[1] >= 2 and len(pooled) >= 16:
        global_pbo = pbo_cscv(pooled.dropna(axis=1).to_numpy(), 8).pbo
    results: List[StrategyEvidence] = []
    for name, wf in runs.items():
        oos = summarize(wf.oos_returns)
        bench = summarize(wf.benchmark_returns)
        ci = sharpe_ci(wf.oos_returns, seed=seed)
        dsr = float("nan")
        if len(wf.oos_returns.dropna()) >= 4:
            dsr = deflated_sharpe_ratio(wf.oos_returns.to_numpy(), max(n_total, 1), var_sr)
        dsr_ex = float("nan")
        excess = (wf.oos_returns - wf.benchmark_returns).dropna()
        if len(excess) >= 4:
            dsr_ex = deflated_sharpe_ratio(excess.to_numpy(), max(n_total, 1), var_ex)
        pbo = float("nan")
        t = wf.trial_returns.dropna(axis=1)
        if t.shape[1] >= 2 and len(t) >= 16:
            pbo = pbo_cscv(t.to_numpy(), 8).pbo
        results.append(
            StrategyEvidence(name, oos, bench, ci, wf.avg_turnover, len(wf.folds), _verdict(oos, bench, ci, dsr_ex),
                             dsr, dsr_ex, pbo, wf.trial_returns.shape[1])
        )
    return EvidenceReport(
        data.label, prices.shape[1], prices.shape[0], issues, cost, results,
        survivorship_warning=data.static_universe, n_trials_total=n_total, global_pbo=global_pbo,
    )
