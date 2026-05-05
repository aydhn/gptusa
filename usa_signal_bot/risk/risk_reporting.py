from pathlib import Path
from usa_signal_bot.risk.risk_models import RiskDecision, RiskRunResult, RiskCheckResult
from usa_signal_bot.risk.risk_limits import RiskLimitConfig
from usa_signal_bot.risk.position_sizing import PositionSizingConfig
from usa_signal_bot.risk.exposure_guard import ExposureSnapshot
from usa_signal_bot.risk.risk_validation import RiskValidationReport
from usa_signal_bot.core.enums import RiskDecisionStatus

def risk_limit_config_to_text(config: RiskLimitConfig) -> str:
    lines = [
        "=== Risk Limit Configuration ===",
        f"Max Position Notional: {config.max_position_notional}",
        f"Max Position % Equity: {config.max_position_pct_equity:.2%}",
        f"Max Symbol Exposure: {config.max_symbol_exposure_pct:.2%}",
        f"Max Strategy Exposure: {config.max_strategy_exposure_pct:.2%}",
        f"Max Portfolio Exposure: {config.max_portfolio_exposure_pct:.2%}",
        f"Max Open Positions: {config.max_open_positions}",
        f"Min Cash Buffer: {config.min_cash_buffer_pct:.2%}",
        f"Allow Short: {config.allow_short}",
        f"Max Candidate Risk Score: {config.max_candidate_risk_score}"
    ]
    return "\n".join(lines)

def position_sizing_config_to_text(config: PositionSizingConfig) -> str:
    lines = [
        "=== Position Sizing Configuration ===",
        f"Method: {config.method.value}",
        f"Fixed Notional: {config.fixed_notional}",
        f"Fixed Fraction: {config.fixed_fraction_pct:.2%}",
        f"Risk Per Trade: {config.risk_per_trade_pct:.2%}",
        f"ATR Multiplier: {config.atr_multiplier}",
        f"Target Volatility: {config.volatility_target_pct:.2%}",
        f"Min Notional: {config.min_notional}",
        f"Max Notional: {config.max_notional}",
        f"Allow Fractional Qty: {config.allow_fractional_quantity}"
    ]
    return "\n".join(lines)

def risk_checks_to_text(checks: list[RiskCheckResult]) -> str:
    lines = []
    for c in checks:
        lines.append(f"  [{c.severity.value}] {c.check_name} -> {c.status.value}: {c.message}")
    return "\n".join(lines)

def risk_decision_to_text(decision: RiskDecision) -> str:
    lines = [
        f"Candidate: {decision.symbol} | {decision.strategy_name} | {decision.timeframe}",
        f"Status: {decision.status.value} (Score: {decision.risk_score:.1f})",
        f"Approved Notional: {decision.approved_notional:.2f} (Qty: {decision.approved_quantity:.2f})"
    ]
    if decision.notes:
        lines.append("Notes: " + ", ".join(decision.notes))
    if decision.rejection_reasons:
        lines.append("Rejection Reasons: " + ", ".join(r.value for r in decision.rejection_reasons))

    return "\n".join(lines)

def risk_run_result_to_text(result: RiskRunResult, limit: int = 30) -> str:
    lines = [
        "=== Risk Run Result ===",
        f"Run ID: {result.run_id}",
        f"Status: {result.status.value}",
        f"Total Candidates: {result.total_candidates}",
        f"Approved: {result.approved_count}",
        f"Rejected: {result.rejected_count}",
        f"Reduced: {result.reduced_count}",
        f"Needs Review: {result.needs_review_count}",
        "",
        "--- Top Decisions ---"
    ]

    for d in result.decisions[:limit]:
        lines.append(risk_decision_to_text(d))
        lines.append("-")

    if len(result.decisions) > limit:
        lines.append(f"... and {len(result.decisions) - limit} more.")

    lines.append("")
    lines.append(risk_limitations_text())
    return "\n".join(lines)

def exposure_snapshot_report_to_text(snapshot: ExposureSnapshot) -> str:
    from usa_signal_bot.risk.exposure_guard import exposure_snapshot_to_text
    return exposure_snapshot_to_text(snapshot)

def risk_limitations_text() -> str:
    return (
        "*** DISCLAIMER ***\n"
        "Risk approval is strictly for research, backtest, and paper environments.\n"
        "It is NOT live trade approval. Position sizing is NOT financial advice.\n"
        "No live execution will be performed by this module."
    )

def write_risk_report_json(path: Path, result: RiskRunResult, validation_report: RiskValidationReport | None = None) -> Path:
    import json
    from usa_signal_bot.risk.risk_models import risk_run_result_to_dict

    data = {
        "run_summary": risk_run_result_to_dict(result),
        "validation": validation_report.__dict__ if validation_report else None,
        "disclaimer": risk_limitations_text()
    }
    p = path / "risk_report.json"
    with open(p, "w", encoding="utf-8") as f:
         json.dump(data, f, indent=2)
    return p
