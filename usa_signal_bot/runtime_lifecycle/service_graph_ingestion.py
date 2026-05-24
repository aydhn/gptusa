from typing import Any, Dict, Optional, Tuple
from pathlib import Path
import json

from usa_signal_bot.runtime_lifecycle.phase104_models import (
    ServiceGraphIngestionResult,
    create_service_graph_ingestion_id,
    _now_str
)
from usa_signal_bot.core.enums import LifecycleRiskFlag

def _get_bool(payload: dict, key: str, default: bool = False) -> bool:
    return bool(payload.get(key, default))

def extract_runtime_service_graph(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("runtime_service_graph")

def extract_orchestration_dry_run_result(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("orchestration_dry_run_result")

def service_graph_supports_phase104(payload: Dict[str, Any]) -> Tuple[bool, list[str]]:
    warnings = []

    if "runtime_service_graph" not in payload:
        return False, ["Missing runtime_service_graph in payload"]

    graph = payload["runtime_service_graph"]
    valid = _get_bool(graph, "is_valid")
    has_cycles = _get_bool(graph, "has_cycles")

    if not valid:
        warnings.append("Service graph is not marked valid")
    if has_cycles:
        warnings.append("Service graph has cycles")

    dry_run = payload.get("orchestration_dry_run_result", {})
    if not _get_bool(dry_run, "success"):
        warnings.append("Orchestration dry run was not successful")

    return (valid and not has_cycles), warnings

def ingest_service_graph_review_payload(payload: Dict[str, Any]) -> ServiceGraphIngestionResult:
    is_supported, support_warnings = service_graph_supports_phase104(payload)

    graph = payload.get("runtime_service_graph", {})
    dry_run = payload.get("orchestration_dry_run_result", {})

    risk_flags = []
    errors = []

    graph_valid = _get_bool(graph, "is_valid")
    has_cycles = _get_bool(graph, "has_cycles")
    missing_deps = int(graph.get("missing_dependency_count", 0))
    invalid_contracts = int(graph.get("invalid_contract_count", 0))
    blocked_routes = int(graph.get("blocked_route_count", 0))
    dry_run_passed = _get_bool(dry_run, "success")

    if not graph_valid:
        risk_flags.append(LifecycleRiskFlag.SERVICE_GRAPH_INVALID)
        errors.append("Service graph is marked as invalid")
    if has_cycles:
        risk_flags.append(LifecycleRiskFlag.SERVICE_GRAPH_INVALID)
        errors.append("Service graph has cyclic dependencies")
    if missing_deps > 0:
        errors.append(f"Service graph has {missing_deps} missing dependencies")
    if invalid_contracts > 0:
        errors.append(f"Service graph has {invalid_contracts} invalid contracts")
    if blocked_routes > 0:
        errors.append(f"Service graph has {blocked_routes} blocked routes")
    if not dry_run_passed:
        risk_flags.append(LifecycleRiskFlag.SERVICE_GRAPH_INVALID)
        errors.append("Dry run validation did not pass")

    # Phase 103 results must not contain real execution
    execution_performed = _get_bool(payload, "execution_performed")
    network_used = _get_bool(payload, "network_used")
    broker_used = _get_bool(payload, "broker_used")
    order_created = _get_bool(payload, "order_created")
    paper_state_mutated = _get_bool(payload, "paper_state_mutated")
    telegram_real_sent = _get_bool(payload, "telegram_real_sent")
    scraping_used = _get_bool(payload, "scraping_used")
    dashboard_started = _get_bool(payload, "dashboard_started")

    if execution_performed:
        risk_flags.append(LifecycleRiskFlag.EXECUTION_ROUTE_RISK)
    if broker_used:
        risk_flags.append(LifecycleRiskFlag.BROKER_ROUTE_RISK)
    if order_created:
        risk_flags.append(LifecycleRiskFlag.ORDER_ROUTE_RISK)
    if paper_state_mutated:
        risk_flags.append(LifecycleRiskFlag.PAPER_MUTATION_RISK)
    if telegram_real_sent:
        risk_flags.append(LifecycleRiskFlag.TELEGRAM_REAL_SEND_RISK)
    if scraping_used:
        risk_flags.append(LifecycleRiskFlag.SCRAPING_RISK)
    if dashboard_started:
        risk_flags.append(LifecycleRiskFlag.DASHBOARD_RISK)
    if network_used:
        risk_flags.append(LifecycleRiskFlag.PROVIDER_NETWORK_FETCH_RISK)

    valid_for_phase104 = (
        is_supported and
        len(errors) == 0 and
        not execution_performed and
        not broker_used and
        not order_created and
        not paper_state_mutated and
        not telegram_real_sent and
        not scraping_used and
        not dashboard_started
    )

    return ServiceGraphIngestionResult(
        ingestion_id=create_service_graph_ingestion_id(),
        created_at_utc=_now_str(),
        source_path=payload.get("source_path"),
        source_review_id=payload.get("review_id"),
        source_graph_id=graph.get("graph_id"),
        available=True,
        service_graph_valid=graph_valid,
        dry_run_passed=dry_run_passed,
        graph_has_cycles=has_cycles,
        missing_dependency_count=missing_deps,
        invalid_contract_count=invalid_contracts,
        blocked_route_count=blocked_routes,
        execution_performed=execution_performed,
        network_used=network_used,
        broker_used=broker_used,
        order_created=order_created,
        paper_state_mutated=paper_state_mutated,
        telegram_real_sent=telegram_real_sent,
        scraping_used=scraping_used,
        dashboard_started=dashboard_started,
        valid_for_phase104=valid_for_phase104,
        risk_flags=risk_flags,
        warnings=support_warnings,
        errors=errors,
        metadata={"payload_keys": list(payload.keys())}
    )

def ingest_latest_service_graph_review_from_store(data_root: Path) -> ServiceGraphIngestionResult:
    reviews_dir = data_root / "service_graph" / "reviews"
    if not reviews_dir.exists():
        return _empty_ingestion_result("Reviews directory not found")

    files = sorted(reviews_dir.glob("*.json"), reverse=True)
    if not files:
        return _empty_ingestion_result("No service graph reviews found")

    try:
        with open(files[0], "r", encoding="utf-8") as f:
            payload = json.load(f)
            payload["source_path"] = str(files[0])
            return ingest_service_graph_review_payload(payload)
    except Exception as e:
        return _empty_ingestion_result(f"Error loading review: {str(e)}")

def _empty_ingestion_result(error_msg: str) -> ServiceGraphIngestionResult:
    return ServiceGraphIngestionResult(
        ingestion_id=create_service_graph_ingestion_id(),
        created_at_utc=_now_str(),
        source_path=None,
        source_review_id=None,
        source_graph_id=None,
        available=False,
        service_graph_valid=False,
        dry_run_passed=False,
        graph_has_cycles=False,
        missing_dependency_count=0,
        invalid_contract_count=0,
        blocked_route_count=0,
        execution_performed=False,
        network_used=False,
        broker_used=False,
        order_created=False,
        paper_state_mutated=False,
        telegram_real_sent=False,
        scraping_used=False,
        dashboard_started=False,
        valid_for_phase104=False,
        risk_flags=[LifecycleRiskFlag.SERVICE_GRAPH_MISSING],
        warnings=[],
        errors=[error_msg],
        metadata={}
    )

def service_graph_ingestion_to_text(result: ServiceGraphIngestionResult) -> str:
    lines = [
        f"=== SERVICE GRAPH INGESTION ===",
        f"ID: {result.ingestion_id}",
        f"Available: {result.available}",
        f"Valid for Phase 104: {result.valid_for_phase104}",
        f"Graph Valid: {result.service_graph_valid} | Dry-Run Passed: {result.dry_run_passed}"
    ]
    if result.errors:
        lines.append("Errors:")
        for e in result.errors:
            lines.append(f" - {e}")
    if result.risk_flags:
        lines.append(f"Risk Flags: {[f.value for f in result.risk_flags]}")
    return "\n".join(lines)
