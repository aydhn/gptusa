from typing import Any, Dict, Optional
from datetime import datetime, timezone
from usa_signal_bot.core.enums import CapitalStateSource
from usa_signal_bot.allocation.allocation_models import CapitalState, RiskBudget, create_capital_state_id, validate_capital_state

def default_capital_state(total_equity_usd: float = 100000.0) -> CapitalState:
    state = CapitalState(
        capital_state_id=create_capital_state_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        source=CapitalStateSource.CONFIG_DEFAULT,
        total_equity_usd=total_equity_usd,
        available_cash_usd=total_equity_usd,
        reserved_cash_usd=0.0,
        open_exposure_usd=0.0,
        max_gross_exposure_usd=total_equity_usd,
        max_net_exposure_usd=total_equity_usd,
        currency="USD",
        warnings=[],
        errors=[],
        metadata={"note": "Default capital state, not a real broker balance."}
    )
    validate_capital_state(state)
    return state

def build_capital_state_from_config(config_dict: Optional[Dict[str, Any]] = None) -> CapitalState:
    if config_dict is None:
        return default_capital_state()

    total_equity = config_dict.get("default_total_equity_usd", 100000.0)
    source_str = config_dict.get("source", "simulated").upper()
    try:
        source = CapitalStateSource(source_str)
    except ValueError:
        source = CapitalStateSource.SIMULATED

    state = CapitalState(
        capital_state_id=create_capital_state_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        source=source,
        total_equity_usd=total_equity,
        available_cash_usd=config_dict.get("default_available_cash_usd", total_equity),
        reserved_cash_usd=config_dict.get("default_reserved_cash_usd", 0.0),
        open_exposure_usd=config_dict.get("default_open_exposure_usd", 0.0),
        max_gross_exposure_usd=total_equity * (config_dict.get("max_gross_exposure_pct_equity", 100.0) / 100.0),
        max_net_exposure_usd=total_equity * (config_dict.get("max_net_exposure_pct_equity", 100.0) / 100.0),
        currency=config_dict.get("currency", "USD"),
        warnings=[],
        errors=[],
        metadata={"note": "Capital state from config, not a real broker balance."}
    )

    if state.available_cash_usd < 0:
        state.warnings.append("Available cash is negative in config.")

    validate_capital_state(state)
    return state

def build_capital_state_from_paper_payload(payload: Dict[str, Any]) -> CapitalState:
    total_equity = payload.get("total_equity_usd", 100000.0)
    state = CapitalState(
        capital_state_id=create_capital_state_id("paper_capital"),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        source=CapitalStateSource.LOCAL_PAPER_STATE,
        total_equity_usd=total_equity,
        available_cash_usd=payload.get("available_cash_usd", total_equity),
        reserved_cash_usd=payload.get("reserved_cash_usd", 0.0),
        open_exposure_usd=payload.get("open_exposure_usd", 0.0),
        max_gross_exposure_usd=payload.get("max_gross_exposure_usd", total_equity),
        max_net_exposure_usd=payload.get("max_net_exposure_usd", total_equity),
        currency=payload.get("currency", "USD"),
        warnings=[],
        errors=[],
        metadata={"note": "Capital state from local paper tracking."}
    )

    if state.available_cash_usd < 0:
        state.warnings.append("Available cash is negative in paper payload.")

    validate_capital_state(state)
    return state

def update_capital_state_with_reserved_notional(state: CapitalState, reserved_notional_usd: float) -> CapitalState:
    new_state = CapitalState(
        capital_state_id=state.capital_state_id,
        created_at_utc=state.created_at_utc,
        source=state.source,
        total_equity_usd=state.total_equity_usd,
        available_cash_usd=state.available_cash_usd - reserved_notional_usd,
        reserved_cash_usd=state.reserved_cash_usd + reserved_notional_usd,
        open_exposure_usd=state.open_exposure_usd,
        max_gross_exposure_usd=state.max_gross_exposure_usd,
        max_net_exposure_usd=state.max_net_exposure_usd,
        currency=state.currency,
        warnings=list(state.warnings),
        errors=list(state.errors),
        metadata=dict(state.metadata)
    )

    if new_state.available_cash_usd < 0:
        new_state.warnings.append("Update resulted in negative available cash.")

    validate_capital_state(new_state)
    return new_state

def available_risk_capital_usd(state: CapitalState, budget: RiskBudget) -> float:
    # Based on portfolio risk budget and available cash
    max_risk_allowed = state.total_equity_usd * (budget.portfolio_risk_budget_pct / 100.0)
    return min(state.available_cash_usd, max_risk_allowed)

def capital_state_to_text(state: CapitalState) -> str:
    text = f"Capital State [{state.capital_state_id}]\n"
    text += f"Source: {state.source.value}\n"
    text += f"Total Equity: {state.total_equity_usd:.2f} {state.currency}\n"
    text += f"Available Cash: {state.available_cash_usd:.2f} {state.currency}\n"
    text += f"Reserved Cash: {state.reserved_cash_usd:.2f} {state.currency}\n"
    text += f"Open Exposure: {state.open_exposure_usd:.2f} {state.currency}\n"
    if state.warnings:
        text += f"Warnings: {', '.join(state.warnings)}\n"
    text += "Note: This is a local/simulated state, not a real broker balance.\n"
    return text
