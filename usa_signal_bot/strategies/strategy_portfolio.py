"""Strategy portfolio aggregation system."""

import datetime
import uuid
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from usa_signal_bot.core.enums import StrategyPortfolioMode, SignalCollapseMode
from usa_signal_bot.core.exceptions import StrategyPortfolioError
from usa_signal_bot.strategies.strategy_models import StrategyRunResult
from usa_signal_bot.strategies.signal_confluence import ConfluenceReport, evaluate_confluence
from usa_signal_bot.strategies.signal_ranking import SignalRankingReport, SignalRankingConfig, rank_signals
from usa_signal_bot.strategies.signal_aggregation import SignalAggregationReport, aggregate_signals, collapse_ranked_signals
from usa_signal_bot.strategies.candidate_selection import CandidateSelectionReport, CandidateSelectionConfig, select_candidates, get_selected_signals
from usa_signal_bot.strategies.signal_contract import StrategySignal

@dataclass
class StrategyPortfolioConfig:
    mode: StrategyPortfolioMode = StrategyPortfolioMode.RESEARCH_POOL
    strategy_names: List[str] = field(default_factory=list)
    max_candidates: int = 20
    max_per_strategy: int = 10
    max_per_symbol: int = 1
    require_confluence: bool = False
    min_confluence_score: Optional[float] = None
    diversify_by_strategy: bool = True

def default_strategy_portfolio_config(strategy_names: Optional[List[str]] = None) -> StrategyPortfolioConfig:
    return StrategyPortfolioConfig(strategy_names=strategy_names or [])

def validate_strategy_portfolio_config(config: StrategyPortfolioConfig) -> None:
    if config.max_candidates <= 0:
        raise StrategyPortfolioError("max_candidates must be positive.")
    if config.max_per_strategy <= 0:
        raise StrategyPortfolioError("max_per_strategy must be positive.")
    if config.max_per_symbol <= 0:
        raise StrategyPortfolioError("max_per_symbol must be positive.")

@dataclass
class StrategyPortfolioRun:
    run_id: str
    created_at_utc: str
    mode: StrategyPortfolioMode
    strategy_names: List[str]
    signal_count: int
    ranked_count: int
    selected_count: int
    confluence_report_path: Optional[str] = None
    ranking_report_path: Optional[str] = None
    selection_report_path: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

@dataclass
class StrategyPortfolioAggregationResult:
    portfolio_run: StrategyPortfolioRun
    strategy_results: List[StrategyRunResult]
    confluence_report: Optional[ConfluenceReport]
    ranking_report: SignalRankingReport
    aggregation_report: SignalAggregationReport
    selection_report: CandidateSelectionReport
    selected_signals: List[StrategySignal]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def aggregate_strategy_portfolio_results(
    strategy_results: List[StrategyRunResult],
    confluence_report: Optional[ConfluenceReport] = None,
    ranking_config: Optional[SignalRankingConfig] = None,
    selection_config: Optional[CandidateSelectionConfig] = None
) -> StrategyPortfolioAggregationResult:

    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    run_id = f"port_{uuid.uuid4().hex[:8]}"
    warnings = []

    all_signals = []
    strategy_names = set()
    for res in strategy_results:
        if hasattr(res, 'quality_report') and res.quality_report:
            for sig in res.signals:
                if sig.quality_status != "REJECTED":
                    all_signals.append(sig)
        else:
            all_signals.extend(res.signals)
        strategy_names.add(res.strategy_name)

    if confluence_report:
        for cr in confluence_report.group_results:
            for sig in all_signals:
                if sig.symbol == cr.symbol and sig.timeframe == cr.timeframe:
                    sig.confluence_score = cr.confluence_score
                    sig.confluence_direction = cr.direction

    ranking_report = rank_signals(all_signals, ranking_config)

    agg_mode = selection_config.collapse_mode if selection_config else None # type: ignore
    mode = SignalCollapseMode[agg_mode.upper()] if isinstance(agg_mode, str) else (agg_mode if agg_mode else SignalCollapseMode.BEST_PER_SYMBOL_TIMEFRAME)

    agg_report = aggregate_signals(all_signals, ranking_report.ranked_signals, collapse_mode=mode)

    collapsed_ranked = collapse_ranked_signals(agg_report)
    ranking_report.ranked_signals = collapsed_ranked
    ranking_report.ranked_count = len([rs for rs in collapsed_ranked if rs.ranking_status.value != "FILTERED"])

    selection_report = select_candidates(ranking_report, selection_config)
    selected_signals = get_selected_signals(selection_report)

    port_run = StrategyPortfolioRun(
        run_id=run_id,
        created_at_utc=now_utc,
        mode=StrategyPortfolioMode.RESEARCH_POOL,
        strategy_names=list(strategy_names),
        signal_count=len(all_signals),
        ranked_count=ranking_report.ranked_count,
        selected_count=selection_report.selected_count,
        warnings=warnings
    )

    return StrategyPortfolioAggregationResult(
        portfolio_run=port_run,
        strategy_results=strategy_results,
        confluence_report=confluence_report,
        ranking_report=ranking_report,
        aggregation_report=agg_report,
        selection_report=selection_report,
        selected_signals=selected_signals,
        warnings=warnings
    )

def strategy_portfolio_result_to_text(result: StrategyPortfolioAggregationResult, limit: int = 20) -> str:
    lines = [
        f"--- Strategy Portfolio Aggregation ({result.portfolio_run.run_id}) ---",
        f"Strategies: {', '.join(result.portfolio_run.strategy_names)}",
        f"Signals: {result.portfolio_run.signal_count} | Ranked: {result.portfolio_run.ranked_count} | Selected: {result.portfolio_run.selected_count}",
        ""
    ]

    if result.warnings:
        lines.append("WARNINGS:")
        for w in result.warnings:
            lines.append(f"  - {w}")
        lines.append("")

    if result.selection_report.selected_candidates:
        lines.append(f"Top {limit} Selected Candidates:")
        for i, c in enumerate(result.selection_report.selected_candidates[:limit]):
            rs = c.ranked_signal
            lines.append(f"  {c.selection_rank}. {rs.signal.symbol} [{rs.signal.timeframe}] {rs.signal.action.value} - Score: {rs.rank_score:.2f} (Str: {rs.signal.strategy_name})")

    return "\n".join(lines)

def write_strategy_portfolio_run_json(path: Path, run: StrategyPortfolioRun) -> Path:
    from usa_signal_bot.core.serialization import serialize_value
    import dataclasses

    path.parent.mkdir(parents=True, exist_ok=True)

    data = dataclasses.asdict(run)

    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=serialize_value)

    return path

def write_strategy_portfolio_result_json(path: Path, result: StrategyPortfolioAggregationResult) -> Path:
    from usa_signal_bot.core.serialization import serialize_value

    path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "run_id": result.portfolio_run.run_id,
        "created_at_utc": result.portfolio_run.created_at_utc,
        "strategies": result.portfolio_run.strategy_names,
        "signal_count": result.portfolio_run.signal_count,
        "selected_count": result.portfolio_run.selected_count,
        "selected_candidates": [
            {
                "symbol": s.symbol,
                "timeframe": s.timeframe,
                "action": s.action.value,
                "strategy": s.strategy_name
            } for s in result.selected_signals
        ]
    }

    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=serialize_value)

    return path
