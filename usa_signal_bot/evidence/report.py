"""Run the evidence pipeline end to end and render an honest markdown report."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import pandas as pd

from usa_signal_bot.evidence.corporate_actions import PriceIssue, validate_adjusted_prices
from usa_signal_bot.evidence.costs import CostModel
from usa_signal_bot.evidence.data import MarketData
from usa_signal_bot.evidence.metrics import PerformanceSummary, sharpe_ci, summarize
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


@dataclass
class EvidenceReport:
    data_label: str
    n_symbols: int
    n_days: int
    price_issues: List[PriceIssue]
    cost: CostModel
    results: List[StrategyEvidence]
    survivorship_warning: bool

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
        lines += ["", "| Strateji | OOS CAGR | OOS Sharpe | Sharpe %95 GA | MaxDD | Yıllık turnover | Kıyas CAGR | Kıyas Sharpe | Karar |",
                  "|---|---|---|---|---|---|---|---|---|"]
        for r in self.results:
            lo, hi = r.sharpe_ci
            lines.append(
                f"| {r.name} | {r.oos.cagr:.1%} | {r.oos.sharpe:.2f} | [{lo:.2f}, {hi:.2f}] | {r.oos.max_drawdown:.1%} "
                f"| {r.avg_annual_turnover:.1f} | {r.benchmark.cagr:.1%} | {r.benchmark.sharpe:.2f} | {r.verdict} |"
            )
        lines += [
            "",
            "Karar kuralı: `POZİTİF` yalnız OOS Sharpe %95 GA alt sınırı > 0 **ve** OOS CAGR > kıyas ise; "
            "OOS Sharpe ≤ 0 veya CAGR < kıyas ise `NEGATİF`; aksi halde `BELİRSİZ`. Negatif sonuç negatif yazılır.",
        ]
        return "\n".join(lines) + "\n"


def _verdict(oos: PerformanceSummary, bench: PerformanceSummary, ci: tuple) -> str:
    lo = ci[0]
    if oos.sharpe <= 0 or oos.cagr < bench.cagr:
        return "NEGATİF"
    if lo == lo and lo > 0:
        return "POZİTİF"
    return "BELİRSİZ"


def run_evidence(
    data: MarketData,
    cost: Optional[CostModel] = None,
    cfg: Optional[WalkForwardConfig] = None,
    seed: int = 0,
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
    }
    results: List[StrategyEvidence] = []
    for name, (fn, grid) in strategies.items():
        wf: WalkForwardResult = run_walk_forward(prices, members, fn, grid, cost, cfg, bench_w)
        oos = summarize(wf.oos_returns)
        bench = summarize(wf.benchmark_returns)
        ci = sharpe_ci(wf.oos_returns, seed=seed)
        results.append(StrategyEvidence(name, oos, bench, ci, wf.avg_turnover, len(wf.folds), _verdict(oos, bench, ci)))
    return EvidenceReport(
        data.label, prices.shape[1], prices.shape[0], issues, cost, results,
        survivorship_warning=data.static_universe,
    )
