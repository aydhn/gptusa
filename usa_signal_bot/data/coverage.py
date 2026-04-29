from dataclasses import dataclass, field
from typing import Optional, Any
from pathlib import Path
from ..core.domain import BaseDomainModel
from ..core.enums import DataCoverageStatus
from .models import OHLCVBar
from .timeframes import is_intraday_timeframe
import json
import datetime

@dataclass
class SymbolTimeframeCoverage(BaseDomainModel):
    symbol: str = ""
    timeframe: str = ""
    bar_count: int = 0
    start_timestamp_utc: Optional[str] = None
    end_timestamp_utc: Optional[str] = None
    expected_min_bars: int = 0
    coverage_ratio: float = 0.0
    status: DataCoverageStatus = DataCoverageStatus.EMPTY
    stale: bool = False
    issues: list[str] = field(default_factory=list)

@dataclass
class DataCoverageReport(BaseDomainModel):
    report_id: str = ""
    provider_name: str = ""
    created_at_utc: str = ""
    symbols: list[str] = field(default_factory=list)
    timeframes: list[str] = field(default_factory=list)
    total_symbol_timeframe_pairs: int = 0
    ready_pairs: int = 0
    partial_pairs: int = 0
    empty_pairs: int = 0
    stale_pairs: int = 0
    invalid_pairs: int = 0
    coverages: list[SymbolTimeframeCoverage] = field(default_factory=list)
    status: DataCoverageStatus = DataCoverageStatus.EMPTY

def calculate_expected_min_bars(timeframe: str, lookback_days: Optional[int] = None) -> int:
    # A simple and safe approximation.
    days = lookback_days if lookback_days and lookback_days > 0 else 30
    if is_intraday_timeframe(timeframe):
        # 1h = ~6.5 bars/day, 15m = ~26 bars/day. Be conservative.
        if timeframe == "1h":
            return int(days * 4)
        elif timeframe == "30m":
            return int(days * 8)
        elif timeframe == "15m":
            return int(days * 15)
        elif timeframe == "5m":
            return int(days * 40)
        elif timeframe == "1m":
            return int(days * 200)
        return days * 2 # default intraday fallback
    else:
        # daily/weekly
        # 5 trading days a week
        return max(1, int(days * 0.6))

def calculate_symbol_timeframe_coverage(
    symbol: str,
    timeframe: str,
    bars: list[OHLCVBar],
    expected_min_bars: int,
    stale_after_seconds: Optional[int] = None
) -> SymbolTimeframeCoverage:

    issues = []
    bar_count = len(bars)

    if bar_count == 0:
        return SymbolTimeframeCoverage(
            symbol=symbol,
            timeframe=timeframe,
            bar_count=0,
            expected_min_bars=expected_min_bars,
            coverage_ratio=0.0,
            status=DataCoverageStatus.EMPTY,
            issues=["No bars found"]
        )

    start_ts = bars[0].timestamp_utc
    end_ts = bars[-1].timestamp_utc

    ratio = min(1.0, bar_count / expected_min_bars) if expected_min_bars > 0 else 1.0

    status = DataCoverageStatus.COMPLETE
    if ratio < 0.5:
        status = DataCoverageStatus.PARTIAL
        issues.append(f"Low coverage: {ratio:.2f} ({bar_count}/{expected_min_bars})")
    elif ratio < 0.9:
        status = DataCoverageStatus.PARTIAL

    stale = False
    if stale_after_seconds and end_ts:
        try:
            # Simple stale check against current time
            now = datetime.datetime.now(datetime.timezone.utc)
            end_dt = datetime.datetime.fromisoformat(end_ts.replace('Z', '+00:00'))
            age_sec = (now - end_dt).total_seconds()
            if age_sec > stale_after_seconds:
                stale = True
                status = DataCoverageStatus.STALE
                issues.append(f"Data is stale (age: {age_sec:.0f}s)")
        except Exception:
            pass

    return SymbolTimeframeCoverage(
        symbol=symbol,
        timeframe=timeframe,
        bar_count=bar_count,
        start_timestamp_utc=start_ts,
        end_timestamp_utc=end_ts,
        expected_min_bars=expected_min_bars,
        coverage_ratio=ratio,
        status=status,
        stale=stale,
        issues=issues
    )

def calculate_coverage_report(
    provider_name: str,
    symbols: list[str],
    timeframes: list[str],
    bars_by_timeframe: dict[str, list[OHLCVBar]]
) -> DataCoverageReport:
    import uuid
    import datetime

    report = DataCoverageReport(
        report_id=str(uuid.uuid4()),
        provider_name=provider_name,
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        symbols=symbols,
        timeframes=timeframes,
        total_symbol_timeframe_pairs=len(symbols) * len(timeframes)
    )

    for tf in timeframes:
        tf_bars = bars_by_timeframe.get(tf, [])
        # Group by symbol
        sym_bars = {s: [] for s in symbols}
        for b in tf_bars:
            if b.symbol in sym_bars:
                sym_bars[b.symbol].append(b)

        expected = calculate_expected_min_bars(tf)

        for sym in symbols:
            bars = sorted(sym_bars[sym], key=lambda x: x.timestamp_utc)
            cov = calculate_symbol_timeframe_coverage(sym, tf, bars, expected)
            report.coverages.append(cov)

            if cov.status == DataCoverageStatus.COMPLETE:
                report.ready_pairs += 1
            elif cov.status == DataCoverageStatus.PARTIAL:
                report.partial_pairs += 1
            elif cov.status == DataCoverageStatus.EMPTY:
                report.empty_pairs += 1
            elif cov.status == DataCoverageStatus.STALE:
                report.stale_pairs += 1
            elif cov.status == DataCoverageStatus.INVALID:
                report.invalid_pairs += 1

    if report.ready_pairs == report.total_symbol_timeframe_pairs and report.total_symbol_timeframe_pairs > 0:
        report.status = DataCoverageStatus.COMPLETE
    elif report.ready_pairs + report.partial_pairs > 0:
        report.status = DataCoverageStatus.PARTIAL
    else:
        report.status = DataCoverageStatus.EMPTY

    return report

def coverage_report_to_text(report: DataCoverageReport) -> str:
    lines = [
        f"Data Coverage Report: {report.report_id}",
        f"Provider: {report.provider_name} | Created: {report.created_at_utc}",
        f"Overall Status: {report.status.value}",
        f"Pairs: {report.total_symbol_timeframe_pairs} total | {report.ready_pairs} ready | {report.partial_pairs} partial | {report.empty_pairs} empty",
        "---"
    ]
    for cov in report.coverages:
        issue_str = f" [{', '.join(cov.issues)}]" if cov.issues else ""
        lines.append(f"{cov.symbol} ({cov.timeframe}): {cov.status.value} - {cov.bar_count}/{cov.expected_min_bars} bars ({cov.coverage_ratio:.2f}){issue_str}")
    return "\n".join(lines)

def write_coverage_report_json(path: Path, report: DataCoverageReport) -> Path:
    from ..core.serialization import dataclass_to_dict
    with open(path, 'w') as f:
        json.dump(dataclass_to_dict(report), f, indent=2)
    return path

def has_minimum_coverage(report: DataCoverageReport, min_ready_ratio: float) -> bool:
    if report.total_symbol_timeframe_pairs == 0:
        return False
    ratio = report.ready_pairs / report.total_symbol_timeframe_pairs
    return ratio >= min_ready_ratio
