from typing import Any
from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import (
    RegimeTransitionIngestionResult, MarketBehaviorProfileSpec, MarketBehaviorProfile,
    RegimeBehaviorSummary, RegimeDiagnosticsInterpretation, BehaviorReportSection,
    BehaviorReportDocument, BehaviorReportQaRuleResult, MarketBehaviorReadinessGate,
    MarketBehaviorContext, MarketBehaviorFullReview
)

def regime_transition_ingestion_result_to_text(item: RegimeTransitionIngestionResult) -> str:
    return f"Ingestion {item.ingestion_id} - valid={item.valid_for_phase130}"

def market_behavior_profile_spec_to_text(item: MarketBehaviorProfileSpec) -> str:
    return f"Spec {item.profile_name}"

def market_behavior_profile_to_text(item: MarketBehaviorProfile) -> str:
    return f"Profile {item.profile_id} ({item.profile_name})"

def regime_behavior_summary_to_text(item: RegimeBehaviorSummary) -> str:
    return f"Summary {item.summary_id} ({item.title})"

def regime_diagnostics_interpretation_to_text(item: RegimeDiagnosticsInterpretation) -> str:
    return f"Interpretation {item.interpretation_id} ({item.interpretation_name})"

def behavior_report_section_to_text(item: BehaviorReportSection, limit: int = 200) -> str:
    return f"Section {item.title}"

def behavior_report_document_to_text(item: BehaviorReportDocument, limit: int = 300) -> str:
    return f"Report {item.document_id} ({len(item.sections)} sections)"

def behavior_report_qa_result_to_text(item: BehaviorReportQaRuleResult) -> str:
    return f"QA {item.rule_name} - pass={item.passed}"

def market_behavior_readiness_gate_to_text(item: MarketBehaviorReadinessGate, limit: int = 300) -> str:
    return f"Gate {item.gate_id} - ready={item.ready_for_phase131}"

def market_behavior_context_to_text(item: MarketBehaviorContext, limit: int = 300) -> str:
    return f"Context {item.context_id}"

def market_behavior_full_review_to_text(item: MarketBehaviorFullReview, limit: int = 300) -> str:
    return f"Review {item.review_id}"

def market_behavior_store_summary_to_text(summary: dict[str, Any]) -> str:
    return f"Store Summary: {summary}"

def market_behavior_limitations_text() -> str:
    return "Phase 130 is a reporting layer and does not generate trade signals or perform deployment."
