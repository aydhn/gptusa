from typing import Any, Dict, List, Optional
from usa_signal_bot.diagnostics.diagnostic_models import (
    DiagnosticEvent, StrategyDiagnosticResult, FailureModeAssessment, FailureCluster, create_strategy_diagnostic_result_id
)
from usa_signal_bot.core.enums import DiagnosticStatus, DiagnosticSeverity
from usa_signal_bot.diagnostics.loss_event_analysis import filter_losing_events, loss_assessments_by_dimension, detect_repeated_loss_patterns
from datetime import datetime, timezone

def diagnose_strategy(strategy_name: str, events: List[DiagnosticEvent]) -> StrategyDiagnosticResult:
    strategy_events = [e for e in events if e.strategy_name == strategy_name]

    if not strategy_events:
        return StrategyDiagnosticResult(
            diagnostic_id=create_strategy_diagnostic_result_id(strategy_name),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            strategy_name=strategy_name,
            status=DiagnosticStatus.INSUFFICIENT_DATA,
            severity=DiagnosticSeverity.INSUFFICIENT_DATA,
            event_count=0,
            trade_count=0
        )

    trades = [e for e in strategy_events if e.scope.value == "TRADE" and e.net_pnl_usd is not None]
    trade_count = len(trades)

    wins = [t for t in trades if t.net_pnl_usd > 0]
    win_rate = (len(wins) / trade_count * 100) if trade_count > 0 else None

    total_net = sum(e.net_pnl_usd for e in trades) if trades else None
    total_cost = sum(e.total_cost_usd for e in trades if e.total_cost_usd is not None)
    gross_pnl = sum(e.gross_pnl_usd for e in trades if e.gross_pnl_usd is not None and e.gross_pnl_usd > 0)

    cost_drag_pct = (total_cost / gross_pnl * 100) if gross_pnl and gross_pnl > 0 and total_cost else None

    # Dummy calls, could be expanded to use other specific modules
    failure_modes = loss_assessments_by_dimension(strategy_events, "symbol")
    clusters = detect_repeated_loss_patterns(strategy_events)

    status = DiagnosticStatus.HEALTHY
    severity = DiagnosticSeverity.INFO

    if trade_count < 10:
        status = DiagnosticStatus.WATCH
        severity = DiagnosticSeverity.INFO
    elif total_net is not None and total_net < 0:
        status = DiagnosticStatus.FAILING
        severity = DiagnosticSeverity.HIGH
    elif win_rate is not None and win_rate < 40.0:
        status = DiagnosticStatus.DEGRADED
        severity = DiagnosticSeverity.MODERATE

    return StrategyDiagnosticResult(
        diagnostic_id=create_strategy_diagnostic_result_id(strategy_name),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        strategy_name=strategy_name,
        status=status,
        severity=severity,
        event_count=len(strategy_events),
        trade_count=trade_count,
        win_rate=win_rate,
        total_net_pnl_usd=total_net,
        total_cost_usd=total_cost,
        cost_drag_pct=cost_drag_pct,
        failure_modes=failure_modes,
        clusters=clusters,
        remediation_hints=[]
    )

def diagnose_strategies(events: List[DiagnosticEvent]) -> List[StrategyDiagnosticResult]:
    strategies = set(e.strategy_name for e in events if e.strategy_name)
    return [diagnose_strategy(s, events) for s in strategies]

def strategy_failure_modes(strategy_name: str, events: List[DiagnosticEvent]) -> List[FailureModeAssessment]:
    res = diagnose_strategy(strategy_name, events)
    return res.failure_modes

def strategy_failure_clusters(strategy_name: str, events: List[DiagnosticEvent]) -> List[FailureCluster]:
    res = diagnose_strategy(strategy_name, events)
    return res.clusters

def classify_strategy_diagnostic_status(result: StrategyDiagnosticResult) -> DiagnosticStatus:
    return result.status

def strategy_diagnostics_to_text(results: List[StrategyDiagnosticResult], limit: int = 50) -> str:
    lines = [f"Strategy Diagnostics (Total: {len(results)}, Showing top {min(len(results), limit)}):"]
    for res in results[:limit]:
        lines.append(f"  [{res.strategy_name}] Status: {res.status.value} | Severity: {res.severity.value} | Win Rate: {res.win_rate}% | Net PnL: {res.total_net_pnl_usd}")
    return "\n".join(lines)
