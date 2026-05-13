from dataclasses import dataclass, field
from typing import Any, List, Optional, Dict
import hashlib
from datetime import datetime, timezone

from usa_signal_bot.core.enums import (
    SymbolLifecycleStatus,
    SymbolLifecycleSource,
    UniverseSnapshotType,
    SymbolHistoryStatus,
    SurvivorshipBiasRisk,
    UniverseGuardStatus,
    SymbolAliasType,
    UniverseLifecycleReportType
)
from usa_signal_bot.core.serialization import dataclass_to_dict

@dataclass
class SymbolLifecycleRecord:
    symbol: str
    status: SymbolLifecycleStatus
    source: SymbolLifecycleSource
    first_seen_date: Optional[str] = None
    last_seen_date: Optional[str] = None
    listed_date: Optional[str] = None
    delisted_date: Optional[str] = None
    successor_symbol: Optional[str] = None
    predecessor_symbol: Optional[str] = None
    reason: Optional[str] = None
    confidence: Optional[float] = None
    notes: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SymbolAliasRecord:
    alias_id: str
    old_symbol: str
    new_symbol: str
    alias_type: SymbolAliasType
    effective_date: Optional[str] = None
    source: SymbolLifecycleSource = SymbolLifecycleSource.MANUAL_REGISTRY
    confidence: Optional[float] = None
    notes: List[str] = field(default_factory=list)

@dataclass
class UniverseSnapshot:
    snapshot_id: str
    created_at_utc: str
    snapshot_type: UniverseSnapshotType
    as_of_date: Optional[str]
    universe_name: str
    symbols: List[str]
    source: SymbolLifecycleSource
    symbol_count: int
    metadata: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

@dataclass
class SymbolHistoryCheck:
    check_id: str
    symbol: str
    created_at_utc: str
    status: SymbolHistoryStatus
    row_count: int
    first_date: Optional[str] = None
    last_date: Optional[str] = None
    missing_row_estimate: Optional[int] = None
    stale_days: Optional[int] = None
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SurvivorshipBiasAssessment:
    assessment_id: str
    created_at_utc: str
    universe_name: str
    as_of_date: Optional[str]
    status: UniverseGuardStatus
    risk: SurvivorshipBiasRisk
    current_symbol_count: int
    historical_symbol_count: Optional[int] = None
    missing_lifecycle_count: int = 0
    delisted_symbol_count: int = 0
    inactive_symbol_count: int = 0
    unknown_status_count: int = 0
    affected_symbols: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class UniverseLifecycleReviewResult:
    review_id: str
    created_at_utc: str
    report_type: UniverseLifecycleReportType
    universe_name: str
    lifecycle_records: List[SymbolLifecycleRecord]
    aliases: List[SymbolAliasRecord]
    snapshots: List[UniverseSnapshot]
    history_checks: List[SymbolHistoryCheck]
    survivorship_assessment: Optional[SurvivorshipBiasAssessment]
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


def symbol_lifecycle_record_to_dict(record: SymbolLifecycleRecord) -> dict:
    return dataclass_to_dict(record)

def symbol_alias_record_to_dict(record: SymbolAliasRecord) -> dict:
    return dataclass_to_dict(record)

def universe_snapshot_to_dict(snapshot: UniverseSnapshot) -> dict:
    return dataclass_to_dict(snapshot)

def symbol_history_check_to_dict(check: SymbolHistoryCheck) -> dict:
    return dataclass_to_dict(check)

def survivorship_bias_assessment_to_dict(assessment: SurvivorshipBiasAssessment) -> dict:
    return dataclass_to_dict(assessment)

def universe_lifecycle_review_result_to_dict(result: UniverseLifecycleReviewResult) -> dict:
    return dataclass_to_dict(result)

def validate_symbol_lifecycle_record(record: SymbolLifecycleRecord) -> None:
    from usa_signal_bot.core.exceptions import LifecycleValidationError
    if not record.symbol:
        raise LifecycleValidationError("symbol cannot be empty")
    if record.confidence is not None and not (0.0 <= record.confidence <= 1.0):
        raise LifecycleValidationError("confidence must be between 0.0 and 1.0")
    if record.listed_date and record.delisted_date:
        if record.delisted_date < record.listed_date:
            raise LifecycleValidationError("delisted_date cannot be before listed_date")

def validate_symbol_alias_record(record: SymbolAliasRecord) -> None:
    from usa_signal_bot.core.exceptions import LifecycleValidationError
    if not record.old_symbol or not record.new_symbol:
        raise LifecycleValidationError("old_symbol and new_symbol cannot be empty")
    if record.confidence is not None and not (0.0 <= record.confidence <= 1.0):
        raise LifecycleValidationError("confidence must be between 0.0 and 1.0")

def validate_universe_snapshot(snapshot: UniverseSnapshot) -> None:
    from usa_signal_bot.core.exceptions import LifecycleValidationError
    if snapshot.symbol_count != len(snapshot.symbols):
        raise LifecycleValidationError("symbol_count must match length of symbols list")

def validate_symbol_history_check(check: SymbolHistoryCheck) -> None:
    from usa_signal_bot.core.exceptions import LifecycleValidationError
    if not check.symbol:
        raise LifecycleValidationError("symbol cannot be empty")

def validate_survivorship_bias_assessment(assessment: SurvivorshipBiasAssessment) -> None:
    from usa_signal_bot.core.exceptions import LifecycleValidationError
    assessment.affected_symbols = sorted(list(set(assessment.affected_symbols)))


def create_symbol_alias_id(old_symbol: str, new_symbol: str) -> str:
    raw = f"{old_symbol}_{new_symbol}"
    return f"alias_{hashlib.sha256(raw.encode('utf-8')).hexdigest()[:8]}"

def create_universe_snapshot_id(universe_name: str, prefix: str = "universe_snapshot") -> str:
    from uuid import uuid4
    return f"{prefix}_{uuid4().hex[:8]}"

def create_symbol_history_check_id(symbol: str) -> str:
    from uuid import uuid4
    return f"hist_check_{symbol}_{uuid4().hex[:8]}"

def create_survivorship_assessment_id(prefix: str = "survivorship") -> str:
    from uuid import uuid4
    return f"{prefix}_{uuid4().hex[:8]}"

def create_universe_lifecycle_review_id(prefix: str = "lifecycle_review") -> str:
    from uuid import uuid4
    return f"{prefix}_{uuid4().hex[:8]}"
