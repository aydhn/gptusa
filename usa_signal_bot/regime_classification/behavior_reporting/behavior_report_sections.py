from typing import Any
from usa_signal_bot.core.enums import BehaviorReportSectionKind
from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import (
    BehaviorReportSection, MarketBehaviorProfile, RegimeBehaviorSummary,
    RegimeTransitionIngestionResult, RegimeDiagnosticsInterpretation
)

def _build_generic_section(kind: BehaviorReportSectionKind, title: str) -> BehaviorReportSection:
    sec = BehaviorReportSection()
    sec.section_kind = kind
    sec.title = title
    return sec

def build_behavior_executive_summary_section(profiles: list[MarketBehaviorProfile], summaries: list[RegimeBehaviorSummary]) -> BehaviorReportSection:
    sec = _build_generic_section(BehaviorReportSectionKind.EXECUTIVE_SUMMARY, "Executive Summary")
    sec.body = "This report summarizes regime behaviors."
    return sec

def build_behavior_data_scope_section(ingestion: RegimeTransitionIngestionResult) -> BehaviorReportSection:
    sec = _build_generic_section(BehaviorReportSectionKind.DATA_SCOPE, "Data Scope")
    sec.body = f"Data scope ingested: {ingestion.ingestion_id}"
    return sec

def build_transition_matrix_summary_section(summaries: list[RegimeBehaviorSummary]) -> BehaviorReportSection:
    sec = _build_generic_section(BehaviorReportSectionKind.TRANSITION_MATRIX_SUMMARY, "Transition Matrix Summary")
    sec.body = "Summary of transitions."
    return sec

def build_persistence_summary_section(summaries: list[RegimeBehaviorSummary]) -> BehaviorReportSection:
    sec = _build_generic_section(BehaviorReportSectionKind.PERSISTENCE_SUMMARY, "Persistence Summary")
    sec.body = "Summary of persistence."
    return sec

def build_duration_churn_summary_section(summaries: list[RegimeBehaviorSummary]) -> BehaviorReportSection:
    sec = _build_generic_section(BehaviorReportSectionKind.DURATION_CHURN_SUMMARY, "Duration/Churn Summary")
    sec.body = "Summary of churn and duration."
    return sec

def build_stability_summary_section(summaries: list[RegimeBehaviorSummary]) -> BehaviorReportSection:
    sec = _build_generic_section(BehaviorReportSectionKind.STABILITY_SUMMARY, "Stability Summary")
    sec.body = "Summary of stability."
    return sec

def build_market_behavior_profiles_section(profiles: list[MarketBehaviorProfile]) -> BehaviorReportSection:
    sec = _build_generic_section(BehaviorReportSectionKind.MARKET_BEHAVIOR_PROFILES, "Market Behavior Profiles")
    sec.body = f"Generated {len(profiles)} profiles."
    return sec

def build_cross_symbol_behavior_section(profiles: list[MarketBehaviorProfile]) -> BehaviorReportSection:
    sec = _build_generic_section(BehaviorReportSectionKind.CROSS_SYMBOL_BEHAVIOR, "Cross-Symbol Behavior")
    sec.body = "Cross-symbol metrics."
    return sec

def build_diagnostic_interpretation_section(items: list[RegimeDiagnosticsInterpretation]) -> BehaviorReportSection:
    sec = _build_generic_section(BehaviorReportSectionKind.DIAGNOSTIC_INTERPRETATION, "Diagnostic Interpretation")
    sec.body = f"Generated {len(items)} interpretations."
    return sec

def build_behavior_limitations_section() -> BehaviorReportSection:
    sec = _build_generic_section(BehaviorReportSectionKind.LIMITATIONS, "Limitations")
    sec.body = "This report is for research purposes only. It is not investment advice."
    return sec

def build_behavior_safety_boundary_section() -> BehaviorReportSection:
    sec = _build_generic_section(BehaviorReportSectionKind.SAFETY_BOUNDARY, "Safety Boundary")
    sec.body = "No execution, orders, or live trading."
    return sec

def validate_behavior_report_sections(sections: list[BehaviorReportSection]) -> list[str]:
    return []
