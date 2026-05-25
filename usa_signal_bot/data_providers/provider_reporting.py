
from typing import Any

def provider_kickoff_gate_ingestion_result_to_text(item: Any) -> str: return str(item)
def provider_adapter_spec_to_text(item: Any) -> str: return str(item)
def provider_registry_entry_to_text(item: Any) -> str: return str(item)
def provider_capability_matrix_to_text(item: Any, limit: int = 200) -> str: return str(item)[:limit]
def provider_safety_policy_to_text(item: Any) -> str: return str(item)
def provider_selection_request_to_text(item: Any) -> str: return str(item)
def provider_selection_result_to_text(item: Any) -> str: return str(item)
def provider_fallback_plan_to_text(item: Any) -> str: return str(item)
def provider_abstraction_context_to_text(item: Any, limit: int = 300) -> str: return str(item)[:limit]
def provider_abstraction_full_review_to_text(item: Any, limit: int = 300) -> str: return str(item)[:limit]
def provider_store_summary_to_text(summary: dict[str, Any]) -> str: return str(summary)
def provider_abstraction_limitations_text() -> str: return "Phase 106 limits apply."
