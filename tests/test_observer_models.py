import pytest
from datetime import datetime, timezone
from usa_signal_bot.paper_observer.observer_models import (
    LockedObserverPolicy, PaperObserverEnrollment, ObserverRuntimeContext,
    ObserverOutput, ObserverDriftEvent, ObserverRuntimeSession, ObserverAuditEntry,
    PaperObserverReview, validate_locked_observer_policy, validate_paper_observer_enrollment,
    validate_observer_runtime_context, validate_observer_output,
    create_locked_observer_policy_id
)
from usa_signal_bot.core.enums import (
    ObserverOutputType, PaperObserverEnrollmentStatus, ObserverRuntimeMode,
    ObserverMonitoringMode, ObserverDriftType, ObserverRuntimeStatus, ObserverReportType
)
from usa_signal_bot.core.exceptions import ObserverValidationError

def test_locked_observer_policy_validation():
    policy = LockedObserverPolicy(
        policy_id=create_locked_observer_policy_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        require_human_approval=True,
        require_planning_ticket=True,
        locked_runtime=True,
        allow_active_paper=False,
        allow_paper_state_mutation=False,
        allow_paper_orders=False,
        allow_broker_orders=False,
        allow_telegram_real_send=False,
        allow_config_patch=False,
        allowed_output_types=[ObserverOutputType.SIGNAL_MIRROR]
    )
    validate_locked_observer_policy(policy)

    policy.allow_active_paper = True
    with pytest.raises(ObserverValidationError):
        validate_locked_observer_policy(policy)

    policy.allow_active_paper = False
    policy.locked_runtime = False
    with pytest.raises(ObserverValidationError):
        validate_locked_observer_policy(policy)

def test_paper_observer_enrollment_validation():
    enrollment = PaperObserverEnrollment(
        enrollment_id="test_id",
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=PaperObserverEnrollmentStatus.ENROLLED,
        candidate_id="cand_1",
        planning_ticket_id="ticket_1",
        approval_queue_item_id="item_1",
        source_controlled_planning_review_id="review_1",
        source_approval_status="APPROVED",
        policy=None,
        allowed_for_active_paper=False,
        allowed_for_broker_execution=False,
        allowed_for_paper_state_mutation=False,
        allowed_for_config_patch=False,
        safety_flags=[]
    )
    validate_paper_observer_enrollment(enrollment)

    enrollment.allowed_for_broker_execution = True
    with pytest.raises(ObserverValidationError):
        validate_paper_observer_enrollment(enrollment)

def test_observer_runtime_context_validation():
    context = ObserverRuntimeContext(
        context_id="ctx_1",
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        enrollment_id="test_id",
        candidate_id="cand_1",
        runtime_mode=ObserverRuntimeMode.FULL_LOCKED_OBSERVER,
        monitoring_mode=ObserverMonitoringMode.FULL_READ_ONLY_PARALLEL_MONITOR,
        read_only_paper_snapshot={},
        candidate_metadata={},
        output_path="/tmp/output",
        locked=True,
        allow_active_paper=False,
        allow_paper_state_mutation=False,
        allow_paper_orders=False,
        allow_broker_orders=False,
        allow_telegram_real_send=False,
        allow_config_patch=False
    )
    validate_observer_runtime_context(context)

    context.locked = False
    with pytest.raises(ObserverValidationError):
        validate_observer_runtime_context(context)

def test_observer_output_validation():
    output = ObserverOutput(
        output_id="out_1",
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        output_type=ObserverOutputType.SIGNAL_MIRROR,
        symbol="AAPL",
        status="OK",
        summary={},
        payload={},
        is_real_order=False,
        mutates_paper_state=False,
        sends_to_broker=False,
        sends_telegram_real=False,
        safety_flags=[]
    )
    validate_observer_output(output)

    output.sends_to_broker = True
    with pytest.raises(ObserverValidationError):
        validate_observer_output(output)
