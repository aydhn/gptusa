from typing import Any, Dict

from usa_signal_bot.regime_classification.diagnostics.regime_labeling_ingestion import regime_labeling_ingestion_to_text
from usa_signal_bot.regime_classification.diagnostics.regime_transition_matrix import transition_matrix_to_text
from usa_signal_bot.regime_classification.diagnostics.regime_persistence_analytics import persistence_analytics_to_text
from usa_signal_bot.regime_classification.diagnostics.regime_duration_analytics import duration_analytics_to_text
from usa_signal_bot.regime_classification.diagnostics.regime_churn_diagnostics import churn_diagnostics_to_text
from usa_signal_bot.regime_classification.diagnostics.regime_stability_diagnostics import stability_diagnostics_to_text
from usa_signal_bot.regime_classification.diagnostics.regime_diagnostics_readiness_gate import regime_diagnostics_readiness_gate_to_text
from usa_signal_bot.regime_classification.diagnostics.regime_transition_report import regime_transition_limitations_text

def regime_labeling_ingestion_result_to_text(item: Any) -> str:
    return regime_labeling_ingestion_to_text(item)

def regime_transition_matrix_to_text_fmt(item: Any, limit: int = 300) -> str:
    return transition_matrix_to_text([item], limit)

def regime_persistence_profile_to_text(item: Any) -> str:
    return persistence_analytics_to_text([item], 1)

def regime_duration_profile_to_text(item: Any) -> str:
    return duration_analytics_to_text([item], 1)

def regime_churn_diagnostic_to_text(item: Any) -> str:
    return churn_diagnostics_to_text([item], 1)

def regime_stability_diagnostic_to_text(item: Any) -> str:
    return stability_diagnostics_to_text([item], 1)

def regime_transition_analytics_result_to_text(item: Any, limit: int = 300) -> str:
    return f"Analytics Result [{item.analytics_id}]: {item.matrix_count} matrices."

def regime_transition_context_to_text(item: Any, limit: int = 300) -> str:
    return f"Transition Context [{item.context_id}]: Ready={item.ready_for_phase130}"

def regime_transition_full_review_to_text(item: Any, limit: int = 300) -> str:
    from usa_signal_bot.regime_classification.diagnostics.regime_transition_report import regime_transition_full_review_to_text as inner
    return inner(item, limit)

def regime_transition_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Store summary: {summary}"
