import pytest
from usa_signal_bot.paper_readiness_confirmation.confirmation_models import (
    ReadinessConfirmationQueueItem,
    HumanReviewBundle,
    HumanReviewChecklistItem,
    ReviewerNote,
    ActivationStillDeniedRegistryEntry,
    ReadinessConfirmationReview,
    create_readiness_confirmation_queue_item_id,
    validate_readiness_confirmation_queue_item,
    validate_human_review_bundle,
    validate_activation_still_denied_registry_entry
)
from usa_signal_bot.core.enums import (
    ReadinessConfirmationQueueStatus,
    ReadinessConfirmationDecision,
    HumanReviewBundleStatus,
    ActivationStillDeniedRegistryStatus,
    ActivationStillDeniedDecision,
    ReadinessConfidenceLevel
)

def test_queue_item_validation_success():
    item = ReadinessConfirmationQueueItem(
        queue_item_id="test", created_at_utc="test", status=ReadinessConfirmationQueueStatus.DRAFT,
        decision=ReadinessConfirmationDecision.UNKNOWN, candidate_id=None,
        source_firewall_audit_review_id=None, source_readiness_audit_checkpoint_id=None,
        source_zero_mutation_audit_id=None, source_firewall_replay_result_id=None,
        evidence_refs=[], required_followups=[], readiness_confidence=ReadinessConfidenceLevel.UNKNOWN,
        safety_flags=[], manual_review_required=True, activation_denied_required=True,
        allows_active_paper=False, allows_broker_execution=False, allows_paper_state_mutation=False,
        allows_config_patch=False, allows_telegram_real_send=False, warnings=[], errors=[], metadata={}
    )
    validate_readiness_confirmation_queue_item(item)

def test_queue_item_validation_failure():
    item = ReadinessConfirmationQueueItem(
        queue_item_id="test", created_at_utc="test", status=ReadinessConfirmationQueueStatus.DRAFT,
        decision=ReadinessConfirmationDecision.UNKNOWN, candidate_id=None,
        source_firewall_audit_review_id=None, source_readiness_audit_checkpoint_id=None,
        source_zero_mutation_audit_id=None, source_firewall_replay_result_id=None,
        evidence_refs=[], required_followups=[], readiness_confidence=ReadinessConfidenceLevel.UNKNOWN,
        safety_flags=[], manual_review_required=True, activation_denied_required=True,
        allows_active_paper=True, allows_broker_execution=False, allows_paper_state_mutation=False,
        allows_config_patch=False, allows_telegram_real_send=False, warnings=[], errors=[], metadata={}
    )
    with pytest.raises(ValueError, match="must not allow active execution"):
        validate_readiness_confirmation_queue_item(item)

def test_human_review_bundle_validation_success():
    bundle = HumanReviewBundle(
        bundle_id="test", created_at_utc="test", status=HumanReviewBundleStatus.DRAFT,
        candidate_id=None, queue_item_id=None, title="test", summary={}, checklist_refs=[],
        evidence_refs=[], reviewer_note_refs=[], required_reviewer_actions=[], safety_flags=[],
        activation_denied=True, activation_allowed=False, allows_active_paper=False,
        allows_broker_execution=False, allows_paper_state_mutation=False, allows_config_patch=False,
        allows_telegram_real_send=False, warnings=[], errors=[], metadata={}
    )
    validate_human_review_bundle(bundle)

def test_human_review_bundle_validation_failure():
    bundle = HumanReviewBundle(
        bundle_id="test", created_at_utc="test", status=HumanReviewBundleStatus.DRAFT,
        candidate_id=None, queue_item_id=None, title="test", summary={}, checklist_refs=[],
        evidence_refs=[], reviewer_note_refs=[], required_reviewer_actions=[], safety_flags=[],
        activation_denied=True, activation_allowed=True, allows_active_paper=False,
        allows_broker_execution=False, allows_paper_state_mutation=False, allows_config_patch=False,
        allows_telegram_real_send=False, warnings=[], errors=[], metadata={}
    )
    with pytest.raises(ValueError, match="activation_allowed must be False"):
        validate_human_review_bundle(bundle)

def test_activation_denied_registry_validation_success():
    entry = ActivationStillDeniedRegistryEntry(
        registry_entry_id="test", created_at_utc="test", status=ActivationStillDeniedRegistryStatus.DRAFT,
        decision=ActivationStillDeniedDecision.UNKNOWN, candidate_id=None, queue_item_id=None,
        bundle_id=None, source_checkpoint_id=None, activation_denied=True, activation_allowed=False,
        denial_reason="test", required_followups=[], safety_flags=[], allows_active_paper=False,
        allows_broker_execution=False, allows_paper_state_mutation=False, allows_config_patch=False,
        allows_telegram_real_send=False, warnings=[], errors=[], metadata={}
    )
    validate_activation_still_denied_registry_entry(entry)

def test_activation_denied_registry_validation_failure():
    entry = ActivationStillDeniedRegistryEntry(
        registry_entry_id="test", created_at_utc="test", status=ActivationStillDeniedRegistryStatus.DRAFT,
        decision=ActivationStillDeniedDecision.UNKNOWN, candidate_id=None, queue_item_id=None,
        bundle_id=None, source_checkpoint_id=None, activation_denied=False, activation_allowed=False,
        denial_reason="test", required_followups=[], safety_flags=[], allows_active_paper=False,
        allows_broker_execution=False, allows_paper_state_mutation=False, allows_config_patch=False,
        allows_telegram_real_send=False, warnings=[], errors=[], metadata={}
    )
    with pytest.raises(ValueError, match="activation_denied must be True"):
        validate_activation_still_denied_registry_entry(entry)
