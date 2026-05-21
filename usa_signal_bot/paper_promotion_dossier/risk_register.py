from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from usa_signal_bot.core.enums import PromotionDossierRiskFlag, ReadinessGateStatus
from .dossier_models import ObserverPromotionDossier, FinalSafetyBoardGate, PromotionRiskRegisterItem, create_promotion_risk_register_item_id

def build_promotion_risk_register(dossier: ObserverPromotionDossier, gates: Optional[List[FinalSafetyBoardGate]] = None) -> List[PromotionRiskRegisterItem]:
    flags = set(dossier.safety_flags)
    if gates:
        for g in gates:
            if g.status == ReadinessGateStatus.FAIL:
                for f in g.risk_flags:
                    flags.add(f)

    items = []
    for f in flags:
        items.append(risk_register_item_from_flag(f))
    return items

def risk_register_item_from_flag(flag: PromotionDossierRiskFlag, evidence_refs: Optional[List[str]] = None) -> PromotionRiskRegisterItem:
    blocking_flags = [
        PromotionDossierRiskFlag.ACTIVE_PAPER_ENABLE_RISK,
        PromotionDossierRiskFlag.PAPER_STATE_MUTATION_RISK,
        PromotionDossierRiskFlag.PAPER_ORDER_RISK,
        PromotionDossierRiskFlag.BROKER_ORDER_RISK,
        PromotionDossierRiskFlag.TELEGRAM_REAL_SEND_RISK,
        PromotionDossierRiskFlag.PRODUCTION_CONFIG_WRITE_RISK,
        PromotionDossierRiskFlag.REAL_ORDER_RISK
    ]

    is_blocking = flag in blocking_flags
    severity = "HIGH" if is_blocking else "MEDIUM"

    return PromotionRiskRegisterItem(
        risk_id=create_promotion_risk_register_item_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        risk_flag=flag,
        severity=severity,
        description=f"Identified risk: {flag.value}",
        mitigation="Ensure configuration explicitly disables execution.",
        blocking=is_blocking,
        evidence_refs=evidence_refs or [],
        warnings=[],
        errors=[]
    )

def risk_register_blocking_flags(items: List[PromotionRiskRegisterItem]) -> List[PromotionDossierRiskFlag]:
    return [item.risk_flag for item in items if item.blocking]

def risk_register_summary(items: List[PromotionRiskRegisterItem]) -> Dict[str, Any]:
    return {
        "total_risks": len(items),
        "blocking_risks": len(risk_register_blocking_flags(items))
    }

def risk_register_to_text(items: List[PromotionRiskRegisterItem], limit: int = 100) -> str:
    lines = [f"Risk Register ({len(items)} items):"]
    for i in items[:limit]:
        lines.append(f"- {i.risk_flag.value} (Severity: {i.severity}, Blocking: {i.blocking})")
    return "\n".join(lines)
