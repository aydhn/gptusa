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
