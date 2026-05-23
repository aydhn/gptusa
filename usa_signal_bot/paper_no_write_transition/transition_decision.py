from typing import Any, Optional
from usa_signal_bot.core.enums import (
    NoWriteTransitionDecision,
    NoWriteTransitionRiskFlag,
    AdmissionEvidenceSealValidationStatus
)
from usa_signal_bot.paper_no_write_transition.no_write_transition_models import (
    NoWriteTransitionDossier,
    TransitionDossierEvidenceItem,
    AdmissionEvidenceSealValidation,
    PaperSandboxBridgeEnvelope
)
from usa_signal_bot.paper_no_write_transition.transition_dossier import build_no_write_transition_dossier

class NoWriteTransitionDecisionEngine:
    def __init__(self, conservative: bool = True):
        self.conservative = conservative

    def collect_decision_risk_flags(
        self,
        admission_payload: dict[str, Any],
        evidence_items: list[TransitionDossierEvidenceItem],
        seal_validation: Optional[AdmissionEvidenceSealValidation] = None,
        bridge_envelope: Optional[PaperSandboxBridgeEnvelope] = None
    ) -> list[NoWriteTransitionRiskFlag]:
        from usa_signal_bot.paper_no_write_transition.transition_dossier import collect_transition_dossier_safety_flags
        flags = collect_transition_dossier_safety_flags(admission_payload, evidence_items)
        if seal_validation:
            flags.extend(seal_validation.risk_flags)
        if bridge_envelope:
            flags.extend(bridge_envelope.risk_flags)
        return list(set(flags))

    def rationale_for_transition_decision(self, decision: NoWriteTransitionDecision, flags: list[NoWriteTransitionRiskFlag]) -> str:
        if decision == NoWriteTransitionDecision.BLOCK:
            return f"Blocked due to severe risk flags: {[f.value for f in flags]}"
        if decision == NoWriteTransitionDecision.CREATE_NO_WRITE_TRANSITION_DOSSIER:
            return "All checks passed. Safe to create no-write transition dossier."
        return "Refresh or manual review requested due to missing/stale data."

    def followups_for_transition_decision(self, decision: NoWriteTransitionDecision, flags: list[NoWriteTransitionRiskFlag]) -> list[str]:
        if decision == NoWriteTransitionDecision.BLOCK:
            return ["Review safety flags and remediate immediate risks."]
        if decision == NoWriteTransitionDecision.REQUEST_EVIDENCE_SEAL_REFRESH:
            return ["Refresh admission evidence seal."]
        return []

    def decide(
        self,
        admission_payload: dict[str, Any],
        evidence_items: list[TransitionDossierEvidenceItem],
        seal_validation: Optional[AdmissionEvidenceSealValidation] = None,
        bridge_envelope: Optional[PaperSandboxBridgeEnvelope] = None
    ) -> NoWriteTransitionDossier:

        flags = self.collect_decision_risk_flags(admission_payload, evidence_items, seal_validation, bridge_envelope)

        block_flags = [
            NoWriteTransitionRiskFlag.ACTIVATION_ALLOWED_RISK,
            NoWriteTransitionRiskFlag.TRANSITION_ALLOWED_RISK,
            NoWriteTransitionRiskFlag.ACTIVE_PAPER_ENABLE_RISK,
            NoWriteTransitionRiskFlag.BROKER_ORDER_RISK,
            NoWriteTransitionRiskFlag.TELEGRAM_REAL_SEND_RISK,
            NoWriteTransitionRiskFlag.PRODUCTION_CONFIG_WRITE_RISK,
            NoWriteTransitionRiskFlag.PAPER_STATE_MUTATION_RISK,
            NoWriteTransitionRiskFlag.SANDBOX_BRIDGE_ACTIVATION_ROUTE_RISK
        ]

        decision = NoWriteTransitionDecision.INCONCLUSIVE
        if any(f in flags for f in block_flags):
            decision = NoWriteTransitionDecision.BLOCK
        elif seal_validation and seal_validation.status in [AdmissionEvidenceSealValidationStatus.STALE, AdmissionEvidenceSealValidationStatus.FAILED, AdmissionEvidenceSealValidationStatus.MISSING]:
            decision = NoWriteTransitionDecision.REQUEST_EVIDENCE_SEAL_REFRESH
        elif admission_payload.get("status") in ["STALE", "FAILED"]:
            decision = NoWriteTransitionDecision.REQUEST_ADMISSION_REVIEW_REFRESH
        else:
            decision = NoWriteTransitionDecision.CREATE_NO_WRITE_TRANSITION_DOSSIER

        dossier = build_no_write_transition_dossier(admission_payload)
        dossier.decision = decision
        from usa_signal_bot.paper_no_write_transition.eligibility_checker import transition_dossier_status_from_decision
        dossier.status = transition_dossier_status_from_decision(decision)
        dossier.safety_flags = flags

        return dossier
