import datetime
from typing import Any
from usa_signal_bot.core.enums import FeatureComputationMode
from usa_signal_bot.feature_engine.phase116_models import FeatureComputationRequest, create_feature_computation_request_id

def build_feature_computation_request(
    symbol: str,
    feature_names: list[str] | None = None,
    factor_names: list[str] | None = None,
    input_contract_id: str | None = None,
    schema_id: str | None = None
) -> FeatureComputationRequest:
    return FeatureComputationRequest(
        request_id=create_feature_computation_request_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        symbol=symbol,
        feature_names=feature_names or [],
        factor_names=factor_names or [],
        computation_mode=FeatureComputationMode.PLANNED,
        input_contract_id=input_contract_id,
        schema_id=schema_id,
        metadata_only=True,
        dry_run_only=True,
        research_data_only=True,
        allow_network=False,
        allow_paid_api=False,
        allow_scraping=False,
        allow_html_parsing=False,
        allow_broker=False,
        allow_order=False,
        allow_paper_mutation=False,
        allow_telegram_real_send=False,
        allow_dashboard=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_default_feature_computation_requests(symbols: list[str] | None = None) -> list[FeatureComputationRequest]:
    if symbols is None:
        symbols = ["AAPL", "MSFT", "SPY"]
    return [build_feature_computation_request(s) for s in symbols]

def validate_feature_computation_request_safety(request: FeatureComputationRequest) -> list[str]:
    errors = []
    if request.allow_network:
        errors.append("allow_network must be false")
    if request.allow_paid_api:
        errors.append("allow_paid_api must be false")
    if request.allow_scraping:
        errors.append("allow_scraping must be false")
    if request.allow_html_parsing:
        errors.append("allow_html_parsing must be false")
    if request.allow_broker:
        errors.append("allow_broker must be false")
    if request.allow_order:
        errors.append("allow_order must be false")
    if request.allow_paper_mutation:
        errors.append("allow_paper_mutation must be false")
    if request.allow_telegram_real_send:
        errors.append("allow_telegram_real_send must be false")
    if request.allow_dashboard:
        errors.append("allow_dashboard must be false")
    if request.computation_mode != FeatureComputationMode.PLANNED:
        errors.append("computation_mode must be PLANNED")
    return errors

def feature_computation_request_summary(request: FeatureComputationRequest) -> dict[str, Any]:
    return {"symbol": request.symbol, "features": len(request.feature_names), "factors": len(request.factor_names)}

def feature_computation_request_to_text(request: FeatureComputationRequest) -> str:
    return f"Request {request.request_id} for {request.symbol}"
