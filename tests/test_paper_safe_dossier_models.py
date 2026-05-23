from usa_signal_bot.paper_safe_dossier.paper_safe_dossier_models import (
    PaperSafeDossierEvidenceItem,
    NonExecutionAcceptanceSeal,
    RuntimeComponentMapItem,
    RuntimeRouteMapItem,
    PrePaperLocalRuntimeMap,
    PaperSafeGateDossier,
    PaperSafeDossierFullReview
)
from usa_signal_bot.core.enums import PaperSafeDossierEvidenceStatus, NonExecutionAcceptanceSealStatus, NonExecutionAcceptanceSealDecision, PrePaperRuntimeMapStatus, PrePaperRuntimeMapDecision, RuntimeComponentMode, RuntimeRoutePermission, PaperSafeDossierStatus, PaperSafeDossierDecision, PaperSafeDossierReportType

def test_paper_safe_dossier_models():
    item = PaperSafeDossierEvidenceItem(
        evidence_id="1",
        created_at_utc="2023-01-01T00:00:00Z",
        evidence_type="test",
        source_ref_id=None,
        source_path=None,
        status=PaperSafeDossierEvidenceStatus.FRESH,
        required=True,
        available=True,
        fresh=True,
        stale=False,
        summary={},
        risk_flags=[],
        warnings=[],
        errors=[]
    )
    assert item.evidence_id == "1"

    seal = NonExecutionAcceptanceSeal(
        seal_id="2",
        created_at_utc="2023-01-01T00:00:00Z",
        status=NonExecutionAcceptanceSealStatus.SEALED,
        decision=NonExecutionAcceptanceSealDecision.SEAL_NON_EXECUTION_ACCEPTANCE,
        candidate_id=None,
        source_paper_safe_gate_id=None,
        source_paper_safe_review_id=None,
        seal_hash=None,
        accepted_boundaries=[],
        sealed=True,
        immutable=True,
        non_execution_confirmed=True,
        no_broker_confirmed=True,
        no_active_paper_confirmed=True,
        no_paper_admission_confirmed=True,
        no_order_confirmed=True,
        no_write_confirmed=True,
        no_telegram_real_send_confirmed=True,
        no_config_patch_confirmed=True,
        seal_is_metadata_only=True,
        risk_flags=[],
        required_followups=[],
        warnings=[],
        errors=[]
    )
    assert seal.seal_id == "2"
