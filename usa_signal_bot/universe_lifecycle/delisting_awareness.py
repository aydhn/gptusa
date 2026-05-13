from dataclasses import dataclass, field
from typing import Any, List, Optional, Dict
import datetime
from uuid import uuid4

from usa_signal_bot.core.enums import SymbolLifecycleStatus, SurvivorshipBiasRisk
from usa_signal_bot.universe_lifecycle.lifecycle_models import SymbolHistoryCheck, SymbolHistoryStatus
from usa_signal_bot.universe_lifecycle.symbol_status_resolver import SymbolStatusResolver
from usa_signal_bot.core.serialization import dataclass_to_dict

@dataclass
class DelistingAwarenessResult:
    result_id: str
    symbol: str
    created_at_utc: str
    status: SymbolLifecycleStatus
    risk: SurvivorshipBiasRisk
    evidence: Dict[str, Any]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def create_delisting_awareness_result_id(symbol: str) -> str:
    return f"delist_aware_{symbol}_{uuid4().hex[:8]}"

def infer_delisting_risk_from_history(check: SymbolHistoryCheck) -> SurvivorshipBiasRisk:
    if check.status == SymbolHistoryStatus.SUFFICIENT:
        return SurvivorshipBiasRisk.LOW
    elif check.status in [SymbolHistoryStatus.SHORT_HISTORY, SymbolHistoryStatus.GAP_HISTORY]:
        return SurvivorshipBiasRisk.MODERATE
    elif check.status in [SymbolHistoryStatus.STALE_HISTORY, SymbolHistoryStatus.MISSING_HISTORY]:
        return SurvivorshipBiasRisk.HIGH
    return SurvivorshipBiasRisk.UNKNOWN

def check_symbol_delisting_awareness(
    symbol: str,
    resolver: SymbolStatusResolver,
    as_of_date: Optional[str] = None,
    history_check: Optional[SymbolHistoryCheck] = None
) -> DelistingAwarenessResult:
    record = resolver.resolve_status(symbol, as_of_date)
    risk = SurvivorshipBiasRisk.UNKNOWN
    evidence = {
        "status": record.status.value,
        "source": record.source.value
    }
    warnings = []

    if record.status in [SymbolLifecycleStatus.DELISTED, SymbolLifecycleStatus.ACQUIRED, SymbolLifecycleStatus.MERGED]:
        risk = SurvivorshipBiasRisk.CRITICAL
        evidence["delisted_date"] = record.delisted_date
        evidence["reason"] = record.reason
        warnings.append(f"Symbol {symbol} is marked as {record.status.value}. High delisting risk.")
    elif record.status == SymbolLifecycleStatus.INACTIVE:
        risk = SurvivorshipBiasRisk.HIGH
        warnings.append(f"Symbol {symbol} is INACTIVE. May be delisted.")
    elif record.status == SymbolLifecycleStatus.ACTIVE:
        risk = SurvivorshipBiasRisk.LOW
        if history_check:
            hist_risk = infer_delisting_risk_from_history(history_check)
            if hist_risk in [SurvivorshipBiasRisk.HIGH, SurvivorshipBiasRisk.CRITICAL]:
                risk = SurvivorshipBiasRisk.MODERATE
                warnings.append("Active symbol has stale or missing history. Review recommended.")
    else:
        if history_check:
            hist_risk = infer_delisting_risk_from_history(history_check)
            if hist_risk in [SurvivorshipBiasRisk.HIGH, SurvivorshipBiasRisk.CRITICAL]:
                risk = SurvivorshipBiasRisk.HIGH
                warnings.append("Unknown symbol status with stale/missing history. High risk.")
            else:
                risk = SurvivorshipBiasRisk.MODERATE
        else:
            risk = SurvivorshipBiasRisk.MODERATE
            warnings.append("Unknown symbol status. Missing history check evidence.")

    return DelistingAwarenessResult(
        result_id=create_delisting_awareness_result_id(symbol),
        symbol=symbol.upper(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        status=record.status,
        risk=risk,
        evidence=evidence,
        warnings=warnings,
        errors=[]
    )

def check_universe_delisting_awareness(symbols: List[str], resolver: SymbolStatusResolver, as_of_date: Optional[str] = None) -> List[DelistingAwarenessResult]:
    return [check_symbol_delisting_awareness(s, resolver, as_of_date) for s in symbols]

def delisting_awareness_result_to_dict(result: DelistingAwarenessResult) -> dict:
    return dataclass_to_dict(result)

def delisting_awareness_result_to_text(result: DelistingAwarenessResult) -> str:
    lines = [
        f"Delisting Awareness: {result.symbol} [{result.status.value}]",
        f"Risk: {result.risk.value}",
        f"Evidence: {result.evidence}"
    ]
    if result.warnings:
        lines.append("Warnings:")
        for w in result.warnings:
            lines.append(f"  - {w}")
    return "\n".join(lines)
