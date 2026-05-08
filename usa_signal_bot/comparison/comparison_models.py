from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional
import uuid
from datetime import datetime, timezone

from usa_signal_bot.core.enums import (
    ComparisonStatus,
    ComparisonSourceType,
    MatchStatus,
    ComparisonMetricStatus,
    ExecutionRealismBucket,
    SignalDriftStatus,
    GapSeverity,
    GapDirection,
    ComparisonReportType
)

@dataclass
class ComparisonRunRequest:
    request_id: str
    report_type: ComparisonReportType
    paper_run_id: Optional[str] = None
    paper_run_dir: Optional[str] = None
    backtest_run_id: Optional[str] = None
    backtest_run_dir: Optional[str] = None
    basket_run_id: Optional[str] = None
    basket_run_dir: Optional[str] = None
    scan_run_id: Optional[str] = None
    scan_run_dir: Optional[str] = None
    signal_file: Optional[str] = None
    candidate_file: Optional[str] = None
    symbol_filter: Optional[List[str]] = None
    timeframe_filter: Optional[List[str]] = None
    matching_tolerance_bars: int = 1
    price_gap_warning_pct: float = 1.0
    timing_gap_warning_bars: int = 1
    write_outputs: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ComparisonSourceSummary:
    source_type: ComparisonSourceType
    source_id: Optional[str]
    source_path: Optional[str]
    record_count: int
    symbols: List[str]
    timeframes: List[str]
    warnings: List[str]
    errors: List[str]

@dataclass
class MatchedTradePair:
    match_id: str
    symbol: str
    timeframe: str
    strategy_name: Optional[str]
    paper_trade_id: Optional[str]
    backtest_trade_id: Optional[str]
    match_status: MatchStatus
    paper_entry_time: Optional[str]
    backtest_entry_time: Optional[str]
    paper_exit_time: Optional[str]
    backtest_exit_time: Optional[str]
    paper_entry_price: Optional[float]
    backtest_entry_price: Optional[float]
    paper_exit_price: Optional[float]
    backtest_exit_price: Optional[float]
    paper_net_pnl: Optional[float]
    backtest_net_pnl: Optional[float]
    pnl_gap: Optional[float]
    return_gap_pct: Optional[float]
    timing_gap_bars: Optional[int]
    price_gap_pct: Optional[float]
    warnings: List[str]
    errors: List[str]

@dataclass
class PerformanceGapMetrics:
    status: ComparisonMetricStatus
    paper_total_return_pct: Optional[float]
    backtest_total_return_pct: Optional[float]
    total_return_gap_pct: Optional[float]
    paper_max_drawdown_pct: Optional[float]
    backtest_max_drawdown_pct: Optional[float]
    drawdown_gap_pct: Optional[float]
    paper_win_rate: Optional[float]
    backtest_win_rate: Optional[float]
    win_rate_gap: Optional[float]
    paper_profit_factor: Optional[float]
    backtest_profit_factor: Optional[float]
    profit_factor_gap: Optional[float]
    paper_trade_count: int
    backtest_trade_count: int
    trade_count_gap: int
    gap_direction: GapDirection
    warnings: List[str]
    errors: List[str]

@dataclass
class ExecutionGapMetrics:
    status: ComparisonMetricStatus
    matched_trade_count: int
    unmatched_paper_count: int
    unmatched_backtest_count: int
    average_entry_price_gap_pct: Optional[float]
    average_exit_price_gap_pct: Optional[float]
    average_timing_gap_bars: Optional[float]
    average_pnl_gap: Optional[float]
    total_fee_gap: Optional[float]
    total_slippage_gap: Optional[float]
    missing_fill_count: int
    execution_realism_score: Optional[float]
    execution_realism_bucket: ExecutionRealismBucket
    warnings: List[str]
    errors: List[str]

@dataclass
class SignalDriftMetrics:
    status: ComparisonMetricStatus
    compared_signal_count: int
    missing_signal_count: int
    changed_signal_count: int
    changed_candidate_count: int
    score_drift_average: Optional[float]
    confidence_drift_average: Optional[float]
    rank_drift_average: Optional[float]
    feature_drift_average: Optional[float]
    drift_status: SignalDriftStatus
    warnings: List[str]
    errors: List[str]

@dataclass
class ComparisonRunResult:
    run_id: str
    created_at_utc: str
    status: ComparisonStatus
    request: ComparisonRunRequest
    paper_source: Optional[ComparisonSourceSummary]
    backtest_source: Optional[ComparisonSourceSummary]
    scan_source: Optional[ComparisonSourceSummary]
    matched_trades: List[MatchedTradePair]
    performance_gap: PerformanceGapMetrics
    execution_gap: ExecutionGapMetrics
    signal_drift: Optional[SignalDriftMetrics]
    execution_realism_bucket: ExecutionRealismBucket
    overall_gap_severity: GapSeverity
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

def comparison_run_request_to_dict(request: ComparisonRunRequest) -> dict:
    from dataclasses import asdict
    d = asdict(request)
    if isinstance(d.get("report_type"), ComparisonReportType):
        d["report_type"] = d["report_type"].value
    return d

def comparison_source_summary_to_dict(summary: ComparisonSourceSummary) -> dict:
    from dataclasses import asdict
    d = asdict(summary)
    if isinstance(d.get("source_type"), ComparisonSourceType):
        d["source_type"] = d["source_type"].value
    return d

def matched_trade_pair_to_dict(pair: MatchedTradePair) -> dict:
    from dataclasses import asdict
    d = asdict(pair)
    if isinstance(d.get("match_status"), MatchStatus):
        d["match_status"] = d["match_status"].value
    return d

def performance_gap_metrics_to_dict(metrics: PerformanceGapMetrics) -> dict:
    from dataclasses import asdict
    d = asdict(metrics)
    if isinstance(d.get("status"), ComparisonMetricStatus):
        d["status"] = d["status"].value
    if isinstance(d.get("gap_direction"), GapDirection):
        d["gap_direction"] = d["gap_direction"].value
    return d

def execution_gap_metrics_to_dict(metrics: ExecutionGapMetrics) -> dict:
    from dataclasses import asdict
    d = asdict(metrics)
    if isinstance(d.get("status"), ComparisonMetricStatus):
        d["status"] = d["status"].value
    if isinstance(d.get("execution_realism_bucket"), ExecutionRealismBucket):
        d["execution_realism_bucket"] = d["execution_realism_bucket"].value
    return d

def signal_drift_metrics_to_dict(metrics: SignalDriftMetrics) -> dict:
    from dataclasses import asdict
    d = asdict(metrics)
    if isinstance(d.get("status"), ComparisonMetricStatus):
        d["status"] = d["status"].value
    if isinstance(d.get("drift_status"), SignalDriftStatus):
        d["drift_status"] = d["drift_status"].value
    return d

def comparison_run_result_to_dict(result: ComparisonRunResult) -> dict:
    from dataclasses import asdict
    d = asdict(result)
    d["request"] = comparison_run_request_to_dict(result.request)
    if result.paper_source:
        d["paper_source"] = comparison_source_summary_to_dict(result.paper_source)
    if result.backtest_source:
        d["backtest_source"] = comparison_source_summary_to_dict(result.backtest_source)
    if result.scan_source:
        d["scan_source"] = comparison_source_summary_to_dict(result.scan_source)
    d["matched_trades"] = [matched_trade_pair_to_dict(p) for p in result.matched_trades]
    if result.performance_gap:
        d["performance_gap"] = performance_gap_metrics_to_dict(result.performance_gap)
    if result.execution_gap:
        d["execution_gap"] = execution_gap_metrics_to_dict(result.execution_gap)
    if result.signal_drift:
        d["signal_drift"] = signal_drift_metrics_to_dict(result.signal_drift)
    if isinstance(d.get("status"), ComparisonStatus):
        d["status"] = d["status"].value
    if isinstance(d.get("execution_realism_bucket"), ExecutionRealismBucket):
        d["execution_realism_bucket"] = d["execution_realism_bucket"].value
    if isinstance(d.get("overall_gap_severity"), GapSeverity):
        d["overall_gap_severity"] = d["overall_gap_severity"].value
    return d

def validate_comparison_run_request(request: ComparisonRunRequest) -> None:
    if not request.request_id:
        raise ValueError("request_id cannot be empty")
    if not request.paper_run_id and not request.paper_run_dir and not request.signal_file and not request.candidate_file:
        raise ValueError("Must provide at least one paper/signal source")

def validate_matched_trade_pair(pair: MatchedTradePair) -> None:
    if not pair.match_id:
        raise ValueError("match_id cannot be empty")
    if not pair.symbol:
        raise ValueError("symbol cannot be empty")

def validate_comparison_run_result(result: ComparisonRunResult) -> None:
    if not result.run_id:
        raise ValueError("run_id cannot be empty")

def create_comparison_request_id(prefix: str = "comparison_req") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_comparison_run_id(prefix: str = "comparison") -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}_{uuid.uuid4().hex[:4]}"

def create_trade_match_id(symbol: str, paper_trade_id: Optional[str], backtest_trade_id: Optional[str]) -> str:
    p_id = paper_trade_id or "none"
    b_id = backtest_trade_id or "none"
    return f"match_{symbol}_{p_id}_{b_id}_{uuid.uuid4().hex[:4]}"

@dataclass
class SignalSnapshot:
    snapshot_id: str
    signal_id: Optional[str]
    candidate_id: Optional[str]
    symbol: str
    timeframe: str
    strategy_name: Optional[str]
    action: Optional[str]
    score: Optional[float]
    confidence: Optional[float]
    rank_score: Optional[float]
    feature_snapshot: Dict[str, Any]
    created_at_utc: Optional[str]
    source: Optional[str] = None

@dataclass
class SignalDriftPair:
    pair_id: str
    symbol: str
    timeframe: str
    original_snapshot_id: Optional[str]
    replay_snapshot_id: Optional[str]
    drift_status: SignalDriftStatus
    score_gap: Optional[float]
    confidence_gap: Optional[float]
    rank_gap: Optional[float]
    feature_gap_score: Optional[float]
    changed_action: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
