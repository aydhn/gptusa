from typing import List, Dict, Any, Optional
import pandas as pd
from usa_signal_bot.release.final_closure.phase160_models import (
    FinalClosureContext,
    FinalDeliveryCertificate,
    ProjectClosureReport,
    ProjectClosureManifest,
    FinalSafetyBoundaryResult,
    FinalClosureReadinessGate,
    FinalClosureRiskFlag
)
from usa_signal_bot.release.final_closure.final_input_resolver import detect_forbidden_final_closure_fields

def validate_final_closure_context_safety(context: FinalClosureContext) -> List[str]:
    errors = []
    if context.live_trading_enabled:
        errors.append("live_trading_enabled is true")
    if context.paper_state_mutation_enabled:
        errors.append("paper_state_mutation_enabled is true")
    if context.broker_execution_enabled:
        errors.append("broker_execution_enabled is true")
    if context.real_order_creation_enabled:
        errors.append("real_order_creation_enabled is true")
    if context.telegram_real_send_enabled:
        errors.append("telegram_real_send_enabled is true")
    if context.deployment_allowed:
        errors.append("deployment_allowed is true")
    if context.production_patch_allowed:
        errors.append("production_patch_allowed is true")
    return errors

def validate_final_delivery_certificate_safety(certificate: FinalDeliveryCertificate) -> List[str]:
    errors = []
    if not certificate.not_deployment_approval:
        errors.append("not_deployment_approval is false")
    if not certificate.not_trading_approval:
        errors.append("not_trading_approval is false")
    if not certificate.not_broker_approval:
        errors.append("not_broker_approval is false")
    return errors

def validate_project_closure_report_safety(report: ProjectClosureReport) -> List[str]:
    errors = []
    if not report.not_deployment_approval:
        errors.append("not_deployment_approval is false")
    if not report.not_trading_approval:
        errors.append("not_trading_approval is false")
    return errors

def validate_project_closure_manifest_safety(manifest: ProjectClosureManifest) -> List[str]:
    errors = []
    if not manifest.no_deployment:
        errors.append("no_deployment is false")
    if not manifest.no_trading_activation:
        errors.append("no_trading_activation is false")
    if not manifest.no_broker_activation:
        errors.append("no_broker_activation is false")
    return errors

def validate_final_safety_boundary_safety(boundary: FinalSafetyBoundaryResult) -> List[str]:
    errors = []
    if not boundary.boundary_passed:
        errors.append("boundary_passed is false")
    return errors

def validate_final_closure_readiness_gate_safety(gate: FinalClosureReadinessGate) -> List[str]:
    errors = []
    if not gate.project_closed and gate.status.value == "PASSED":
        errors.append("Gate passed but project_closed is false")
    return errors

def validate_final_closure_dataframe_output_safety(df: pd.DataFrame) -> List[str]:
    from usa_signal_bot.release.final_closure.final_input_resolver import detect_forbidden_final_closure_columns
    forbidden = detect_forbidden_final_closure_columns(list(df.columns))
    if forbidden:
        return [f"Dataframe contains forbidden columns: {forbidden}"]
    return []

def final_closure_text_has_trade_or_execution_language(text: str) -> bool:
    unsafe_words = ['emir gönderildi', 'aktif trading başladı', 'kesin al', 'kesin sat', 'garanti kâr', 'yatırım tavsiyesi']
    text_lower = text.lower()
    for word in unsafe_words:
        if word in text_lower:
            return True
    return False

def final_closure_payload_has_forbidden_fields(payload: dict[str, Any]) -> bool:
    forbidden = detect_forbidden_final_closure_fields(payload)
    return len(forbidden) > 0

def collect_final_closure_risk_flags(context: Optional[FinalClosureContext] = None) -> List[FinalClosureRiskFlag]:
    if not context:
        return []
    flags = set()
    if context.ingestion:
        flags.update(context.ingestion.risk_flags)
    for ref in context.input_references:
        flags.update(ref.risk_flags)
    if context.final_safety_boundary:
        flags.update(context.final_safety_boundary.risk_flags)
    return list(flags)

def final_closure_safety_summary(errors: List[str]) -> Dict[str, Any]:
    return {"safe": len(errors) == 0, "error_count": len(errors), "errors": errors}

def final_closure_safety_to_text(errors: List[str]) -> str:
    return f"Safety Validation: Safe={len(errors) == 0}, Errors={len(errors)}"
