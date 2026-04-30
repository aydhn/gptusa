import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from usa_signal_bot.core.enums import UniverseConflictResolution, UniverseLayer
from usa_signal_bot.universe.models import UniverseDefinition, UniverseSummary, UniverseValidationReport
from usa_signal_bot.universe.sources import UniverseSource, UniverseSourceLoadResult
from usa_signal_bot.universe.reconciliation import UniverseReconciliationReport, reconcile_universe_symbols
from usa_signal_bot.universe.loader import load_universe_csv
from usa_signal_bot.universe.filters import apply_universe_filter, UniverseFilter
from usa_signal_bot.universe.reporting import summarize_universe
from usa_signal_bot.universe.validator import assert_universe_valid
from usa_signal_bot.core.exceptions import UniverseSourceError

@dataclass
class UniverseExpansionRequest:
    name: str
    sources: List[UniverseSource]
    include_layers: Optional[List[UniverseLayer]] = None
    exclude_layers: Optional[List[UniverseLayer]] = None
    include_stocks: bool = True
    include_etfs: bool = True
    include_inactive: bool = False
    max_symbols: Optional[int] = None
    conflict_resolution: UniverseConflictResolution = UniverseConflictResolution.PREFER_COMPLETE_METADATA
    write_snapshot: bool = True

@dataclass
class UniverseExpansionResult:
    request: UniverseExpansionRequest
    universe: UniverseDefinition
    source_results: List[UniverseSourceLoadResult]
    reconciliation_report: UniverseReconciliationReport
    validation_report: UniverseValidationReport
    summary: UniverseSummary
    snapshot_path: Optional[str]
    success: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def expand_universe(request: UniverseExpansionRequest, data_root: Path) -> UniverseExpansionResult:
    warnings = []
    errors = []

    # 1. Filter sources
    filtered_sources = filter_sources_by_layer(request.sources, request.include_layers, request.exclude_layers)
    if not filtered_sources:
        raise UniverseSourceError("No valid sources remaining after applying layer filters.")

    # Sort by priority ascending
    filtered_sources.sort(key=lambda x: x.priority)

    # 2. Load sources
    source_results = load_sources_for_expansion(filtered_sources, data_root)

    success_sources = [r for r in source_results if r.success and r.universe]
    if not success_sources:
         raise UniverseSourceError("Failed to load any valid universes from the provided sources.")

    for r in source_results:
        if not r.success:
            errors.extend([f"[{r.source.name}] {e}" for e in r.errors])
        warnings.extend([f"[{r.source.name}] {w}" for w in r.warnings])

    # 3. Reconcile
    reconciled_universe, recon_report = reconcile_universe_symbols(success_sources, request.conflict_resolution)
    reconciled_universe.name = request.name

    # 4. Apply expansion filters (asset type, max symbols, etc)
    final_universe = apply_expansion_filters(reconciled_universe, request)

    if not final_universe.symbols:
        raise UniverseSourceError("No symbols remaining after applying expansion filters.")

    # 5. Validate final
    val_report = UniverseValidationReport(passed=True, total_rows=len(final_universe.symbols), valid_rows=len(final_universe.symbols), source_path='expansion')

    # 6. Summarize
    summary = summarize_universe(final_universe)

    # 7. Write Snapshot if requested
    snapshot_path = None
    if request.write_snapshot:
        from usa_signal_bot.universe.snapshots import write_universe_snapshot
        snapshot = write_universe_snapshot(
            data_root=data_root,
            universe=final_universe,
            summary=summary,
            validation_report=val_report,
            reconciliation_report=recon_report,
            name=request.name
        )
        snapshot_path = snapshot.universe_file

    return UniverseExpansionResult(
        request=request,
        universe=final_universe,
        source_results=source_results,
        reconciliation_report=recon_report,
        validation_report=val_report,
        summary=summary,
        snapshot_path=snapshot_path,
        success=True,
        warnings=warnings,
        errors=errors
    )

def load_sources_for_expansion(sources: List[UniverseSource], data_root: Path) -> List[UniverseSourceLoadResult]:
    results = []

    for src in sources:
        if not src.enabled:
            continue

        res = UniverseSourceLoadResult(
            source=src,
            universe=None,
            success=False,
            symbol_count=0
        )

        try:
            if not src.path:
                res.errors.append(f"Source {src.name} has no path defined")
                results.append(res)
                continue

            p = Path(src.path)
            if not p.is_absolute():
                p = data_root / p

            load_res = load_universe_csv(p, src.name)

            res.universe = load_res.universe
            res.success = True
            res.symbol_count = load_res.valid_count
            res.warnings.extend(load_res.warnings)
            res.errors.extend(load_res.errors)

        except Exception as e:
            res.errors.append(str(e))

        results.append(res)

    return results

def filter_sources_by_layer(
    sources: List[UniverseSource],
    include_layers: Optional[List[UniverseLayer]],
    exclude_layers: Optional[List[UniverseLayer]]
) -> List[UniverseSource]:

    filtered = []
    for src in sources:
        if not src.enabled:
            continue

        if exclude_layers and src.layer in exclude_layers:
            continue

        if include_layers and src.layer not in include_layers:
            continue

        filtered.append(src)

    return filtered

def apply_expansion_filters(universe: UniverseDefinition, request: UniverseExpansionRequest) -> UniverseDefinition:
    ufilter = UniverseFilter(
        include_stocks=request.include_stocks,
        include_etfs=request.include_etfs,
        max_symbols=request.max_symbols
    )

    # Our standard apply_universe_filter strips inactive symbols.
    # If include_inactive is true, we must manually filter instead to preserve them.
    if request.include_inactive:
        from usa_signal_bot.universe.filters import filter_by_asset_type, limit_universe
        u = filter_by_asset_type(universe, request.include_stocks, request.include_etfs)
        u = limit_universe(u, request.max_symbols)
        return u
    else:
        return apply_universe_filter(universe, ufilter)

def expansion_result_to_text(result: UniverseExpansionResult) -> str:
    lines = [
        "=== Universe Expansion Result ===",
        f"Name          : {result.request.name}",
        f"Success       : {'Yes' if result.success else 'No'}",
        f"Total Symbols : {len(result.universe.symbols)}",
        f"Snapshot Path : {result.snapshot_path or 'Not created'}",
        "\nSources Processed:"
    ]

    for r in result.source_results:
        status = "OK" if r.success else "FAIL"
        lines.append(f"  - [{status}] {r.source.name} ({r.symbol_count} symbols)")

    if result.reconciliation_report:
        lines.append(f"\nReconciliation:")
        lines.append(f"  Duplicates resolved : {result.reconciliation_report.duplicate_count}")
        lines.append(f"  Conflicts handled   : {result.reconciliation_report.conflict_count}")

    if result.errors:
        lines.append("\nErrors:")
        for e in result.errors:
            lines.append(f"  - {e}")

    if result.warnings:
        lines.append("\nWarnings:")
        for w in result.warnings:
            lines.append(f"  - {w}")

    return "\n".join(lines)

def write_expansion_result_json(path: Path, result: UniverseExpansionResult) -> Path:
    from usa_signal_bot.core.serialization import DefaultJSONEncoder

    path.parent.mkdir(parents=True, exist_ok=True)

    import tempfile
    import os
    fd, temp_path_str = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    temp_path = Path(temp_path_str)

    try:
        data = {
            "request": {
                "name": result.request.name,
                "include_stocks": result.request.include_stocks,
                "include_etfs": result.request.include_etfs,
                "max_symbols": result.request.max_symbols
            },
            "success": result.success,
            "total_symbols": len(result.universe.symbols),
            "snapshot_path": result.snapshot_path,
            "warnings": result.warnings,
            "errors": result.errors
        }

        with open(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, cls=DefaultJSONEncoder, indent=2)

        os.replace(temp_path, path)
    except Exception:
        if temp_path.exists():
            temp_path.unlink()
        raise

    return path
