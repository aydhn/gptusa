from typing import Any
from usa_signal_bot.provider_orchestration.phase110_models import *

def provider_quality_ingestion_result_to_text(item: ProviderQualityIngestionResult) -> str:
    return f"Ingestion ID: {item.ingestion_id}, Valid: {item.valid_for_phase110}"

def orchestrated_data_request_to_text(item: OrchestratedDataRequest) -> str:
    return f"Request ID: {item.request_id}, Symbol: {item.symbol}"

def provider_route_plan_to_text(item: ProviderRoutePlan) -> str:
    return f"Plan ID: {item.route_plan_id}, Symbol: {item.symbol}, Status: {item.route_status.value}"

def provider_route_result_to_text(item: ProviderRouteResult) -> str:
    return f"Result ID: {item.route_result_id}, Provider: {item.selected_provider}, Status: {item.route_status.value}"

def source_blend_input_to_text(item: SourceBlendInput) -> str:
    return f"Blend Input ID: {item.blend_input_id}, Symbol: {item.symbol}"

def source_blend_result_to_text(item: SourceBlendResult) -> str:
    return f"Blend Result ID: {item.blend_result_id}, Status: {item.status.value}"

def data_availability_item_to_text(item: DataAvailabilityItem) -> str:
    return f"Symbol: {item.symbol}, Status: {item.status.value}"

def data_availability_report_to_text(item: DataAvailabilityReport, limit: int = 200) -> str:
    return f"Coverage Ratio: {item.coverage_ratio:.2f}, Missing: {item.missing_count}"

def refresh_plan_item_to_text(item: RefreshPlanItem) -> str:
    return f"Symbol: {item.symbol}, Priority: {item.priority.value}"

def refresh_plan_report_to_text(item: RefreshPlanReport, limit: int = 200) -> str:
    return f"Requires Refresh: {item.refresh_required_count}, High Priority: {item.high_priority_count}"

def provider_orchestration_context_to_text(item: ProviderOrchestrationContext, limit: int = 300) -> str:
    return f"Context ID: {item.context_id}, Status: {item.status.value}, Routes: {len(item.route_plans)}"

def provider_orchestration_full_review_to_text(item: ProviderOrchestrationFullReview, limit: int = 300) -> str:
    return f"Review ID: {item.review_id}, Type: {item.report_type.value}"

def provider_orchestration_store_summary_to_text(summary: dict[str, Any]) -> str:
    return "\n".join([f"{k}: {v}" for k, v in summary.items()])

def provider_orchestration_limitations_text() -> str:
    return "Phase 110 is NOT activation. NO broker, NO paper mutation, NO network, NO Telegram."
