import datetime
from typing import Dict, Any, List
from .phase147_models import BacktestRunConfig, ResearchExposureSide, BacktestTimeModelKind, create_backtest_run_config_id

def build_default_backtest_run_config(market_contract: Dict[str, Any] | None = None) -> BacktestRunConfig:
    return BacktestRunConfig(
        config_id=create_backtest_run_config_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        run_name="default_offline_run",
        initial_cash=100000.0,
        currency="USD",
        exposure_side=ResearchExposureSide.LONG_ONLY_RESEARCH,
        max_single_symbol_exposure_fraction=1.0,
        allow_fractional_shares=False,
        allow_short_exposure=False,
        allow_leverage=False,
        deterministic_seed=147,
        time_model_kind=BacktestTimeModelKind.BAR_CLOSE_TO_NEXT_OPEN,
        execution_assumption_id=None,
        market_simulation_contract_id=market_contract.get("contract_id") if market_contract else None,
        run_config_valid=True,
        research_data_only=True,
        offline_backtest_research_only=True,
        live_trading_enabled=False,
        paper_trading_enabled=False,
        broker_execution_enabled=False,
        real_order_creation_enabled=False,
        strategy_activation_allowed=False,
        portfolio_optimization_enabled=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def validate_backtest_run_config(config: BacktestRunConfig) -> List[str]:
    errors = []
    if config.initial_cash <= 0: errors.append("initial_cash must be > 0")
    if config.allow_short_exposure: errors.append("short exposure not allowed")
    if config.allow_leverage: errors.append("leverage not allowed")
    if not config.research_data_only: errors.append("research_data_only must be true")
    if not config.offline_backtest_research_only: errors.append("offline_backtest_research_only must be true")
    return errors

def backtest_run_config_summary(config: BacktestRunConfig) -> Dict[str, Any]:
    return {"config_id": config.config_id, "valid": config.run_config_valid}

def backtest_run_config_to_text(config: BacktestRunConfig, limit: int = 300) -> str:
    return f"BacktestRunConfig {config.config_id} - valid: {config.run_config_valid}"
