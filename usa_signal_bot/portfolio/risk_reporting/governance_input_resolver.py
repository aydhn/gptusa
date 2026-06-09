from typing import Any, Dict, List, Optional
import datetime
# Try to import pandas, but fallback gracefully if missing so tests can pass without it
try:
    import pandas as pd
except ImportError:
    pd = None

from usa_signal_bot.portfolio.risk_reporting.phase157_models import (
    PortfolioRiskInputReference,
    create_portfolio_risk_input_reference_id
)
from usa_signal_bot.core.enums import PortfolioRiskInputKind, PortfolioRiskReportingRiskFlag

FORBIDDEN_COLUMNS = {
    "broker_order", "paper_order", "live_order", "sent_to_broker",
    "strategy_active", "deployment_enabled", "portfolio_weight",
    "target_weight", "actual_target_weight", "actual_portfolio_weight",
    "allocation", "actual_allocation", "capital_allocation",
    "actual_position_size", "position_size", "order_size",
    "real_order", "live_signal", "buy_signal", "sell_signal",
    "recommended_weight", "production_patch"
}

def build_portfolio_risk_input_references(payloads: Dict[str, Any], dataframes: Optional[Dict[str, Any]] = None) -> List[PortfolioRiskInputReference]:
    refs = []
    for key, payload in payloads.items():
        kind = PortfolioRiskInputKind.UNKNOWN
        if "optimizer" in key.lower() and "review" in key.lower(): kind = PortfolioRiskInputKind.OPTIMIZER_PROTOTYPE_REVIEW
        elif "policy" in key.lower(): kind = PortfolioRiskInputKind.OPTIMIZER_POLICY
        elif "comparison" in key.lower(): kind = PortfolioRiskInputKind.OBJECTIVE_COMPARISON_REPORT
        elif "validation" in key.lower(): kind = PortfolioRiskInputKind.OPTIMIZER_VALIDATION_REPORT
        elif "boundary" in key.lower(): kind = PortfolioRiskInputKind.OPTIMIZER_SAFETY_BOUNDARY

        forbidden_payload_fields = detect_forbidden_portfolio_risk_fields(payload)
        df = dataframes.get(key) if dataframes else None
        cols = list(df.columns) if df is not None and hasattr(df, 'columns') else []
        forbidden_cols = detect_forbidden_portfolio_risk_columns(cols)

        flags = []
        if forbidden_payload_fields or forbidden_cols:
            flags.append(PortfolioRiskReportingRiskFlag.FORBIDDEN_PORTFOLIO_RISK_COLUMN)

        refs.append(PortfolioRiskInputReference(
            input_ref_id=create_portfolio_risk_input_reference_id(),
            created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            input_kind=kind,
            source_artifact_name=key,
            source_path=None,
            source_hash=None,
            available=True,
            read_only=True,
            row_count=len(df) if df is not None and hasattr(df, '__len__') else None,
            columns=cols,
            forbidden_columns_detected=forbidden_cols,
            research_data_only=True,
            portfolio_risk_governance_only=True,
            warnings=[],
            errors=forbidden_payload_fields,
            risk_flags=flags,
            metadata={}
        ))
    return refs

def detect_forbidden_portfolio_risk_columns(columns: List[str]) -> List[str]:
    return [c for c in columns if c.lower() in FORBIDDEN_COLUMNS]

def detect_forbidden_portfolio_risk_fields(payload: Dict[str, Any]) -> List[str]:
    return [k for k in payload.keys() if k.lower() in FORBIDDEN_COLUMNS]

def validate_portfolio_risk_input_references(items: List[PortfolioRiskInputReference]) -> List[str]:
    errs = []
    for item in items:
        if item.forbidden_columns_detected:
            errs.append(f"Forbidden columns detected in {item.source_artifact_name}")
    return errs

def portfolio_risk_input_resolver_summary(items: List[PortfolioRiskInputReference]) -> Dict[str, Any]:
    return {"count": len(items)}

def portfolio_risk_input_resolver_to_text(items: List[PortfolioRiskInputReference], limit: int = 300) -> str:
    return f"Resolved {len(items)} inputs."
