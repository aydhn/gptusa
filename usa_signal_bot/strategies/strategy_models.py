from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import uuid
import datetime
from usa_signal_bot.core.enums import StrategyRunStatus, SignalAction
from usa_signal_bot.strategies.signal_contract import StrategySignal, signal_to_dict

@dataclass
class StrategyRunContext:
    run_id: str
    strategy_name: str
    provider_name: str
    symbols: List[str]
    timeframes: List[str]
    created_at_utc: str
    universe_name: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class StrategyRunResult:
    run_id: str
    strategy_name: str
    status: StrategyRunStatus
    signals: List[StrategySignal]
    symbols_processed: List[str]
    timeframes_processed: List[str]
    warnings: List[str]
    errors: List[str]
    created_at_utc: str

@dataclass
class StrategyExecutionSummary:
    run_id: str
    strategy_name: str
    total_signals: int
    long_count: int
    short_count: int
    flat_count: int
    watch_count: int
    avoid_count: int
    warnings: List[str]
    errors: List[str]
    average_confidence: Optional[float] = None

def create_strategy_run_id(strategy_name: str) -> str:
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%md%H%M%S")
    uid = str(uuid.uuid4())[:8]
    return f"{strategy_name}_{timestamp}_{uid}"

def strategy_run_result_to_dict(result: StrategyRunResult) -> dict:
    return {
        "run_id": result.run_id,
        "strategy_name": result.strategy_name,
        "status": result.status.value if isinstance(result.status, StrategyRunStatus) else result.status,
        "signals": [signal_to_dict(s) for s in result.signals],
        "symbols_processed": result.symbols_processed,
        "timeframes_processed": result.timeframes_processed,
        "warnings": result.warnings,
        "errors": result.errors,
        "created_at_utc": result.created_at_utc
    }

def summarize_strategy_run(result: StrategyRunResult) -> StrategyExecutionSummary:
    long_count = sum(1 for s in result.signals if s.action == SignalAction.LONG)
    short_count = sum(1 for s in result.signals if s.action == SignalAction.SHORT)
    flat_count = sum(1 for s in result.signals if s.action == SignalAction.FLAT)
    watch_count = sum(1 for s in result.signals if s.action == SignalAction.WATCH)
    avoid_count = sum(1 for s in result.signals if s.action == SignalAction.AVOID)

    avg_conf = None
    if result.signals:
        avg_conf = sum(s.confidence for s in result.signals) / len(result.signals)

    return StrategyExecutionSummary(
        run_id=result.run_id,
        strategy_name=result.strategy_name,
        total_signals=len(result.signals),
        long_count=long_count,
        short_count=short_count,
        flat_count=flat_count,
        watch_count=watch_count,
        avoid_count=avoid_count,
        warnings=result.warnings,
        errors=result.errors,
        average_confidence=avg_conf
    )
