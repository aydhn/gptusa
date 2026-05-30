from typing import Any, Dict
from usa_signal_bot.regime_classification.freeze_preparation.phase134_models import (
    RegimeMonitoringIngestionResult,
    MonitoringValidationRule,
    MonitoringValidationResult,
    DriftReportSection,
    DriftReportDocument,
    DriftReportQaRuleResult,
    ResearchFreezeArtifactReference,
    ResearchFreezePackage,
    ResearchFreezeReadinessGate,
    RegimeResearchFreezeContext,
    RegimeResearchFreezeFullReview
)
from usa_signal_bot.regime_classification.freeze_preparation.regime_monitoring_ingestion import regime_monitoring_ingestion_to_text
from usa_signal_bot.regime_classification.freeze_preparation.monitoring_validation_runner import monitoring_validation_to_text
from usa_signal_bot.regime_classification.freeze_preparation.drift_report_builder import drift_report_document_to_text
from usa_signal_bot.regime_classification.freeze_preparation.drift_report_qa_validator import drift_report_qa_to_text
from usa_signal_bot.regime_classification.freeze_preparation.research_freeze_package_builder import research_freeze_package_to_text
from usa_signal_bot.regime_classification.freeze_preparation.research_freeze_readiness_gate import research_freeze_readiness_gate_to_text
from usa_signal_bot.regime_classification.freeze_preparation.research_freeze_report import regime_research_freeze_full_review_to_text, regime_research_freeze_limitations_text

def regime_monitoring_ingestion_result_to_text(item: RegimeMonitoringIngestionResult) -> str:
    return regime_monitoring_ingestion_to_text(item)

def monitoring_validation_rule_to_text(item: MonitoringValidationRule) -> str:
    return f"Rule {item.name}: Passed={item.passed}"

def monitoring_validation_result_to_text(item: MonitoringValidationResult, limit: int = 300) -> str:
    return monitoring_validation_to_text(item, limit)

def drift_report_section_to_text(item: DriftReportSection, limit: int = 200) -> str:
    return f"Section {item.title}: {item.body[:50]}..."[:limit]

def drift_report_document_to_text_alias(item: DriftReportDocument, limit: int = 300) -> str:
    return drift_report_document_to_text(item, limit)

def drift_report_qa_result_to_text(item: DriftReportQaRuleResult) -> str:
    return f"QA Rule {item.rule_name}: Passed={item.passed}"

def research_freeze_artifact_reference_to_text(item: ResearchFreezeArtifactReference) -> str:
    return f"Artifact {item.artifact_name}: Available={item.available}"

def research_freeze_package_to_text_alias(item: ResearchFreezePackage, limit: int = 300) -> str:
    return research_freeze_package_to_text(item, limit)

def research_freeze_readiness_gate_to_text_alias(item: ResearchFreezeReadinessGate, limit: int = 300) -> str:
    return research_freeze_readiness_gate_to_text(item, limit)

def regime_research_freeze_context_to_text(item: RegimeResearchFreezeContext, limit: int = 300) -> str:
    return f"Context {item.context_id} - Ready: {item.ready_for_phase135}"[:limit]

def regime_research_freeze_full_review_to_text_alias(item: RegimeResearchFreezeFullReview, limit: int = 300) -> str:
    return regime_research_freeze_full_review_to_text(item, limit)

def research_freeze_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Store Summary: {summary}"
