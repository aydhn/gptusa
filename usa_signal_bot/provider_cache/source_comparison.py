from typing import Any
from pathlib import Path
from datetime import datetime, timezone
from usa_signal_bot.provider_cache.phase108_models import (
    SourceComparisonInput,
    SourceComparisonResult,
    ProviderCacheRecord,
    create_source_comparison_id,
    create_source_comparison_result_id,
    SourceComparisonStatus,
    SourceConfidenceLevel,
    ProviderCacheRiskFlag
)
from usa_signal_bot.provider_cache.ohlcv_comparison import compare_ohlcv_records
from usa_signal_bot.provider_cache.cache_store import read_provider_cache_csv

def build_source_comparison_input(symbol: str, source_records: list[ProviderCacheRecord], capability: str = "GET_DAILY_OHLCV", interval: str | None = "1d") -> SourceComparisonInput:
    return SourceComparisonInput(
        comparison_id=create_source_comparison_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        symbol=symbol,
        capability=capability,
        interval=interval,
        source_records=source_records,
        compare_columns=["close", "volume", "timestamp"],
        tolerance_pct=0.5,
        min_rows_required=1,
        dry_run_only=True,
        metadata={}
    )

def run_source_comparison(input_item: SourceComparisonInput, cache_root: Path | None = None) -> SourceComparisonResult:
    # Read actual records if cache_root is not None, else simulate
    source_data = {}
    if cache_root:
        for r in input_item.source_records:
            if r.cache_path and Path(r.cache_path).exists():
                 source_data[r.provider_name] = read_provider_cache_csv(Path(r.cache_path))
    else:
        # Provide dummy data
        for r in input_item.source_records:
             source_data[r.provider_name] = [{"timestamp": "2024-01-01", "close": 150.0, "volume": 10000}]

    return run_source_comparison_from_records(input_item.symbol, source_data, input_item.tolerance_pct)

def run_source_comparison_from_records(symbol: str, sources: dict[str, list[dict[str, Any]]], tolerance_pct: float = 0.5) -> SourceComparisonResult:
    if len(sources) < 2:
        return _build_failed_comparison(symbol, "Need at least 2 sources to compare")

    names = list(sources.keys())
    data_a = sources[names[0]]
    data_b = sources[names[1]]

    comp = compare_ohlcv_records(data_a, data_b, tolerance_pct)

    material_diff = comp.get("material_difference", False)
    status = SourceComparisonStatus.MATERIAL_DIFFERENCE if material_diff else SourceComparisonStatus.MATCH
    confidence = SourceConfidenceLevel.LOW if material_diff else SourceConfidenceLevel.HIGH

    risk_flags = []
    if material_diff:
        risk_flags.append(ProviderCacheRiskFlag.SOURCE_DISAGREEMENT_HIGH)

    return SourceComparisonResult(
        result_id=create_source_comparison_result_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        comparison_id=None,
        symbol=symbol,
        status=status,
        confidence=confidence,
        compared_source_count=len(sources),
        matched_source_count=len(sources) if not material_diff else 0,
        missing_source_count=0,
        material_difference_count=1 if material_diff else 0,
        metrics=comp,
        disagreement_score=comp.get("close_diff_pct"),
        confidence_score=90.0 if not material_diff else 30.0,
        source_rank_hints=[{"provider": n, "rank": 1} for n in names],
        outlier_sources=[names[1]] if material_diff else [],
        drift_warnings=["Potential drift detected"] if material_diff else [],
        schema_valid=True,
        dry_run_only=True,
        network_used=False, paid_api_used=False, scraping_used=False, html_parsing_used=False,
        broker_used=False, order_created=False, paper_state_mutated=False,
        risk_flags=risk_flags, warnings=[], errors=[], metadata={}
    )

def _build_failed_comparison(symbol: str, error: str) -> SourceComparisonResult:
     return SourceComparisonResult(
        result_id=create_source_comparison_result_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        comparison_id=None, symbol=symbol,
        status=SourceComparisonStatus.FAILED, confidence=SourceConfidenceLevel.UNKNOWN,
        compared_source_count=0, matched_source_count=0, missing_source_count=0, material_difference_count=0,
        metrics={}, disagreement_score=None, confidence_score=None, source_rank_hints=[],
        outlier_sources=[], drift_warnings=[], schema_valid=False, dry_run_only=True,
        network_used=False, paid_api_used=False, scraping_used=False, html_parsing_used=False,
        broker_used=False, order_created=False, paper_state_mutated=False,
        risk_flags=[], warnings=[], errors=[error], metadata={}
    )

def source_comparison_summary(result: SourceComparisonResult) -> dict[str, Any]:
    return {"status": result.status.value, "confidence": result.confidence.value}

def source_comparison_to_text(result: SourceComparisonResult, limit: int = 200) -> str:
    return f"Comparison {result.result_id} for {result.symbol} - Status: {result.status.value}"
