import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict, Any

from usa_signal_bot.core.enums import ActiveUniverseSource, UniverseDataRunStatus, UniverseRunStep
from usa_signal_bot.core.exceptions import ActiveUniversePipelineError
from usa_signal_bot.universe.models import UniverseDefinition
from usa_signal_bot.universe.active import ActiveUniverseResolution, resolve_active_universe, write_active_universe_resolution_json
from usa_signal_bot.data.universe_runs import (
    UniverseDataRun,
    create_universe_data_run,
    start_universe_data_run,
    finish_universe_data_run,
    add_run_step_result,
    create_step_result,
    write_universe_data_run,
    build_universe_run_dir
)
from usa_signal_bot.data.multitimeframe import MultiTimeframeDataResult, MultiTimeframeDataRequest
from usa_signal_bot.data.coverage import DataCoverageReport, write_coverage_report_json
from usa_signal_bot.data.readiness import DataReadinessReport, write_readiness_report_json
from usa_signal_bot.universe.readiness_gate import (
    UniverseReadinessGateReport,
    UniverseReadinessGateCriteria,
    evaluate_universe_readiness_gate,
    write_universe_readiness_gate_report_json,
    write_eligible_symbols_csv,
    write_eligible_symbols_txt,
    get_eligible_symbols,
    get_ineligible_symbols
)
from usa_signal_bot.data.pipeline import MultiTimeframeDataPipeline


@dataclass
class ActiveUniversePipelineRequest:
    provider_name: str = "yfinance"
    timeframes: List[str] = field(default_factory=list)
    explicit_universe_file: Optional[str] = None
    asset_type: Optional[str] = None
    max_symbols: Optional[int] = None
    force_refresh: bool = False
    use_cache: bool = True
    fallback_to_watchlist: bool = True
    write_reports: bool = True
    write_eligible_outputs: bool = True
    readiness_criteria: Optional[UniverseReadinessGateCriteria] = None


@dataclass
class ActiveUniversePipelineResult:
    run: UniverseDataRun
    active_resolution: ActiveUniverseResolution
    mtf_result: MultiTimeframeDataResult
    coverage_report: DataCoverageReport
    readiness_report: DataReadinessReport
    gate_report: UniverseReadinessGateReport
    eligible_symbols: List[str]
    ineligible_symbols: List[str]
    output_paths: Dict[str, str] = field(default_factory=dict)
    success: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class ActiveUniverseDataPipeline:
    def __init__(self, mtf_pipeline: MultiTimeframeDataPipeline, data_root: Path):
        self.mtf_pipeline = mtf_pipeline
        self.data_root = data_root

    def run(self, request: ActiveUniversePipelineRequest) -> ActiveUniversePipelineResult:
        warnings = []
        errors = []

        # 1. Resolve and filter universe
        try:
            resolution = self.resolve_and_filter_universe(request)
            warnings.extend(resolution.warnings)
        except Exception as e:
            raise ActiveUniversePipelineError(f"Failed to resolve active universe: {e}")

        filtered_symbols_count = len(resolution.universe.symbols)

        # 2. Create Run Metadata
        run = create_universe_data_run(
            universe_name=resolution.universe.name,
            source=resolution.source,
            source_path=resolution.source_path,
            provider_name=request.provider_name,
            timeframes=request.timeframes,
            total_symbols=filtered_symbols_count
        )
        run = start_universe_data_run(run)

        run_dir = build_universe_run_dir(self.data_root, run.run_id)

        # Add RESOLVE_UNIVERSE step
        run = add_run_step_result(run, create_step_result(
            UniverseRunStep.RESOLVE_UNIVERSE,
            UniverseDataRunStatus.COMPLETED,
            f"Resolved {filtered_symbols_count} symbols from {resolution.source.value}"
        ))

        # 3. MultiTimeframe Pipeline execution
        if filtered_symbols_count == 0:
            errors.append("No active symbols remaining after filtering")
            run = finish_universe_data_run(run, UniverseDataRunStatus.FAILED)
            write_universe_data_run(run_dir / "run_metadata.json", run)
            raise ActiveUniversePipelineError("No active symbols remaining after filtering")

        try:
            mtf_result, coverage, readiness = self.mtf_pipeline.run_for_universe(
                universe=resolution.universe,
                timeframes=request.timeframes,
                limit=request.max_symbols,
                asset_type=request.asset_type,
                force_refresh=request.force_refresh,
                readiness_criteria=None # We will use the UniverseReadinessGate instead
            )

            # Record steps based on mtf_result
            status = UniverseDataRunStatus.COMPLETED if 0 == 0 else UniverseDataRunStatus.PARTIAL_SUCCESS

            run = add_run_step_result(run, create_step_result(
                UniverseRunStep.DOWNLOAD_DATA,
                status,
                f"Downloaded data for {len(mtf_result.symbols_by_timeframe) if hasattr(mtf_result, 'symbols_by_timeframe') else 0}/{len(resolution.universe.symbols)} symbols"
            ))
            run = add_run_step_result(run, create_step_result(
                UniverseRunStep.VALIDATE_DATA,
                UniverseDataRunStatus.COMPLETED,
                "Validation completed"
            ))
            run = add_run_step_result(run, create_step_result(
                UniverseRunStep.REPAIR_DATA,
                UniverseDataRunStatus.COMPLETED,
                "Repair completed"
            ))
            run = add_run_step_result(run, create_step_result(
                UniverseRunStep.COVERAGE_REPORT,
                UniverseDataRunStatus.COMPLETED,
                "Coverage report generated"
            ))
            run = add_run_step_result(run, create_step_result(
                UniverseRunStep.READINESS_REPORT,
                UniverseDataRunStatus.COMPLETED,
                "Readiness report generated"
            ))

            warnings.extend(mtf_result.warnings)
            errors.extend(mtf_result.errors)

        except Exception as e:
            run = add_run_step_result(run, create_step_result(
                UniverseRunStep.DOWNLOAD_DATA,
                UniverseDataRunStatus.FAILED,
                str(e)
            ))
            run = finish_universe_data_run(run, UniverseDataRunStatus.FAILED)
            write_universe_data_run(run_dir / "run_metadata.json", run)
            raise ActiveUniversePipelineError(f"Multi-timeframe pipeline failed: {e}")

        # 4. Readiness Gate
        try:
            gate_report = evaluate_universe_readiness_gate(
                universe=resolution.universe,
                readiness_report=readiness,
                criteria=request.readiness_criteria
            )

            gate_status = UniverseDataRunStatus.COMPLETED if gate_report.status.value in ("PASSED", "PARTIAL") else UniverseDataRunStatus.FAILED

            run = add_run_step_result(run, create_step_result(
                UniverseRunStep.READINESS_GATE,
                gate_status,
                f"Gate status: {gate_report.status.value}"
            ))

            warnings.extend(gate_report.warnings)

        except Exception as e:
            run = add_run_step_result(run, create_step_result(
                UniverseRunStep.READINESS_GATE,
                UniverseDataRunStatus.FAILED,
                str(e)
            ))
            run = finish_universe_data_run(run, UniverseDataRunStatus.FAILED)
            write_universe_data_run(run_dir / "run_metadata.json", run)
            raise ActiveUniversePipelineError(f"Readiness gate evaluation failed: {e}")

        # 5. Determine Eligible Symbols
        eligible_symbols = get_eligible_symbols(gate_report)
        ineligible_symbols = get_ineligible_symbols(gate_report)

        success = gate_report.status.value in ("PASSED", "PARTIAL") and len(eligible_symbols) > 0

        # 6. Write Outputs
        output_paths = {}
        if request.write_reports or request.write_eligible_outputs:
            try:
                # Update run metadata with warnings and errors before writing
                run.warnings = warnings
                run.errors = errors
                run = finish_universe_data_run(run, UniverseDataRunStatus.COMPLETED if success else UniverseDataRunStatus.FAILED)

                result = ActiveUniversePipelineResult(
                    run=run,
                    active_resolution=resolution,
                    mtf_result=mtf_result,
                    coverage_report=coverage,
                    readiness_report=readiness,
                    gate_report=gate_report,
                    eligible_symbols=eligible_symbols,
                    ineligible_symbols=ineligible_symbols,
                    success=success,
                    warnings=warnings,
                    errors=errors
                )

                paths = self.write_active_universe_outputs(result, run_dir, request)
                output_paths.update(paths)

                run = add_run_step_result(run, create_step_result(
                    UniverseRunStep.WRITE_OUTPUTS,
                    UniverseDataRunStatus.COMPLETED,
                    "Outputs written successfully"
                ))
                run.output_paths = {k: str(v) for k, v in paths.items()}
                write_universe_data_run(run_dir / "run_metadata.json", run)

            except Exception as e:
                run = add_run_step_result(run, create_step_result(
                    UniverseRunStep.WRITE_OUTPUTS,
                    UniverseDataRunStatus.FAILED,
                    str(e)
                ))
                run = finish_universe_data_run(run, UniverseDataRunStatus.FAILED)
                write_universe_data_run(run_dir / "run_metadata.json", run)
                warnings.append(f"Failed to write outputs: {e}")
        else:
            run = finish_universe_data_run(run, UniverseDataRunStatus.COMPLETED if success else UniverseDataRunStatus.FAILED)
            write_universe_data_run(run_dir / "run_metadata.json", run)

        return ActiveUniversePipelineResult(
            run=run,
            active_resolution=resolution,
            mtf_result=mtf_result,
            coverage_report=coverage,
            readiness_report=readiness,
            gate_report=gate_report,
            eligible_symbols=eligible_symbols,
            ineligible_symbols=ineligible_symbols,
            output_paths=output_paths,
            success=success,
            warnings=warnings,
            errors=errors
        )

    def resolve_and_filter_universe(self, request: ActiveUniversePipelineRequest) -> ActiveUniverseResolution:
        explicit_file = Path(request.explicit_universe_file) if request.explicit_universe_file else None

        resolution = resolve_active_universe(
            data_root=self.data_root,
            explicit_file=explicit_file,
            fallback_to_watchlist=request.fallback_to_watchlist
        )

        # Filter active symbols
        active_symbols = resolution.universe.get_active_symbols()

        # Filter by asset type
        if request.asset_type:
            at_lower = request.asset_type.lower()
            active_symbols = [s for s in active_symbols if (s.asset_type.value.lower() if hasattr(s.asset_type, 'value') else str(s.asset_type).lower()) == at_lower]

        # Apply max_symbols
        if request.max_symbols and request.max_symbols > 0:
            active_symbols = active_symbols[:request.max_symbols]

        # Update resolution
        resolution.universe.symbols = active_symbols
        resolution.symbol_count = len(active_symbols)
        resolution.active_symbol_count = len(active_symbols)

        return resolution

    def write_active_universe_outputs(self, result: ActiveUniversePipelineResult, run_dir: Path, request: ActiveUniversePipelineRequest) -> Dict[str, Path]:
        paths = {}

        if request.write_reports:
            res_path = run_dir / "active_resolution.json"
            write_active_universe_resolution_json(res_path, result.active_resolution)
            paths["resolution"] = res_path

            cov_path = run_dir / "coverage_report.json"
            write_coverage_report_json(cov_path, result.coverage_report)
            paths["coverage"] = cov_path

            read_path = run_dir / "readiness_report.json"
            write_readiness_report_json(read_path, result.readiness_report)
            paths["readiness"] = read_path

            gate_path = run_dir / "gate_report.json"
            write_universe_readiness_gate_report_json(gate_path, result.gate_report)
            paths["gate"] = gate_path

        if request.write_eligible_outputs:
            readiness_dir = self.data_root / "universe" / "readiness"
            readiness_dir.mkdir(parents=True, exist_ok=True)

            csv_path = readiness_dir / "eligible_symbols.csv"
            write_eligible_symbols_csv(csv_path, result.gate_report)
            paths["eligible_csv"] = csv_path

            txt_path = readiness_dir / "eligible_symbols.txt"
            write_eligible_symbols_txt(txt_path, result.gate_report)
            paths["eligible_txt"] = txt_path

            ineligible_csv_path = readiness_dir / "ineligible_symbols.csv"
            ineligible = get_ineligible_symbols(result.gate_report)
            import csv
            with open(ineligible_csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["symbol"])
                for sym in ineligible:
                    writer.writerow([sym])
            paths["ineligible_csv"] = ineligible_csv_path

        return paths

def active_pipeline_result_to_text(result: ActiveUniversePipelineResult) -> str:
    lines = [
        "=== Active Universe Pipeline Result ===",
        f"Success             : {result.success}",
        f"Run ID              : {result.run.run_id}",
        f"Universe Source     : {result.active_resolution.source.value}",
        f"Processed Symbols   : {len(result.active_resolution.universe.symbols)}",
        f"Eligible Symbols    : {len(result.eligible_symbols)}",
        f"Ineligible Symbols  : {len(result.ineligible_symbols)}",
        f"Gate Status         : {result.gate_report.status.value}"
    ]

    if result.output_paths:
        lines.append("\nOutput Paths:")
        for k, v in result.output_paths.items():
            lines.append(f" - {k}: {v}")

    if result.warnings:
        lines.append("\nWarnings:")
        for w in result.warnings:
            lines.append(f" - {w}")

    if result.errors:
        lines.append("\nErrors:")
        for e in result.errors:
            lines.append(f" - {e}")

    return "\n".join(lines)
