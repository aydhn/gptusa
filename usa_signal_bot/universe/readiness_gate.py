import csv
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from usa_signal_bot.core.enums import SymbolReadinessStatus, UniverseReadinessGateStatus
from usa_signal_bot.universe.models import UniverseDefinition
from usa_signal_bot.data.readiness import DataReadinessReport, DataReadinessStatus
from usa_signal_bot.core.exceptions import UniverseReadinessGateError


@dataclass
class SymbolReadinessDecision:
    symbol: str
    status: SymbolReadinessStatus
    score: float
    ready_timeframes: List[str]
    missing_timeframes: List[str]
    failed_timeframes: List[str]
    reasons: List[str] = field(default_factory=list)


@dataclass
class UniverseReadinessGateCriteria:
    min_symbol_score: float
    min_required_timeframes: int
    required_primary_timeframe: str
    allow_partial_symbols: bool
    min_eligible_symbol_ratio: float
    max_failed_symbol_ratio: float


@dataclass
class UniverseReadinessGateReport:
    report_id: str
    created_at_utc: str
    universe_name: str
    total_symbols: int
    eligible_symbols: int
    partial_symbols: int
    ineligible_symbols: int
    missing_data_symbols: int
    failed_validation_symbols: int
    eligible_symbol_ratio: float
    failed_symbol_ratio: float
    status: UniverseReadinessGateStatus
    decisions: List[SymbolReadinessDecision]
    blocking_reasons: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


def default_universe_readiness_gate_criteria() -> UniverseReadinessGateCriteria:
    return UniverseReadinessGateCriteria(
        min_symbol_score=70.0,
        min_required_timeframes=1,
        required_primary_timeframe="1d",
        allow_partial_symbols=True,
        min_eligible_symbol_ratio=0.60,
        max_failed_symbol_ratio=0.30
    )


def symbol_decisions_from_readiness(
    universe: UniverseDefinition,
    readiness_report: DataReadinessReport,
    criteria: UniverseReadinessGateCriteria
) -> List[SymbolReadinessDecision]:
    from usa_signal_bot.data.readiness import symbol_readiness_score, symbol_ready_timeframes, symbol_missing_or_failed_timeframes

    decisions = []

    for sym_obj in universe.symbols:
        if hasattr(sym_obj, 'active') and not sym_obj.active:
            continue

        symbol = sym_obj.symbol if hasattr(sym_obj, 'symbol') else sym_obj

        score = symbol_readiness_score(readiness_report, symbol)
        ready_tfs = symbol_ready_timeframes(readiness_report, symbol)
        missing_tfs, failed_tfs = symbol_missing_or_failed_timeframes(readiness_report, symbol)

        reasons = []
        status = SymbolReadinessStatus.ELIGIBLE

        if criteria.required_primary_timeframe not in ready_tfs:
            status = SymbolReadinessStatus.INELIGIBLE
            reasons.append(f"Missing required primary timeframe: {criteria.required_primary_timeframe}")
        elif len(ready_tfs) < criteria.min_required_timeframes:
            status = SymbolReadinessStatus.INELIGIBLE
            reasons.append(f"Ready timeframes ({len(ready_tfs)}) < required ({criteria.min_required_timeframes})")
        elif score < criteria.min_symbol_score:
            status = SymbolReadinessStatus.INELIGIBLE
            reasons.append(f"Readiness score ({score:.1f}) < minimum ({criteria.min_symbol_score:.1f})")
        elif (missing_tfs or failed_tfs):
            if criteria.allow_partial_symbols:
                status = SymbolReadinessStatus.PARTIAL
                reasons.append(f"Partial data. Missing: {missing_tfs}, Failed: {failed_tfs}")
            else:
                status = SymbolReadinessStatus.INELIGIBLE
                reasons.append(f"Partial symbols not allowed. Missing: {missing_tfs}, Failed: {failed_tfs}")

        if status == SymbolReadinessStatus.INELIGIBLE:
             if failed_tfs:
                 status = SymbolReadinessStatus.FAILED_VALIDATION
             elif missing_tfs:
                 status = SymbolReadinessStatus.MISSING_DATA

        decision = SymbolReadinessDecision(
            symbol=symbol,
            status=status,
            score=score,
            ready_timeframes=ready_tfs,
            missing_timeframes=missing_tfs,
            failed_timeframes=failed_tfs,
            reasons=reasons
        )
        decisions.append(decision)

    return decisions


def evaluate_universe_readiness_gate(
    universe: UniverseDefinition,
    readiness_report: DataReadinessReport,
    criteria: Optional[UniverseReadinessGateCriteria] = None
) -> UniverseReadinessGateReport:

    if not criteria:
        criteria = default_universe_readiness_gate_criteria()

    decisions = symbol_decisions_from_readiness(universe, readiness_report, criteria)

    total = len(decisions)
    if total == 0:
        return UniverseReadinessGateReport(
            report_id=f"urg_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            universe_name=universe.name,
            total_symbols=0,
            eligible_symbols=0,
            partial_symbols=0,
            ineligible_symbols=0,
            missing_data_symbols=0,
            failed_validation_symbols=0,
            eligible_symbol_ratio=0.0,
            failed_symbol_ratio=0.0,
            status=UniverseReadinessGateStatus.FAILED,
            decisions=[],
            blocking_reasons=["No active symbols to evaluate"]
        )

    eligible = sum(1 for d in decisions if d.status == SymbolReadinessStatus.ELIGIBLE)
    partial = sum(1 for d in decisions if d.status == SymbolReadinessStatus.PARTIAL)
    ineligible = sum(1 for d in decisions if d.status == SymbolReadinessStatus.INELIGIBLE)
    missing = sum(1 for d in decisions if d.status == SymbolReadinessStatus.MISSING_DATA)
    failed_val = sum(1 for d in decisions if d.status == SymbolReadinessStatus.FAILED_VALIDATION)

    eligible_ratio = (eligible + partial) / total if total > 0 else 0.0
    failed_ratio = (failed_val + missing + ineligible) / total if total > 0 else 0.0

    status = UniverseReadinessGateStatus.PASSED
    blocking_reasons = []

    if eligible_ratio < criteria.min_eligible_symbol_ratio and total > 0:
        status = UniverseReadinessGateStatus.FAILED
        blocking_reasons.append(f"Eligible ratio ({eligible_ratio:.2f}) < minimum ({criteria.min_eligible_symbol_ratio:.2f})")

    if failed_ratio > criteria.max_failed_symbol_ratio:
        status = UniverseReadinessGateStatus.FAILED
        blocking_reasons.append(f"Failed ratio ({failed_ratio:.2f}) > maximum ({criteria.max_failed_symbol_ratio:.2f})")

    if status == UniverseReadinessGateStatus.PASSED and partial > 0 and eligible == 0:
        status = UniverseReadinessGateStatus.PARTIAL

    report = UniverseReadinessGateReport(
        report_id=f"urg_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        universe_name=universe.name,
        total_symbols=total,
        eligible_symbols=eligible,
        partial_symbols=partial,
        ineligible_symbols=ineligible,
        missing_data_symbols=missing,
        failed_validation_symbols=failed_val,
        eligible_symbol_ratio=eligible_ratio,
        failed_symbol_ratio=failed_ratio,
        status=status,
        decisions=decisions,
        blocking_reasons=blocking_reasons
    )

    return report


def get_eligible_symbols(report: UniverseReadinessGateReport) -> List[str]:
    return [d.symbol for d in report.decisions if d.status in (SymbolReadinessStatus.ELIGIBLE, SymbolReadinessStatus.PARTIAL)]

def get_ineligible_symbols(report: UniverseReadinessGateReport) -> List[str]:
    return [d.symbol for d in report.decisions if d.status not in (SymbolReadinessStatus.ELIGIBLE, SymbolReadinessStatus.PARTIAL)]

def universe_readiness_gate_report_to_text(report: UniverseReadinessGateReport) -> str:
    lines = [
        "=== Universe Readiness Gate Report ===",
        f"Universe Name     : {report.universe_name}",
        f"Status            : {report.status.value}",
        f"Total Symbols     : {report.total_symbols}",
        f"Eligible          : {report.eligible_symbols}",
        f"Partial           : {report.partial_symbols}",
        f"Ineligible        : {report.ineligible_symbols}",
        f"Missing Data      : {report.missing_data_symbols}",
        f"Failed Validation : {report.failed_validation_symbols}",
        f"Eligible Ratio    : {report.eligible_symbol_ratio:.2%}",
        f"Failed Ratio      : {report.failed_symbol_ratio:.2%}"
    ]

    if report.blocking_reasons:
        lines.append("\nBlocking Reasons:")
        for r in report.blocking_reasons:
            lines.append(f" - {r}")

    if report.warnings:
        lines.append("\nWarnings:")
        for w in report.warnings:
            lines.append(f" - {w}")

    return "\n".join(lines)


def write_universe_readiness_gate_report_json(path: Path, report: UniverseReadinessGateReport) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "report_id": report.report_id,
        "created_at_utc": report.created_at_utc,
        "universe_name": report.universe_name,
        "total_symbols": report.total_symbols,
        "eligible_symbols": report.eligible_symbols,
        "partial_symbols": report.partial_symbols,
        "ineligible_symbols": report.ineligible_symbols,
        "missing_data_symbols": report.missing_data_symbols,
        "failed_validation_symbols": report.failed_validation_symbols,
        "eligible_symbol_ratio": report.eligible_symbol_ratio,
        "failed_symbol_ratio": report.failed_symbol_ratio,
        "status": report.status.value,
        "decisions": [
            {
                "symbol": d.symbol,
                "status": d.status.value,
                "score": d.score,
                "ready_timeframes": d.ready_timeframes,
                "missing_timeframes": d.missing_timeframes,
                "failed_timeframes": d.failed_timeframes,
                "reasons": d.reasons
            }
            for d in report.decisions
        ],
        "blocking_reasons": report.blocking_reasons,
        "warnings": report.warnings
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return path


def write_eligible_symbols_csv(path: Path, report: UniverseReadinessGateReport) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    eligible = get_eligible_symbols(report)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["symbol"])
        for sym in eligible:
            writer.writerow([sym])

    return path


def write_eligible_symbols_txt(path: Path, report: UniverseReadinessGateReport) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    eligible = get_eligible_symbols(report)

    with open(path, "w", encoding="utf-8") as f:
        for sym in eligible:
            f.write(f"{sym}\n")

    return path

def assert_universe_readiness_gate_passed(report: UniverseReadinessGateReport) -> None:
    if report.status == UniverseReadinessGateStatus.FAILED:
        raise UniverseReadinessGateError(f"Universe Readiness Gate failed: {', '.join(report.blocking_reasons)}")
