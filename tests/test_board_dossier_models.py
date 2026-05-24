from usa_signal_bot.paper_readiness_board_dossier.board_dossier_models import (
    BoardDossierEvidenceItem,
    AcceptanceBoardSeal,
    ShadowLaunchBlockerRule,
    ShadowLaunchBlockerEvent,
    PaperReadinessBoardDossier,
    BoardDossierFullReview
)
from usa_signal_bot.core.enums import (
    BoardDossierEvidenceStatus,
    AcceptanceBoardSealStatus,
    AcceptanceBoardSealDecision,
    ShadowLaunchBlockerAction,
    ShadowLaunchAttemptType,
    ShadowLaunchBlockerStatus,
    ShadowLaunchBlockerDecision,
    PaperReadinessBoardDossierStatus,
    PaperReadinessBoardDossierDecision,
    BoardDossierReportType
)
from usa_signal_bot.paper_readiness_board_dossier.acceptance_board_seal_validator import validate_acceptance_board_seal_safety
from usa_signal_bot.paper_readiness_board_dossier.board_dossier_validation import validate_board_dossier_report

def test_board_dossier_models_importable():
    # If this runs, it imported fine
    assert True

def test_acceptance_board_seal_safety():
    seal = AcceptanceBoardSeal(
        seal_id="s1",
        created_at_utc="now",
        status=AcceptanceBoardSealStatus.SEALED,
        decision=AcceptanceBoardSealDecision.SEAL_ACCEPTANCE_BOARD,
        board_gates_passed=True,
        board_assertions_passed=True,
        runtime_replay_passed=True,
        all_dangerous_runtime_routes_denied=True,
        non_execution_seal_integrity_valid=True,
        sealed=True,
        immutable=True,
        seal_is_metadata_only=True,
        allows_shadow_launch=False,
        allows_paper_mode_launch=False,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        risk_flags=[],
        required_followups=[],
        warnings=[],
        errors=[]
    )
    assert len(validate_acceptance_board_seal_safety(seal)) == 0
