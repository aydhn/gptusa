from typing import Any, Dict
from usa_signal_bot.universe_lifecycle.lifecycle_models import (
    SymbolLifecycleRecord, SymbolAliasRecord, UniverseSnapshot,
    SymbolHistoryCheck, SurvivorshipBiasAssessment, UniverseLifecycleReviewResult
)

def symbol_lifecycle_record_to_text(record: SymbolLifecycleRecord) -> str:
    delist = f" (Delisted: {record.delisted_date})" if record.delisted_date else ""
    return f"{record.symbol}: {record.status.value}{delist} [Source: {record.source.value}]"

def symbol_alias_record_to_text(record: SymbolAliasRecord) -> str:
    eff = f" [Eff: {record.effective_date}]" if record.effective_date else ""
    return f"{record.old_symbol} -> {record.new_symbol} ({record.alias_type.value}){eff}"

def survivorship_bias_assessment_to_text(assessment: SurvivorshipBiasAssessment) -> str:
    lines = [
        f"Survivorship Bias Assessment: {assessment.universe_name} [{assessment.status.value}]",
        f"Risk Level: {assessment.risk.value}",
        f"Current Symbols: {assessment.current_symbol_count}",
        f"Inactive/Delisted/Unknown: {assessment.inactive_symbol_count} / {assessment.delisted_symbol_count} / {assessment.unknown_status_count}"
    ]
    if assessment.warnings:
        lines.append("Warnings:")
        for w in assessment.warnings:
            lines.append(f"  - {w}")
    return "\n".join(lines)

def universe_lifecycle_review_result_to_text(result: UniverseLifecycleReviewResult, limit: int = 100) -> str:
    lines = [
        f"Universe Lifecycle Review: {result.universe_name} ({result.report_type.value})",
        f"Date: {result.created_at_utc}"
    ]
    if result.survivorship_assessment:
        lines.append("\n" + survivorship_bias_assessment_to_text(result.survivorship_assessment))
    return "\n".join(lines)

def lifecycle_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Lifecycle Store Summary: {summary.get('snapshots', 0)} snapshots, {summary.get('reviews', 0)} reviews."

def lifecycle_limitations_text() -> str:
    return (
        "LIFECYCLE MANAGEMENT LIMITATIONS:\n"
        "1. This is a local system using manual registries or inferred metadata. It is NOT an official stock exchange delisting database.\n"
        "2. Survivorship-bias guards generate operational research warnings, NOT financial investment advice.\n"
        "3. Missing history or 'inactive' status is an evidence-based flag, not a definitive legal corporate action proof.\n"
        "4. A 'CLEAR' or 'PASS' guard status does NOT constitute approval for live trading or real broker execution.\n"
        "5. The system performs no live web-scraping or live API calls for this verification."
    )
