import uuid
from dataclasses import dataclass, field
from typing import Any, List, Optional, Tuple
from pathlib import Path
from usa_signal_bot.data.models import OHLCVBar
from usa_signal_bot.core.enums import DataRepairActionType
from usa_signal_bot.data.anomalies import DataAnomalyReport

@dataclass
class DataRepairAction:
    action_id: str
    action_type: DataRepairActionType
    symbol: Optional[str]
    timestamp_utc: Optional[str]
    reason: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class DataRepairReport:
    report_id: str
    created_at_utc: str
    original_bar_count: int
    repaired_bar_count: int
    dropped_bar_count: int
    actions: List[DataRepairAction]
    warnings: List[str]
    errors: List[str]

def drop_duplicate_bars(bars: List[OHLCVBar]) -> Tuple[List[OHLCVBar], List[DataRepairAction]]:
    actions = []
    repaired = []
    seen = set()
    for bar in bars:
        key = (bar.symbol, bar.timeframe, bar.timestamp_utc)
        if key in seen:
            actions.append(DataRepairAction(
                action_id=str(uuid.uuid4()),
                action_type=DataRepairActionType.DROP_DUPLICATE_BAR,
                symbol=bar.symbol,
                timestamp_utc=bar.timestamp_utc,
                reason="Duplicate bar"
            ))
        else:
            seen.add(key)
            repaired.append(bar)
    return repaired, actions

def drop_invalid_price_bars(bars: List[OHLCVBar]) -> Tuple[List[OHLCVBar], List[DataRepairAction]]:
    actions = []
    repaired = []
    for bar in bars:
        if bar.open <= 0 or bar.high <= 0 or bar.low <= 0 or bar.close <= 0 or bar.high < bar.low:
            actions.append(DataRepairAction(
                action_id=str(uuid.uuid4()),
                action_type=DataRepairActionType.DROP_INVALID_BAR,
                symbol=bar.symbol,
                timestamp_utc=bar.timestamp_utc,
                reason="Invalid price"
            ))
        elif bar.volume < 0:
            actions.append(DataRepairAction(
                action_id=str(uuid.uuid4()),
                action_type=DataRepairActionType.DROP_INVALID_BAR,
                symbol=bar.symbol,
                timestamp_utc=bar.timestamp_utc,
                reason="Negative volume"
            ))
        else:
            repaired.append(bar)
    return repaired, actions

def fill_missing_volume_with_zero(bars: List[OHLCVBar]) -> Tuple[List[OHLCVBar], List[DataRepairAction]]:
    actions = []
    for bar in bars:
        if bar.volume is None:
            bar.volume = 0.0
            actions.append(DataRepairAction(
                action_id=str(uuid.uuid4()),
                action_type=DataRepairActionType.FILL_MISSING_VOLUME_WITH_ZERO,
                symbol=bar.symbol,
                timestamp_utc=bar.timestamp_utc,
                reason="Missing volume replaced with 0"
            ))
    return bars, actions

def sort_bars_by_symbol_time(bars: List[OHLCVBar]) -> List[OHLCVBar]:
    return sorted(bars, key=lambda x: (x.symbol, x.timestamp_utc))

def plan_repair_actions(bars: List[OHLCVBar], anomaly_report: DataAnomalyReport) -> List[DataRepairAction]:
    # Placeholder for generating a plan without mutating data
    return []

def repair_ohlcv_bars(bars: List[OHLCVBar], expected_symbols: Optional[List[str]] = None, allow_drop_invalid: bool = True) -> Tuple[List[OHLCVBar], DataRepairReport]:
    from usa_signal_bot.utils.time_utils import utc_now
    original_count = len(bars)
    all_actions = []

    # 1. Fill missing volume
    bars, a = fill_missing_volume_with_zero(bars)
    all_actions.extend(a)

    # 2. Drop duplicates
    bars, a = drop_duplicate_bars(bars)
    all_actions.extend(a)

    # 3. Drop invalid prices
    if allow_drop_invalid:
        bars, a = drop_invalid_price_bars(bars)
        all_actions.extend(a)

    # 4. Sort
    bars = sort_bars_by_symbol_time(bars)

    repaired_count = len(bars)
    dropped_count = original_count - repaired_count

    report = DataRepairReport(
        report_id=str(uuid.uuid4()),
        created_at_utc=utc_now().isoformat(),
        original_bar_count=original_count,
        repaired_bar_count=repaired_count,
        dropped_bar_count=dropped_count,
        actions=all_actions,
        warnings=[],
        errors=[]
    )
    return bars, report

def repair_report_to_text(report: DataRepairReport) -> str:
    lines = [
        f"Data Repair Report",
        f"Original: {report.original_bar_count} | Repaired: {report.repaired_bar_count} | Dropped: {report.dropped_bar_count}",
        f"Actions Taken: {len(report.actions)}"
    ]
    if report.actions:
        lines.append("Sample Actions:")
        for a in report.actions[:10]:
            lines.append(f"  - {a.action_type.value} [{a.symbol}@{a.timestamp_utc}]: {a.reason}")
        if len(report.actions) > 10:
             lines.append(f"  ... and {len(report.actions) - 10} more actions.")
    return "\n".join(lines)

def write_repair_report_json(path: Path, report: DataRepairReport) -> Path:
    import json
    from dataclasses import asdict
    from usa_signal_bot.utils.file_utils import safe_mkdir
    safe_mkdir(path.parent)

    d = asdict(report)
    for a in d['actions']:
        if hasattr(a['action_type'], 'value'):
            a['action_type'] = a['action_type'].value

    with path.open('w', encoding='utf-8') as f:
        json.dump(d, f, indent=2)
    return path
