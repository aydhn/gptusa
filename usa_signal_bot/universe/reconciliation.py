import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from usa_signal_bot.core.enums import UniverseConflictResolution
from usa_signal_bot.universe.models import UniverseDefinition, UniverseSymbol
from usa_signal_bot.universe.sources import UniverseSourceLoadResult
from usa_signal_bot.core.exceptions import UniverseReconciliationError

@dataclass
class UniverseConflict:
    symbol: str
    field: str
    existing_value: Any
    incoming_value: Any
    existing_source: Optional[str]
    incoming_source: Optional[str]
    resolution: Optional[str] = None

@dataclass
class UniverseReconciliationReport:
    report_id: str
    created_at_utc: str
    total_input_symbols: int
    total_output_symbols: int
    duplicate_count: int
    conflict_count: int
    conflicts: List[UniverseConflict] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def reconcile_universe_symbols(
    sources: List[UniverseSourceLoadResult],
    resolution: UniverseConflictResolution = UniverseConflictResolution.PREFER_COMPLETE_METADATA
) -> Tuple[UniverseDefinition, UniverseReconciliationReport]:
    import uuid

    report = UniverseReconciliationReport(
        report_id=f"recon_{uuid.uuid4().hex[:8]}",
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        total_input_symbols=0,
        total_output_symbols=0,
        duplicate_count=0,
        conflict_count=0
    )

    merged_symbols: Dict[str, Tuple[UniverseSymbol, str]] = {} # symbol -> (UniverseSymbol, source_name)

    # Process sources deterministically
    # Source list is expected to be pre-sorted by priority
    for src_result in sources:
        if not src_result.success or not src_result.universe:
            continue

        source_name = src_result.source.name

        for symbol in src_result.universe.symbols:
            report.total_input_symbols += 1

            sym_str = symbol.symbol

            if sym_str not in merged_symbols:
                merged_symbols[sym_str] = (symbol, source_name)
            else:
                report.duplicate_count += 1
                existing_sym, existing_src = merged_symbols[sym_str]

                resolved_sym, conflicts = resolve_symbol_conflict(
                    existing=existing_sym,
                    incoming=symbol,
                    resolution=resolution,
                    existing_source=existing_src,
                    incoming_source=source_name
                )

                if conflicts:
                    report.conflict_count += len(conflicts)
                    report.conflicts.extend(conflicts)

                # For first wins, keep existing source attribution
                # For last wins, update to new source attribution
                # For others, use whichever symbol we kept
                if resolution == UniverseConflictResolution.LAST_WINS:
                     merged_symbols[sym_str] = (resolved_sym, source_name)
                elif resolution == UniverseConflictResolution.FIRST_WINS:
                     merged_symbols[sym_str] = (resolved_sym, existing_src)
                else:
                    # If resolved symbol has same metadata as incoming (we preferred incoming), use new source
                    if resolved_sym is symbol:
                        merged_symbols[sym_str] = (resolved_sym, source_name)
                    else:
                        # We preferred existing, but may have merged metadata. Still attribute to existing.
                        merged_symbols[sym_str] = (resolved_sym, existing_src)

    report.total_output_symbols = len(merged_symbols)

    final_universe = UniverseDefinition(
        name="reconciled_universe",
        symbols=[s for s, _ in merged_symbols.values()],
        created_from="reconciliation"
    )

    return final_universe, report

def resolve_symbol_conflict(
    existing: UniverseSymbol,
    incoming: UniverseSymbol,
    resolution: UniverseConflictResolution,
    existing_source: Optional[str] = None,
    incoming_source: Optional[str] = None
) -> Tuple[UniverseSymbol, List[UniverseConflict]]:

    conflicts = []

    # Detect conflicts
    if existing.asset_type != incoming.asset_type:
        conflicts.append(UniverseConflict(
            symbol=existing.symbol,
            field="asset_type",
            existing_value=existing.asset_type.value if hasattr(existing.asset_type, 'value') else str(existing.asset_type),
            incoming_value=incoming.asset_type.value if hasattr(incoming.asset_type, 'value') else str(incoming.asset_type),
            existing_source=existing_source,
            incoming_source=incoming_source
        ))

    if existing.exchange and incoming.exchange and existing.exchange != incoming.exchange:
        conflicts.append(UniverseConflict(
            symbol=existing.symbol,
            field="exchange",
            existing_value=existing.exchange,
            incoming_value=incoming.exchange,
            existing_source=existing_source,
            incoming_source=incoming_source
        ))

    if resolution == UniverseConflictResolution.ERROR_ON_CONFLICT and conflicts:
        raise UniverseReconciliationError(f"Conflict detected for {existing.symbol} and resolution is ERROR_ON_CONFLICT")

    if resolution == UniverseConflictResolution.FIRST_WINS:
        for c in conflicts: c.resolution = "Kept FIRST_WINS"
        return existing, conflicts

    if resolution == UniverseConflictResolution.LAST_WINS:
        for c in conflicts: c.resolution = "Kept LAST_WINS"
        return incoming, conflicts

    if resolution == UniverseConflictResolution.PREFER_ACTIVE:
        if existing.active and not incoming.active:
            for c in conflicts: c.resolution = "Kept EXISTING (Active)"
            return merge_symbol_metadata(existing, incoming), conflicts
        elif not existing.active and incoming.active:
            for c in conflicts: c.resolution = "Kept INCOMING (Active)"
            return merge_symbol_metadata(incoming, existing), conflicts

        # Fall back to complete metadata if both are active/inactive
        resolution = UniverseConflictResolution.PREFER_COMPLETE_METADATA

    if resolution == UniverseConflictResolution.PREFER_COMPLETE_METADATA:
        ex_score = score_metadata_completeness(existing)
        in_score = score_metadata_completeness(incoming)

        if in_score > ex_score:
            for c in conflicts: c.resolution = "Kept INCOMING (More metadata)"
            return merge_symbol_metadata(incoming, existing), conflicts
        else:
            for c in conflicts: c.resolution = "Kept EXISTING (More/equal metadata)"
            return merge_symbol_metadata(existing, incoming), conflicts

    return existing, conflicts

def score_metadata_completeness(symbol: UniverseSymbol) -> int:
    score = 0
    if symbol.name: score += 1
    if symbol.exchange: score += 1
    if symbol.sector: score += 1
    if symbol.industry: score += 1
    return score

def merge_symbol_metadata(base: UniverseSymbol, supplementary: UniverseSymbol) -> UniverseSymbol:
    import copy
    merged = copy.deepcopy(base)

    if not merged.name and supplementary.name:
        merged.name = supplementary.name
    if not merged.exchange and supplementary.exchange:
        merged.exchange = supplementary.exchange
    if not merged.sector and supplementary.sector:
        merged.sector = supplementary.sector
    if not merged.industry and supplementary.industry:
        merged.industry = supplementary.industry

    return merged

def reconciliation_report_to_text(report: UniverseReconciliationReport) -> str:
    lines = [
        "--- Universe Reconciliation Report ---",
        f"Report ID : {report.report_id}",
        f"Time      : {report.created_at_utc}",
        f"Input     : {report.total_input_symbols} symbols",
        f"Output    : {report.total_output_symbols} symbols",
        f"Duplicates: {report.duplicate_count}",
        f"Conflicts : {report.conflict_count}"
    ]

    if report.errors:
        lines.append("\nErrors:")
        for e in report.errors:
            lines.append(f"  - {e}")

    if report.warnings:
        lines.append("\nWarnings:")
        for w in report.warnings:
            lines.append(f"  - {w}")

    return "\n".join(lines)

def write_reconciliation_report_json(path: Path, report: UniverseReconciliationReport) -> Path:
    from usa_signal_bot.core.serialization import DefaultJSONEncoder

    path.parent.mkdir(parents=True, exist_ok=True)

    # Use atomic write pattern
    import tempfile
    import os

    fd, temp_path_str = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    temp_path = Path(temp_path_str)

    try:
        report_dict = {
            "report_id": report.report_id,
            "created_at_utc": report.created_at_utc,
            "total_input_symbols": report.total_input_symbols,
            "total_output_symbols": report.total_output_symbols,
            "duplicate_count": report.duplicate_count,
            "conflict_count": report.conflict_count,
            "conflicts": [
                {
                    "symbol": c.symbol,
                    "field": c.field,
                    "existing_value": c.existing_value,
                    "incoming_value": c.incoming_value,
                    "existing_source": c.existing_source,
                    "incoming_source": c.incoming_source,
                    "resolution": c.resolution
                } for c in report.conflicts
            ],
            "warnings": report.warnings,
            "errors": report.errors
        }

        with open(fd, "w", encoding="utf-8") as f:
            json.dump(report_dict, f, cls=DefaultJSONEncoder, indent=2)

        os.replace(temp_path, path)
    except Exception:
        if temp_path.exists():
            temp_path.unlink()
        raise

    return path
