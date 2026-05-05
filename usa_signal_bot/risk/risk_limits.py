from dataclasses import dataclass
from typing import Any

from usa_signal_bot.core.enums import (
    ExposureLimitType,
    RiskSeverity,
    RiskCheckStatus,
    RiskRejectionReason,
    SignalAction
)
from usa_signal_bot.core.exceptions import RiskLimitError
from usa_signal_bot.risk.risk_models import RiskLimit, RiskCheckResult

@dataclass
class RiskLimitConfig:
    max_position_notional: float
    max_position_pct_equity: float
    max_symbol_exposure_pct: float
    max_strategy_exposure_pct: float
    max_portfolio_exposure_pct: float
    max_open_positions: int
    min_cash_buffer_pct: float
    allow_short: bool
    max_candidate_risk_score: float

def default_risk_limit_config() -> RiskLimitConfig:
    return RiskLimitConfig(
        max_position_notional=10000.0,
        max_position_pct_equity=0.10,
        max_symbol_exposure_pct=0.15,
        max_strategy_exposure_pct=0.30,
        max_portfolio_exposure_pct=0.80,
        max_open_positions=10,
        min_cash_buffer_pct=0.05,
        allow_short=False,
        max_candidate_risk_score=70.0
    )

def validate_risk_limit_config(config: RiskLimitConfig) -> None:
    if config.max_position_notional < 0:
        raise RiskLimitError("max_position_notional cannot be negative")
    for pct in [config.max_position_pct_equity, config.max_symbol_exposure_pct,
                config.max_strategy_exposure_pct, config.max_portfolio_exposure_pct,
                config.min_cash_buffer_pct]:
        if not (0 <= pct <= 1):
            raise RiskLimitError("Percentage limits must be between 0 and 1")
    if config.max_open_positions <= 0:
        raise RiskLimitError("max_open_positions must be positive")

def build_default_risk_limits(config: RiskLimitConfig | None = None) -> list[RiskLimit]:
    cfg = config or default_risk_limit_config()
    return [
        RiskLimit("max_portfolio_exposure", ExposureLimitType.PORTFOLIO, cfg.max_portfolio_exposure_pct, severity=RiskSeverity.CRITICAL),
        RiskLimit("max_symbol_exposure", ExposureLimitType.SYMBOL, cfg.max_symbol_exposure_pct, severity=RiskSeverity.HIGH),
        RiskLimit("max_strategy_exposure", ExposureLimitType.STRATEGY, cfg.max_strategy_exposure_pct, severity=RiskSeverity.HIGH),
    ]

def check_max_position_notional(notional: float, config: RiskLimitConfig) -> RiskCheckResult:
    if notional > config.max_position_notional:
        return RiskCheckResult(
            check_name="max_position_notional",
            status=RiskCheckStatus.WARNING,
            severity=RiskSeverity.MODERATE,
            message=f"Notional {notional:.2f} exceeds max {config.max_position_notional:.2f}",
            rejection_reason=RiskRejectionReason.MAX_POSITION_SIZE_EXCEEDED,
            observed_value=notional,
            limit_value=config.max_position_notional
        )
    return RiskCheckResult("max_position_notional", RiskCheckStatus.PASSED, RiskSeverity.INFO, "Passed", observed_value=notional)

def check_max_position_pct_equity(notional: float, equity: float, config: RiskLimitConfig) -> RiskCheckResult:
    if equity <= 0:
        return RiskCheckResult("max_position_pct_equity", RiskCheckStatus.FAILED, RiskSeverity.CRITICAL, "Equity <= 0", observed_value=equity)
    pct = notional / equity
    if pct > config.max_position_pct_equity:
        return RiskCheckResult(
            check_name="max_position_pct_equity",
            status=RiskCheckStatus.WARNING,
            severity=RiskSeverity.MODERATE,
            message=f"Position size {pct:.2%} exceeds max {config.max_position_pct_equity:.2%}",
            rejection_reason=RiskRejectionReason.MAX_POSITION_SIZE_EXCEEDED,
            observed_value=pct,
            limit_value=config.max_position_pct_equity
        )
    return RiskCheckResult("max_position_pct_equity", RiskCheckStatus.PASSED, RiskSeverity.INFO, "Passed", observed_value=pct)

def check_symbol_exposure(symbol: str, proposed_notional: float, current_symbol_exposure: float, equity: float, config: RiskLimitConfig) -> RiskCheckResult:
    if equity <= 0:
        return RiskCheckResult("symbol_exposure", RiskCheckStatus.FAILED, RiskSeverity.CRITICAL, "Equity <= 0")
    total_exposure = (current_symbol_exposure + proposed_notional) / equity
    if total_exposure > config.max_symbol_exposure_pct:
        return RiskCheckResult(
            check_name="symbol_exposure",
            status=RiskCheckStatus.FAILED,
            severity=RiskSeverity.HIGH,
            message=f"Symbol exposure {total_exposure:.2%} exceeds max {config.max_symbol_exposure_pct:.2%}",
            rejection_reason=RiskRejectionReason.MAX_SYMBOL_EXPOSURE_EXCEEDED,
            observed_value=total_exposure,
            limit_value=config.max_symbol_exposure_pct
        )
    return RiskCheckResult("symbol_exposure", RiskCheckStatus.PASSED, RiskSeverity.INFO, "Passed", observed_value=total_exposure)

def check_strategy_exposure(strategy_name: str | None, proposed_notional: float, current_strategy_exposure: float, equity: float, config: RiskLimitConfig) -> RiskCheckResult:
    if not strategy_name:
        return RiskCheckResult("strategy_exposure", RiskCheckStatus.SKIPPED, RiskSeverity.INFO, "No strategy specified")
    if equity <= 0:
        return RiskCheckResult("strategy_exposure", RiskCheckStatus.FAILED, RiskSeverity.CRITICAL, "Equity <= 0")
    total_exposure = (current_strategy_exposure + proposed_notional) / equity
    if total_exposure > config.max_strategy_exposure_pct:
        return RiskCheckResult(
            check_name="strategy_exposure",
            status=RiskCheckStatus.FAILED,
            severity=RiskSeverity.HIGH,
            message=f"Strategy exposure {total_exposure:.2%} exceeds max {config.max_strategy_exposure_pct:.2%}",
            rejection_reason=RiskRejectionReason.MAX_STRATEGY_EXPOSURE_EXCEEDED,
            observed_value=total_exposure,
            limit_value=config.max_strategy_exposure_pct
        )
    return RiskCheckResult("strategy_exposure", RiskCheckStatus.PASSED, RiskSeverity.INFO, "Passed", observed_value=total_exposure)

def check_portfolio_exposure(total_exposure: float, proposed_notional: float, equity: float, config: RiskLimitConfig) -> RiskCheckResult:
    if equity <= 0:
        return RiskCheckResult("portfolio_exposure", RiskCheckStatus.FAILED, RiskSeverity.CRITICAL, "Equity <= 0")
    new_exposure = (total_exposure + proposed_notional) / equity
    if new_exposure > config.max_portfolio_exposure_pct:
        return RiskCheckResult(
            check_name="portfolio_exposure",
            status=RiskCheckStatus.FAILED,
            severity=RiskSeverity.HIGH,
            message=f"Portfolio exposure {new_exposure:.2%} exceeds max {config.max_portfolio_exposure_pct:.2%}",
            rejection_reason=RiskRejectionReason.MAX_PORTFOLIO_EXPOSURE_EXCEEDED,
            observed_value=new_exposure,
            limit_value=config.max_portfolio_exposure_pct
        )
    return RiskCheckResult("portfolio_exposure", RiskCheckStatus.PASSED, RiskSeverity.INFO, "Passed", observed_value=new_exposure)

def check_open_positions_count(current_open_positions: int, config: RiskLimitConfig) -> RiskCheckResult:
    if current_open_positions >= config.max_open_positions:
        return RiskCheckResult(
            check_name="open_positions_count",
            status=RiskCheckStatus.FAILED,
            severity=RiskSeverity.HIGH,
            message=f"Open positions {current_open_positions} >= max {config.max_open_positions}",
            rejection_reason=RiskRejectionReason.MAX_OPEN_POSITIONS_EXCEEDED,
            observed_value=current_open_positions,
            limit_value=config.max_open_positions
        )
    return RiskCheckResult("open_positions_count", RiskCheckStatus.PASSED, RiskSeverity.INFO, "Passed", observed_value=current_open_positions)

def check_cash_buffer(available_cash: float, proposed_notional: float, equity: float, config: RiskLimitConfig) -> RiskCheckResult:
    if equity <= 0:
        return RiskCheckResult("cash_buffer", RiskCheckStatus.FAILED, RiskSeverity.CRITICAL, "Equity <= 0")
    remaining_cash = available_cash - proposed_notional
    required_cash = equity * config.min_cash_buffer_pct
    if remaining_cash < required_cash:
        return RiskCheckResult(
            check_name="cash_buffer",
            status=RiskCheckStatus.FAILED,
            severity=RiskSeverity.HIGH,
            message=f"Remaining cash {remaining_cash:.2f} below buffer {required_cash:.2f}",
            rejection_reason=RiskRejectionReason.INSUFFICIENT_CASH,
            observed_value=remaining_cash,
            limit_value=required_cash
        )
    return RiskCheckResult("cash_buffer", RiskCheckStatus.PASSED, RiskSeverity.INFO, "Passed", observed_value=remaining_cash)

def check_short_allowed(action: SignalAction, config: RiskLimitConfig) -> RiskCheckResult:
    if action == SignalAction.SHORT and not config.allow_short:
        return RiskCheckResult(
            check_name="short_allowed",
            status=RiskCheckStatus.FAILED,
            severity=RiskSeverity.CRITICAL,
            message="Shorting is not allowed",
            rejection_reason=RiskRejectionReason.SHORT_NOT_ALLOWED
        )
    return RiskCheckResult("short_allowed", RiskCheckStatus.PASSED, RiskSeverity.INFO, "Passed")
