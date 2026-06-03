import datetime

from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    MonteCarloDistributionSummary,
    MonteCarloReplayResult,
    ScenarioReplayResult,
    TailRiskDiagnostic,
    create_tail_risk_diagnostic_id
)
from usa_signal_bot.core.enums import TailRiskDiagnosticKind

def build_tail_risk_diagnostics(distribution: MonteCarloDistributionSummary, results: list[MonteCarloReplayResult], scenario_results: list[ScenarioReplayResult] | None = None) -> list[TailRiskDiagnostic]:
    diags = []

    # Left tail return
    diags.append(_create_diag(
        TailRiskDiagnosticKind.LEFT_TAIL_RETURN,
        distribution.return_p05,
        infer_tail_risk_severity(distribution.return_p05, TailRiskDiagnosticKind.LEFT_TAIL_RETURN)
    ))

    # Worst path drawdown
    worst_dd = max([r.max_drawdown for r in results if r.max_drawdown is not None], default=None)
    diags.append(_create_diag(
        TailRiskDiagnosticKind.WORST_PATH_DRAWDOWN,
        worst_dd,
        infer_tail_risk_severity(worst_dd, TailRiskDiagnosticKind.WORST_PATH_DRAWDOWN)
    ))

    # Ruin
    diags.append(_create_diag(
        TailRiskDiagnosticKind.RUIN_PROBABILITY_APPROX,
        distribution.ruin_probability_approx,
        infer_tail_risk_severity(distribution.ruin_probability_approx, TailRiskDiagnosticKind.RUIN_PROBABILITY_APPROX)
    ))

    return diags

def _create_diag(kind: TailRiskDiagnosticKind, value: Any, severity: str) -> TailRiskDiagnostic:
    return TailRiskDiagnostic(
        diagnostic_id=create_tail_risk_diagnostic_id(),
        created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
        diagnostic_kind=kind,
        value=value,
        severity_label=severity,
        diagnostic_notes=[],
        diagnostic_valid=True,
        not_investment_advice=True,
        not_strategy_activation=True,
        research_data_only=True,
        warnings=[], errors=[], risk_flags=[], metadata={}
    )

def infer_tail_risk_severity(value: float | None, diagnostic_kind: TailRiskDiagnosticKind) -> str:
    if value is None:
        return "UNKNOWN"
    if diagnostic_kind == TailRiskDiagnosticKind.LEFT_TAIL_RETURN:
        if value < -0.3: return "SEVERE"
        if value < -0.15: return "WARNING"
        return "ACCEPTABLE"
    if diagnostic_kind == TailRiskDiagnosticKind.WORST_PATH_DRAWDOWN:
        if value > 0.5: return "SEVERE"
        if value > 0.3: return "WARNING"
        return "ACCEPTABLE"
    if diagnostic_kind == TailRiskDiagnosticKind.RUIN_PROBABILITY_APPROX:
        if value > 0.05: return "SEVERE"
        if value > 0.01: return "WARNING"
        return "ACCEPTABLE"
    return "UNKNOWN"
