from usa_signal_bot.core.enums import NoWriteTransitionCheckpointStatus, NoWriteTransitionCheckpointDecision
from usa_signal_bot.paper_admission_review.admission_review_models import FinalNoWriteTransitionCheckpoint
from usa_signal_bot.paper_admission_review.transition_checkpoint_validator import validate_transition_checkpoint_safety

def test_validate_transition_checkpoint_safety():
    checkpoint = FinalNoWriteTransitionCheckpoint(
        checkpoint_id="test",
        created_at_utc="test",
        status=NoWriteTransitionCheckpointStatus.VALIDATED_NO_WRITE,
        decision=NoWriteTransitionCheckpointDecision.CONTINUE_TO_NO_WRITE_TRANSITION_DOSSIER,
        activation_denied=True,
        activation_allowed=False,
        all_writes_blocked=True,
        mutation_detected=False,
        transition_allowed=False,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        required_followups=[],
        safety_flags=[],
        warnings=[],
        errors=[]
    )
    errors = validate_transition_checkpoint_safety(checkpoint)
    assert len(errors) == 0

    checkpoint.transition_allowed = True
    errors = validate_transition_checkpoint_safety(checkpoint)
    assert len(errors) > 0
