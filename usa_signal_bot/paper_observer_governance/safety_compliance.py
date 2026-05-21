from typing import Any
from usa_signal_bot.core.enums import ObserverGovernanceRiskFlag

def calculate_observer_safety_compliance(observer_payload: dict[str, Any], paper_snapshot: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "locked_runtime": check_locked_runtime_compliance(observer_payload),
        "non_execution": check_non_execution_compliance(observer_payload),
        "paper_snapshot_read_only": check_paper_snapshot_read_only_compliance(paper_snapshot or {})
    }

def check_locked_runtime_compliance(observer_payload: dict[str, Any]) -> dict[str, Any]:
    locked = observer_payload.get("locked_runtime", False)
    return {"status": "PASS" if locked else "FAIL"}

def check_non_execution_compliance(observer_payload: dict[str, Any]) -> dict[str, Any]:
    flags = []
    if observer_payload.get("active_paper_permission", False): flags.append("active_paper_permission")
    if observer_payload.get("paper_mutation", False): flags.append("paper_mutation")
    if observer_payload.get("broker_send", False): flags.append("broker_send")
    if observer_payload.get("telegram_real_send", False): flags.append("telegram_real_send")
    if observer_payload.get("config_patch", False): flags.append("config_patch")
    return {"status": "FAIL" if flags else "PASS", "violations": flags}

def check_paper_snapshot_read_only_compliance(paper_snapshot: dict[str, Any]) -> dict[str, Any]:
    flags = []
    if paper_snapshot.get("paper_state_committed", False): flags.append("paper_state_committed")
    if paper_snapshot.get("paper_order_executed", False): flags.append("paper_order_executed")
    return {"status": "FAIL" if flags else "PASS", "violations": flags}

def safety_compliance_risk_flags(payload: dict[str, Any]) -> list[ObserverGovernanceRiskFlag]:
    flags = []
    if payload.get("locked_runtime", {}).get("status") == "FAIL":
        flags.append(ObserverGovernanceRiskFlag.LOCKED_RUNTIME_NOT_CONFIRMED)
    viol = payload.get("non_execution", {}).get("violations", [])
    if "active_paper_permission" in viol: flags.append(ObserverGovernanceRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
    if "paper_mutation" in viol: flags.append(ObserverGovernanceRiskFlag.PAPER_STATE_MUTATION_RISK)
    if "broker_send" in viol: flags.append(ObserverGovernanceRiskFlag.BROKER_ORDER_RISK)
    if "telegram_real_send" in viol: flags.append(ObserverGovernanceRiskFlag.TELEGRAM_REAL_SEND_RISK)
    if "config_patch" in viol: flags.append(ObserverGovernanceRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)

    viol_paper = payload.get("paper_snapshot_read_only", {}).get("violations", [])
    if viol_paper: flags.append(ObserverGovernanceRiskFlag.PAPER_STATE_MUTATION_RISK)
    return flags

def safety_compliance_to_text(payload: dict[str, Any]) -> str:
    return str(payload)
