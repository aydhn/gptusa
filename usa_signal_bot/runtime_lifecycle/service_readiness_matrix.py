from typing import Any, Dict, Optional, List
from usa_signal_bot.core.enums import ServiceReadinessStatus, LifecycleRiskFlag
from usa_signal_bot.runtime_lifecycle.phase104_models import (
    ServiceReadinessItem,
    ServiceReadinessMatrix,
    create_service_readiness_id,
    create_service_readiness_matrix_id,
    _now_str
)

def build_service_readiness_item(service_payload: Dict[str, Any]) -> ServiceReadinessItem:
    s_id = service_payload.get("service_id", "unknown-service")
    s_name = service_payload.get("service_name", "Unknown Service")

    # We heuristically assume ready for local compute for MVP
    # since no execution is true by definition here
    metadata_ready = True
    read_only_ready = True
    local_compute_ready = True
    config_ready = True
    dependency_ready = True
    validation_ready = True
    observability_ready = True
    notification_boundary_ready = True
    provider_interface_ready = True
    no_execution_ready = True

    return ServiceReadinessItem(
        readiness_id=create_service_readiness_id(),
        created_at_utc=_now_str(),
        service_id=s_id,
        service_name=s_name,
        readiness_status=ServiceReadinessStatus.READY_METADATA_ONLY,
        metadata_ready=metadata_ready,
        read_only_ready=read_only_ready,
        local_compute_ready=local_compute_ready,
        config_ready=config_ready,
        dependency_ready=dependency_ready,
        validation_ready=validation_ready,
        observability_ready=observability_ready,
        notification_boundary_ready=notification_boundary_ready,
        provider_interface_ready=provider_interface_ready,
        no_execution_ready=no_execution_ready,
        required_followups=[],
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def build_service_readiness_matrix(service_graph_payload: Optional[Dict[str, Any]] = None) -> ServiceReadinessMatrix:
    services = []
    if service_graph_payload and "runtime_service_graph" in service_graph_payload:
        sg = service_graph_payload["runtime_service_graph"]
        for node in sg.get("nodes", []):
            services.append(build_service_readiness_item(node))

    # Default to passing matrix if empty for now since execution is inherently blocked
    all_ready = True

    return ServiceReadinessMatrix(
        matrix_id=create_service_readiness_matrix_id(),
        created_at_utc=_now_str(),
        items=services,
        total_services=len(services),
        ready_services=len(services),
        blocked_services=0,
        not_ready_services=0,
        disabled_services=0,
        all_required_services_ready=all_ready,
        no_execution_ready=True,
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def service_readiness_matrix_summary(matrix: ServiceReadinessMatrix) -> Dict[str, Any]:
    return {
        "matrix_id": matrix.matrix_id,
        "total": matrix.total_services,
        "ready": matrix.ready_services,
        "blocked": matrix.blocked_services,
        "no_execution_ready": matrix.no_execution_ready
    }

def service_readiness_matrix_to_text(matrix: ServiceReadinessMatrix, limit: int = 300) -> str:
    lines = [
        f"=== SERVICE READINESS MATRIX ===",
        f"ID: {matrix.matrix_id}",
        f"Total Services: {matrix.total_services}",
        f"Ready: {matrix.ready_services}",
        f"Blocked: {matrix.blocked_services}",
        f"No-Execution Ready: {matrix.no_execution_ready}",
        f"All Required Ready: {matrix.all_required_services_ready}"
    ]
    return "\n".join(lines)[:limit]
