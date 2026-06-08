import pandas as pd
import hashlib
import json
from typing import Any, Dict, List
from usa_signal_bot.portfolio.construction.phase155_models import (
    PrototypeExposureTable,
    PrototypeExposureRecord,
    SandboxAllocationResult,
    PortfolioSandboxCandidate,
    create_prototype_exposure_record_id,
    create_prototype_exposure_table_id,
    _now_str
)
from usa_signal_bot.core.enums import PortfolioConstructionRiskFlag

def build_prototype_exposure_table(
    results: List[SandboxAllocationResult],
    candidates: List[PortfolioSandboxCandidate]
) -> PrototypeExposureTable:

    cand_map = {c.symbol: c for c in candidates}
    records = []

    for r in results:
        cand = cand_map.get(r.symbol)
        group = cand.diversification_group if cand else None

        records.append(PrototypeExposureRecord(
            exposure_id=create_prototype_exposure_record_id(),
            created_at_utc=_now_str(),
            symbol=r.symbol,
            method_kind=r.method_kind,
            sandbox_prototype_weight=r.sandbox_prototype_weight,
            normalized_sandbox_weight=r.normalized_sandbox_weight,
            diversification_group=group,
            group_sandbox_weight=None,
            exposure_valid=True,
            research_exposure_only=True,
            actual_exposure=None,
            actual_position_size=None,
            actual_allocation=None,
            order_size=None,
            capital_allocation=None,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={"method_name": r.method_name}
        ))

    # Group weights per method
    method_groups = {}
    for rec in records:
        key = (rec.method_kind, rec.diversification_group)
        if key not in method_groups:
            method_groups[key] = 0.0
        if rec.normalized_sandbox_weight is not None:
            method_groups[key] += rec.normalized_sandbox_weight

    for rec in records:
        key = (rec.method_kind, rec.diversification_group)
        rec.group_sandbox_weight = method_groups.get(key)

    table = PrototypeExposureTable(
        table_id=create_prototype_exposure_table_id(),
        created_at_utc=_now_str(),
        records=records,
        symbol_count=len(set(r.symbol for r in records)),
        method_count=len(set(r.method_kind for r in records)),
        table_hash=None,
        table_valid=True,
        research_exposure_only=True,
        no_actual_target_weights=True,
        no_actual_portfolio_weights=True,
        no_actual_allocation=True,
        no_actual_position_size=True,
        no_order_size=True,
        no_capital_allocation=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    table.table_hash = compute_prototype_exposure_table_hash(table)
    return table

def compute_prototype_exposure_table_hash(table: PrototypeExposureTable) -> str:
    data = []
    for r in sorted(table.records, key=lambda x: (x.symbol, x.method_kind.value)):
        data.append({
            "symbol": r.symbol,
            "method": r.method_kind.value,
            "weight": round(r.normalized_sandbox_weight, 6) if r.normalized_sandbox_weight is not None else None
        })
    s = json.dumps(data, sort_keys=True)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def prototype_exposure_table_to_dataframe(table: PrototypeExposureTable) -> pd.DataFrame:
    data = []
    for r in table.records:
        data.append({
            "symbol": r.symbol,
            "method_kind": r.method_kind.value,
            "sandbox_prototype_weight": r.sandbox_prototype_weight,
            "normalized_sandbox_weight": r.normalized_sandbox_weight,
            "diversification_group": r.diversification_group,
            "group_sandbox_weight": r.group_sandbox_weight
        })
    return pd.DataFrame(data)

def validate_prototype_exposure_table(table: PrototypeExposureTable) -> List[str]:
    errors = []
    for r in table.records:
        if r.actual_exposure is not None:
            errors.append(f"Record {r.symbol} has actual_exposure.")
            r.risk_flags.append(PortfolioConstructionRiskFlag.ACTUAL_PORTFOLIO_WEIGHT_RISK)
        if r.actual_allocation is not None:
            errors.append(f"Record {r.symbol} has actual_allocation.")
            r.risk_flags.append(PortfolioConstructionRiskFlag.ACTUAL_ALLOCATION_RISK)
        if r.actual_position_size is not None:
            errors.append(f"Record {r.symbol} has actual_position_size.")
            r.risk_flags.append(PortfolioConstructionRiskFlag.ACTUAL_POSITION_SIZE_RISK)
        if r.order_size is not None:
            errors.append(f"Record {r.symbol} has order_size.")
            r.risk_flags.append(PortfolioConstructionRiskFlag.ORDER_SIZE_RISK)
        if r.capital_allocation is not None:
            errors.append(f"Record {r.symbol} has capital_allocation.")
            r.risk_flags.append(PortfolioConstructionRiskFlag.CAPITAL_DEPLOYMENT_RISK)

    if not table.no_actual_target_weights:
        errors.append("Table no_actual_target_weights is False.")
    if not table.no_actual_portfolio_weights:
        errors.append("Table no_actual_portfolio_weights is False.")
    if not table.no_actual_allocation:
        errors.append("Table no_actual_allocation is False.")
    if not table.no_actual_position_size:
        errors.append("Table no_actual_position_size is False.")
    if not table.no_order_size:
        errors.append("Table no_order_size is False.")
    if not table.no_capital_allocation:
        errors.append("Table no_capital_allocation is False.")

    return errors

def prototype_exposure_table_summary(table: PrototypeExposureTable) -> Dict[str, Any]:
    return {
        "record_count": len(table.records),
        "symbol_count": table.symbol_count,
        "method_count": table.method_count,
        "hash": table.table_hash
    }

def prototype_exposure_table_to_text(table: PrototypeExposureTable, limit: int = 300) -> str:
    summary = prototype_exposure_table_summary(table)
    return (
        f"Prototype Exposure Table: {summary['record_count']} records\n"
        f"Symbols: {summary['symbol_count']}, Methods: {summary['method_count']}\n"
        f"Hash: {summary['hash']}"
    )
