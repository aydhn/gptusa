import pandas as pd
from typing import Any, Dict, List, Optional
from usa_signal_bot.portfolio.construction.phase155_models import (
    PortfolioConstructionInputReference,
    PortfolioConstructionInputKind,
    create_portfolio_construction_input_reference_id,
    _now_str
)
from usa_signal_bot.core.enums import PortfolioConstructionRiskFlag

def build_portfolio_construction_input_references(
    payloads: Dict[str, Any],
    dataframes: Optional[Dict[str, pd.DataFrame]] = None
) -> List[PortfolioConstructionInputReference]:

    refs = []

    for key, payload in payloads.items():
        if not payload:
            continue

        kind = _determine_input_kind_from_key(key)
        forbidden_fields = detect_forbidden_construction_fields(payload)

        flags = []
        if forbidden_fields:
            flags.append(PortfolioConstructionRiskFlag.CONSTRUCTION_INPUT_INVALID)

        refs.append(PortfolioConstructionInputReference(
            input_ref_id=create_portfolio_construction_input_reference_id(),
            created_at_utc=_now_str(),
            input_kind=kind,
            source_artifact_name=key,
            source_path=None,
            source_hash=None,
            available=True,
            read_only=True,
            row_count=None,
            columns=[],
            forbidden_columns_detected=[],
            research_data_only=True,
            allocation_sandbox_only=True,
            warnings=[],
            errors=forbidden_fields,
            risk_flags=flags,
            metadata={"type": "payload"}
        ))

    if dataframes:
        for key, df in dataframes.items():
            if df is None or df.empty:
                continue

            columns = df.columns.tolist()
            forbidden_columns = detect_forbidden_construction_columns(columns)

            flags = []
            if forbidden_columns:
                flags.append(PortfolioConstructionRiskFlag.FORBIDDEN_CONSTRUCTION_COLUMN)

            refs.append(PortfolioConstructionInputReference(
                input_ref_id=create_portfolio_construction_input_reference_id(),
                created_at_utc=_now_str(),
                input_kind=PortfolioConstructionInputKind.SANDBOX_CANDIDATE_INPUTS,
                source_artifact_name=key,
                source_path=None,
                source_hash=None,
                available=True,
                read_only=True,
                row_count=len(df),
                columns=columns,
                forbidden_columns_detected=forbidden_columns,
                research_data_only=True,
                allocation_sandbox_only=True,
                warnings=[],
                errors=[],
                risk_flags=flags,
                metadata={"type": "dataframe"}
            ))

    return refs

def _determine_input_kind_from_key(key: str) -> PortfolioConstructionInputKind:
    key = key.lower()
    if "review" in key:
        return PortfolioConstructionInputKind.SIZING_PROTOTYPE_REVIEW
    elif "policy" in key:
        return PortfolioConstructionInputKind.SIZING_POLICY
    elif "contract" in key:
        return PortfolioConstructionInputKind.SIZING_METHOD_CONTRACTS
    elif "matrix" in key:
        return PortfolioConstructionInputKind.SIZING_COMPARISON_MATRIX
    elif "sensitivity" in key:
        return PortfolioConstructionInputKind.SIZING_SENSITIVITY_REPORT
    elif "budget" in key:
        return PortfolioConstructionInputKind.RISK_BUDGET_ADHERENCE_REPORT
    elif "boundary" in key:
        return PortfolioConstructionInputKind.SIZING_SAFETY_BOUNDARY
    return PortfolioConstructionInputKind.UNKNOWN

def validate_sandbox_candidate_inputs_frame(df: pd.DataFrame) -> List[str]:
    errors = []
    if df is None or df.empty:
        errors.append("Sandbox candidate dataframe is empty.")
        return errors

    if "symbol" not in df.columns:
        errors.append("Missing required column 'symbol'.")

    forbidden = detect_forbidden_construction_columns(df.columns.tolist())
    for f in forbidden:
        errors.append(f"Forbidden column detected: {f}")

    return errors

def detect_forbidden_construction_columns(columns: List[str]) -> List[str]:
    forbidden = [
        "broker_order", "paper_order", "live_order", "sent_to_broker",
        "strategy_active", "deployment_enabled", "portfolio_weight",
        "target_weight", "actual_target_weight", "actual_portfolio_weight",
        "allocation", "actual_allocation", "capital_allocation",
        "actual_position_size", "position_size", "order_size", "real_order",
        "live_signal", "buy_signal", "sell_signal", "recommended_weight",
        "production_patch"
    ]
    return [col for col in columns if col in forbidden]

def detect_forbidden_construction_fields(payload: Dict[str, Any]) -> List[str]:
    forbidden = [
        "actual_target_weight", "actual_portfolio_weight", "actual_allocation",
        "capital_allocation", "actual_position_size", "order_size",
        "broker_order_id", "live_trade_id"
    ]
    detected = []

    def _search(obj: Any):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in forbidden:
                    detected.append(k)
                _search(v)
        elif isinstance(obj, list):
            for item in obj:
                _search(item)

    _search(payload)
    return list(set(detected))

def portfolio_construction_input_resolver_summary(items: List[PortfolioConstructionInputReference]) -> Dict[str, Any]:
    return {
        "count": len(items),
        "kinds": list(set(item.input_kind.value for item in items)),
        "available_count": sum(1 for item in items if item.available),
        "forbidden_fields_detected": any(item.errors for item in items if item.metadata.get("type") == "payload"),
        "forbidden_columns_detected": any(item.forbidden_columns_detected for item in items)
    }

def portfolio_construction_input_resolver_to_text(items: List[PortfolioConstructionInputReference], limit: int = 300) -> str:
    summary = portfolio_construction_input_resolver_summary(items)
    return (
        f"Input References: {summary['count']} total\n"
        f"Available: {summary['available_count']}\n"
        f"Forbidden Fields: {summary['forbidden_fields_detected']}\n"
        f"Forbidden Columns: {summary['forbidden_columns_detected']}"
    )
