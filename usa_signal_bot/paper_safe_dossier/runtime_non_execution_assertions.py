from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_safe_dossier.paper_safe_dossier_models import PrePaperLocalRuntimeMap, NonExecutionAcceptanceSeal
from usa_signal_bot.core.enums import PaperSafeDossierRiskFlag

def required_runtime_non_execution_assertions() -> List[str]:
    return [
        "no_broker_execution",
        "no_active_paper_enable",
        "no_paper_admission",
        "no_order_creation",
        "no_paper_state_write",
        "no_config_patch",
        "no_telegram_real_send",
        "metadata_only_runtime_map",
        "read_only_boundary_preserved"
    ]

def check_runtime_non_execution_assertions(runtime_map: Optional[PrePaperLocalRuntimeMap] = None, seal: Optional[NonExecutionAcceptanceSeal] = None) -> Dict[str, bool]:
    results = {
        "no_broker_execution": False,
        "no_active_paper_enable": False,
        "no_paper_admission": False,
        "no_order_creation": False,
        "no_paper_state_write": False,
        "no_config_patch": False,
        "no_telegram_real_send": False,
        "metadata_only_runtime_map": False,
        "read_only_boundary_preserved": False
    }

    if seal:
        results["no_broker_execution"] = seal.no_broker_confirmed
        results["no_active_paper_enable"] = seal.no_active_paper_confirmed
        results["no_paper_admission"] = seal.no_paper_admission_confirmed
        results["no_order_creation"] = seal.no_order_confirmed
        results["no_paper_state_write"] = seal.no_write_confirmed
        results["no_config_patch"] = seal.no_config_patch_confirmed
        results["no_telegram_real_send"] = seal.no_telegram_real_send_confirmed

    if runtime_map:
        results["metadata_only_runtime_map"] = runtime_map.map_is_metadata_only
        results["read_only_boundary_preserved"] = runtime_map.read_only_boundary_confirmed
        # fallback to map if seal not provided or false
        if not results["no_broker_execution"]: results["no_broker_execution"] = runtime_map.all_broker_routes_denied
        if not results["no_active_paper_enable"]: results["no_active_paper_enable"] = runtime_map.all_activation_routes_denied
        if not results["no_paper_admission"]: results["no_paper_admission"] = runtime_map.all_paper_admission_routes_denied
        if not results["no_order_creation"]: results["no_order_creation"] = runtime_map.all_order_routes_denied
        if not results["no_paper_state_write"]: results["no_paper_state_write"] = runtime_map.all_write_routes_denied
        if not results["no_config_patch"]: results["no_config_patch"] = runtime_map.all_config_patch_routes_denied
        if not results["no_telegram_real_send"]: results["no_telegram_real_send"] = runtime_map.all_telegram_real_send_routes_denied

    return results

def failed_runtime_non_execution_assertions(results: Dict[str, bool]) -> List[str]:
    return [k for k, v in results.items() if not v]

def runtime_non_execution_assertion_flags(results: Dict[str, bool]) -> List[PaperSafeDossierRiskFlag]:
    flags = []
    if not results.get("no_broker_execution", False): flags.append(PaperSafeDossierRiskFlag.BROKER_ORDER_RISK)
    if not results.get("no_active_paper_enable", False): flags.append(PaperSafeDossierRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
    if not results.get("no_paper_admission", False): flags.append(PaperSafeDossierRiskFlag.PAPER_ADMISSION_RISK)
    if not results.get("no_order_creation", False): flags.append(PaperSafeDossierRiskFlag.ORDER_CREATED_RISK)
    if not results.get("no_paper_state_write", False): flags.append(PaperSafeDossierRiskFlag.PAPER_STATE_MUTATION_RISK)
    if not results.get("no_config_patch", False): flags.append(PaperSafeDossierRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)
    if not results.get("no_telegram_real_send", False): flags.append(PaperSafeDossierRiskFlag.TELEGRAM_REAL_SEND_RISK)
    if not results.get("metadata_only_runtime_map", False): flags.append(PaperSafeDossierRiskFlag.RUNTIME_MAP_INVALID)
    if not results.get("read_only_boundary_preserved", False): flags.append(PaperSafeDossierRiskFlag.RUNTIME_ROUTE_PERMISSION_RISK)
    return flags

def runtime_non_execution_assertions_summary(results: Dict[str, bool]) -> Dict[str, Any]:
    failed = failed_runtime_non_execution_assertions(results)
    return {
        "all_passed": len(failed) == 0,
        "failed_count": len(failed),
        "passed_count": len(results) - len(failed)
    }

def runtime_non_execution_assertions_to_text(results: Dict[str, bool]) -> str:
    summary = runtime_non_execution_assertions_summary(results)
    lines = [f"All Assertions Passed: {summary['all_passed']}"]
    lines.append(f"Passed: {summary['passed_count']} | Failed: {summary['failed_count']}")
    if summary['failed_count'] > 0:
         failed = failed_runtime_non_execution_assertions(results)
         lines.append(f"Failed Assertions: {', '.join(failed)}")
    return "\n".join(lines)
