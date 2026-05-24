from typing import List, Dict, Any, Optional
from usa_signal_bot.runtime_lifecycle.phase104_models import (
    StartupCheckReport,
    ServiceReadinessMatrix,
    ReadinessGate
)
from usa_signal_bot.core.enums import LifecycleRiskFlag

def validate_no_execution_readiness(
    startup_report: Optional[StartupCheckReport] = None,
    readiness_matrix: Optional[ServiceReadinessMatrix] = None,
    gate: Optional[ReadinessGate] = None
) -> List[str]:
    errors = []

    if startup_report:
        if startup_report.execution_performed:
            errors.append("Startup report implies execution performed")
        if startup_report.network_used:
            errors.append("Startup report implies network used")

    if gate:
        if gate.activation_allowed or gate.active_paper_enabled:
            errors.append("Gate allows active paper or activation")
        if gate.execution_performed or gate.order_created:
            errors.append("Gate implies execution or order creation")

    if readiness_matrix and not readiness_matrix.no_execution_ready:
        errors.append("Matrix indicates execution risk")

    return errors

def collect_no_execution_risk_flags(
    startup_report: Optional[StartupCheckReport] = None,
    readiness_matrix: Optional[ServiceReadinessMatrix] = None,
    gate: Optional[ReadinessGate] = None
) -> List[LifecycleRiskFlag]:
    flags = set()
    errors = validate_no_execution_readiness(startup_report, readiness_matrix, gate)
    if errors:
        flags.add(LifecycleRiskFlag.EXECUTION_ROUTE_RISK)
    return list(flags)

def no_execution_readiness_summary(errors: List[str]) -> Dict[str, Any]:
    return {"errors": errors}

def no_execution_readiness_validator_to_text(errors: List[str]) -> str:
    if not errors:
        return "No-execution readiness validated successfully."
    return "No-execution readiness errors:\n" + "\n".join([f"- {e}" for e in errors])
