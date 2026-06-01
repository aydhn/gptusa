from typing import Any, Dict
from ..ml_research.foundation.phase136_models import MLFoundationFullReview

class NotificationMessage:
    def __init__(self, message: str):
        self.message = message

def format_ml_foundation_report_message(review: MLFoundationFullReview) -> NotificationMessage:
    return NotificationMessage(f"ML Foundation Review {review.review_id} generated. Ready for Phase 137: {review.readiness_gate.ready_for_phase137}.")

def notifications_from_ml_foundation_review(review: MLFoundationFullReview) -> list[NotificationMessage]:
    return [format_ml_foundation_report_message(review)]


def format_ml_dataset_assembly_report_message(review: 'Any') -> 'Any':
    from usa_signal_bot.notifications.notification_models import NotificationMessage
    from usa_signal_bot.ml_research.experiment_scaffolding.phase138_models import BaselineMLScaffoldingFullReview, EvaluationHarnessContract, ModelCardDraft
    from usa_signal_bot.core.enums import NotificationType
    import uuid
    from datetime import datetime, timezone
    now_str = datetime.now(timezone.utc).isoformat()
    return NotificationMessage(
        message_id=f"notif_{uuid.uuid4().hex[:12]}",
        created_at_utc=now_str,
        notification_type=NotificationType.ML_DATASET_ASSEMBLY_REPORT,
        subject="ML Dataset Assembly Report",
        body=f"ML Dataset Assembly Report ID: {review.review_id}",
        severity="INFO",
        metadata={"review_id": review.review_id}
    )

def format_ml_leakage_audit_warning_message(result: 'Any') -> 'Any':
    from usa_signal_bot.notifications.notification_models import NotificationMessage
    from usa_signal_bot.ml_research.experiment_scaffolding.phase138_models import BaselineMLScaffoldingFullReview, EvaluationHarnessContract, ModelCardDraft
    from usa_signal_bot.core.enums import NotificationType
    import uuid
    from datetime import datetime, timezone
    now_str = datetime.now(timezone.utc).isoformat()
    return NotificationMessage(
        message_id=f"notif_{uuid.uuid4().hex[:12]}",
        created_at_utc=now_str,
        notification_type=NotificationType.ML_LEAKAGE_AUDIT_WARNING,
        subject="ML Leakage Audit Warning",
        body=f"ML Leakage Audit Warnings/Failures detected in Audit ID: {result.audit_id}",
        severity="WARNING",
        metadata={"audit_id": result.audit_id}
    )

def format_ml_split_quality_warning_message(profile: 'Any') -> 'Any':
    from usa_signal_bot.notifications.notification_models import NotificationMessage
    from usa_signal_bot.ml_research.experiment_scaffolding.phase138_models import BaselineMLScaffoldingFullReview, EvaluationHarnessContract, ModelCardDraft
    from usa_signal_bot.core.enums import NotificationType
    import uuid
    from datetime import datetime, timezone
    now_str = datetime.now(timezone.utc).isoformat()
    return NotificationMessage(
        message_id=f"notif_{uuid.uuid4().hex[:12]}",
        created_at_utc=now_str,
        notification_type=NotificationType.ML_SPLIT_QUALITY_WARNING,
        subject="ML Split Quality Warning",
        body=f"ML Split Quality is Low/Warning in Profile ID: {profile.profile_id}. Score: {profile.score}",
        severity="WARNING",
        metadata={"profile_id": profile.profile_id}
    )

def notifications_from_ml_dataset_assembly_review(review: 'Any') -> list:
    msgs = [format_ml_dataset_assembly_report_message(review)]
    if review.leakage_audit and (review.leakage_audit.failed_rules > 0 or review.leakage_audit.warning_rules > 0):
        msgs.append(format_ml_leakage_audit_warning_message(review.leakage_audit))
    if review.split_quality_profile and review.split_quality_profile.score < 80.0:
        msgs.append(format_ml_split_quality_warning_message(review.split_quality_profile))
    return msgs

# Phase 113 Notifications dummy
def format_provider_governance_report_message(review): pass
def format_data_lineage_warning_message(graph): pass
def format_audit_trail_warning_message(manifest): pass
def notifications_from_provider_governance_review(review): pass


def format_baseline_ml_scaffolding_report_message(review: 'BaselineMLScaffoldingFullReview') -> NotificationMessage:
    lines = [
        "🔬 Baseline ML Scaffolding Report (Phase 138)",
        f"Review ID: {review.review_id}",
        f"Ready for Phase 139: {review.readiness_gate.ready_for_phase139}",
        f"Experiments: {review.experiment_registry.experiment_count}",
        f"Harness Valid: {review.evaluation_harness_contract.contract_valid}",
        f"Non-Activation Passed: {review.non_activation_boundary.boundary_passed}",
        "",
        "Note: This is a metadata-only non-activation phase. No models were trained. No predictions were made. Not investment advice."
    ]
    return NotificationMessage(
        message_id=f"notif_{uuid.uuid4().hex[:8]}",
        notification_type=NotificationType.BASELINE_ML_SCAFFOLDING_REPORT,
        subject="Baseline ML Scaffolding Report",
        body="\n".join(lines),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        metadata={"review_id": review.review_id}
    )

def format_evaluation_harness_warning_message(contract: 'EvaluationHarnessContract') -> NotificationMessage:
    lines = [
        "⚠️ Evaluation Harness Warning",
        f"Harness ID: {contract.harness_id}",
        "Issues found in Evaluation Harness Contract setup."
    ]
    for w in contract.warnings:
        lines.append(f"- {w}")
    for e in contract.errors:
        lines.append(f"- [ERROR] {e}")

    return NotificationMessage(
        message_id=f"notif_{uuid.uuid4().hex[:8]}",
        notification_type=NotificationType.EVALUATION_HARNESS_WARNING,
        subject="Evaluation Harness Warning",
        body="\n".join(lines),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        metadata={"harness_id": contract.harness_id}
    )

def format_model_card_draft_warning_message(cards: list['ModelCardDraft']) -> NotificationMessage:
    lines = [
        "⚠️ Model Card Draft Warning",
        f"Cards with warnings: {len(cards)}"
    ]
    for c in cards:
        if c.errors or c.warnings:
            lines.append(f"\nCard: {c.card_title}")
            for e in c.errors: lines.append(f"- [ERROR] {e}")

    return NotificationMessage(
        message_id=f"notif_{uuid.uuid4().hex[:8]}",
        notification_type=NotificationType.MODEL_CARD_DRAFT_WARNING,
        subject="Model Card Draft Warning",
        body="\n".join(lines),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        metadata={"card_count": len(cards)}
    )

def notifications_from_baseline_ml_scaffolding_review(review: 'BaselineMLScaffoldingFullReview') -> list[NotificationMessage]:
    messages = [format_baseline_ml_scaffolding_report_message(review)]
    if not review.evaluation_harness_contract.contract_valid or review.evaluation_harness_contract.errors:
        messages.append(format_evaluation_harness_warning_message(review.evaluation_harness_contract))

    bad_cards = [c for c in review.experiment_registry.model_card_drafts if not c.draft_only or c.errors or c.warnings]
    if bad_cards:
        messages.append(format_model_card_draft_warning_message(bad_cards))

    return messages

def format_baseline_training_report_message(review: Any) -> NotificationMessage:
    lines = [
        "🔬 Baseline Training Report",
        f"Review ID: {review.review_id}",
        f"Jobs: {len(review.training_jobs)}",
        f"Models: {len(review.fitted_models)}",
        f"Predictions: {len(review.prediction_artifacts)}",
        f"Reports: {len(review.evaluation_reports)}",
        f"Ready for Phase 140: {review.readiness_gate.ready_for_phase140}"
    ]
    return NotificationMessage(
        type=NotificationType.BASELINE_TRAINING_REPORT,
        subject="Baseline Training Report",
        content="\n".join(lines),
        metadata={"review_id": review.review_id}
    )

def format_offline_evaluation_warning_message(reports: list[Any]) -> NotificationMessage:
    lines = [
        "⚠️ Offline Evaluation Warnings",
        f"Found warnings in {len(reports)} reports."
    ]
    return NotificationMessage(
        type=NotificationType.OFFLINE_EVALUATION_WARNING,
        subject="Offline Evaluation Warning",
        content="\n".join(lines),
        metadata={"report_count": len(reports)}
    )

def format_non_activation_model_registry_warning_message(registry: Any) -> NotificationMessage:
    lines = [
        "⚠️ Model Registry Warnings",
        f"Registry ID: {registry.registry_id}",
        f"Warnings: {len(registry.warnings)}"
    ]
    return NotificationMessage(
        type=NotificationType.NON_ACTIVATION_MODEL_REGISTRY_WARNING,
        subject="Model Registry Warning",
        content="\n".join(lines),
        metadata={"registry_id": registry.registry_id}
    )

def notifications_from_baseline_training_review(review: Any) -> list[NotificationMessage]:
    messages = []
    messages.append(format_baseline_training_report_message(review))
    reports_with_warnings = [r for r in review.evaluation_reports if len(r.warnings) > 0]
    if reports_with_warnings:
        messages.append(format_offline_evaluation_warning_message(reports_with_warnings))
    if len(review.model_registry.warnings) > 0:
        messages.append(format_non_activation_model_registry_warning_message(review.model_registry))
    return messages
from typing import Any

class NotificationMessage:
    def __init__(self, message_type: str, content: str):
        self.message_type = message_type
        self.content = content

def format_baseline_model_comparison_report_message(review: Any) -> NotificationMessage:
    content = f"Baseline Model Comparison Report Generated. ID: {review.review_id}\n(Research metadata only. No active trading.)"
    return NotificationMessage("BASELINE_MODEL_COMPARISON_REPORT", content)

def format_model_ranking_warning_message(ranking: Any) -> NotificationMessage:
    content = f"Model Ranking Warning. Rankable entries: {ranking.rankable_entry_count}"
    return NotificationMessage("MODEL_RANKING_WARNING", content)

def format_calibration_preparation_warning_message(profiles: list) -> NotificationMessage:
    content = f"Calibration Preparation Warning for {len(profiles)} profiles."
    return NotificationMessage("CALIBRATION_PREPARATION_WARNING", content)

def notifications_from_model_comparison_review(review: Any) -> list[NotificationMessage]:
    return [format_baseline_model_comparison_report_message(review)]


def format_calibration_diagnostics_report_message(review: 'Any') -> 'Any':
    try:
        from usa_signal_bot.notifications.notification_adapters import NotificationMessage
        from usa_signal_bot.core.enums import NotificationType
        return NotificationMessage(
            message_id="dummy",
            type=NotificationType.CALIBRATION_DIAGNOSTICS_REPORT,
            subject="Phase 141 Calibration Diagnostics",
            body="Calibration diagnostics review built successfully. No live inference or deployment was performed.",
            severity="INFO",
            timestamp="2024-01-01T00:00:00Z"
        )
    except Exception:
        return None

def format_probability_reliability_warning_message(reports: list) -> 'Any':
    try:
        from usa_signal_bot.notifications.notification_adapters import NotificationMessage
        from usa_signal_bot.core.enums import NotificationType
        return NotificationMessage(
            message_id="dummy",
            type=NotificationType.PROBABILITY_RELIABILITY_WARNING,
            subject="Phase 141 Probability Reliability Warning",
            body="Warnings found during reliability binning.",
            severity="WARNING",
            timestamp="2024-01-01T00:00:00Z"
        )
    except Exception:
        return None

def format_post_training_validation_warning_message(validations: list) -> 'Any':
    try:
        from usa_signal_bot.notifications.notification_adapters import NotificationMessage
        from usa_signal_bot.core.enums import NotificationType
        return NotificationMessage(
            message_id="dummy",
            type=NotificationType.POST_TRAINING_VALIDATION_WARNING,
            subject="Phase 141 Post-Training Validation Warning",
            body="Warnings found during post-training validation.",
            severity="WARNING",
            timestamp="2024-01-01T00:00:00Z"
        )
    except Exception:
        return None

def notifications_from_calibration_diagnostics_review(review: 'Any') -> list:
    res = []
    msg1 = format_calibration_diagnostics_report_message(review)
    if msg1: res.append(msg1)
    msg2 = format_probability_reliability_warning_message([])
    if msg2: res.append(msg2)
    msg3 = format_post_training_validation_warning_message([])
    if msg3: res.append(msg3)
    return res
