
from typing import List, Dict, Any
from usa_signal_bot.provider_freeze.phase114_models import (
    ProviderFreezeFullReview,
    MultiProviderFinalReviewReport,
    DataLayerRehearsalReport
)

class NotificationMessage:
    def __init__(self, title: str, body: str, type: str):
        self.title = title
        self.body = body
        self.type = type

def format_provider_freeze_report_message(review: ProviderFreezeFullReview) -> NotificationMessage:
    return NotificationMessage(
        title=f"Provider Freeze Report: {review.review_id}",
        body=f"Ready for Phase 115: {review.context.ready_for_phase115}. Validation status: {review.freeze_bundle.freeze_valid}",
        type="PROVIDER_FREEZE_REPORT"
    )

def format_multi_provider_review_warning_message(report: MultiProviderFinalReviewReport) -> NotificationMessage:
    return NotificationMessage(
        title="Multi-Provider Review Warning",
        body=f"Warning items found: {report.warning_items}, Failed: {report.failed_items}",
        type="MULTI_PROVIDER_REVIEW_WARNING"
    )

def format_data_layer_rehearsal_warning_message(report: DataLayerRehearsalReport) -> NotificationMessage:
    return NotificationMessage(
        title="Data Layer Rehearsal Warning",
        body=f"Failed scenarios: {report.failed_scenarios}, Warning scenarios: {report.warning_scenarios}",
        type="DATA_LAYER_REHEARSAL_WARNING"
    )

def notifications_from_provider_freeze_review(review: ProviderFreezeFullReview) -> List[NotificationMessage]:
    msgs = [format_provider_freeze_report_message(review)]
    if not review.multi_provider_review.multi_provider_review_passed or review.multi_provider_review.warning_items > 0:
        msgs.append(format_multi_provider_review_warning_message(review.multi_provider_review))
    if not review.rehearsal_report.rehearsal_passed or review.rehearsal_report.warning_scenarios > 0:
        msgs.append(format_data_layer_rehearsal_warning_message(review.rehearsal_report))
    return msgs

# Phase 113 Notifications dummy
def format_provider_governance_report_message(review): pass
def format_data_lineage_warning_message(graph): pass
def format_audit_trail_warning_message(manifest): pass
def notifications_from_provider_governance_review(review): pass


def format_feature_foundation_report_message(review) -> dict:
    return {"message": "Dry-run feature foundation report", "type": "FEATURE_FOUNDATION_REPORT"}

def format_feature_contract_warning_message(contract) -> dict:
    return {"message": "Dry-run feature contract warning", "type": "FEATURE_CONTRACT_WARNING"}

def format_feature_registry_warning_message(registry) -> dict:
    return {"message": "Dry-run feature registry warning", "type": "FEATURE_REGISTRY_WARNING"}

def notifications_from_feature_foundation_review(review) -> list:
    return [format_feature_foundation_report_message(review)]


# Phase 117 Notifications
def format_core_indicator_report_message(review) -> dict: return {}
def format_feature_computation_warning_message(results) -> dict: return {}
def format_feature_table_warning_message(tables) -> dict: return {}
def notifications_from_core_indicator_review(review) -> list: return []


from usa_signal_bot.feature_engine.advanced_features.phase118_models import AdvancedFeatureFullReview, AdvancedFeatureComputationResult, AdvancedFeatureTableResult

class NotificationMessage:
    def __init__(self, message: str, type: str):
        self.message = message
        self.type = type

def format_advanced_feature_report_message(review: AdvancedFeatureFullReview) -> NotificationMessage:
    msg = f"Phase 118 Review {review.review_id} completed. This is a local-only research artifact and NOT investment advice."
    return NotificationMessage(message=msg, type="ADVANCED_FEATURE_REPORT")

def format_cross_sectional_feature_warning_message(result: AdvancedFeatureComputationResult) -> NotificationMessage:
    msg = f"Cross sectional feature warning for {result.result_id}."
    return NotificationMessage(message=msg, type="CROSS_SECTIONAL_FEATURE_WARNING")

def format_advanced_feature_table_warning_message(tables: list[AdvancedFeatureTableResult]) -> NotificationMessage:
    msg = f"Advanced feature table warning for {len(tables)} tables."
    return NotificationMessage(message=msg, type="ADVANCED_FEATURE_TABLE_WARNING")

def notifications_from_advanced_feature_review(review: AdvancedFeatureFullReview) -> list[NotificationMessage]:
    return [format_advanced_feature_report_message(review)]

from typing import Any

def format_feature_enrichment_report_message(review: Any) -> Any:
    return {"subject": "Feature Enrichment Review", "body": "Phase 119 completed.", "risk_flags": []}

def format_feature_interaction_warning_message(result: Any) -> Any:
    return {"subject": "Feature Interaction Warning", "body": "Check interaction schema.", "risk_flags": []}

def format_enriched_feature_table_warning_message(tables: list[Any]) -> Any:
    return {"subject": "Enriched Feature Table Warning", "body": "Check table schema.", "risk_flags": []}

def notifications_from_feature_enrichment_review(review: Any) -> list[Any]:
    return [format_feature_enrichment_report_message(review)]

def format_factor_composition_report_message(review: Any) -> Any:
    # Dry-run stub
    pass

def format_feature_selection_warning_message(items: list[Any]) -> Any:
    # Dry-run stub
    pass

def format_factor_readiness_warning_message(gate: Any) -> Any:
    # Dry-run stub
    pass

def notifications_from_factor_composition_review(review: Any) -> list[Any]:
    return []

# Phase 113 Notifications dummy
def format_provider_governance_report_message(review): pass
def format_data_lineage_warning_message(graph): pass
def format_audit_trail_warning_message(manifest): pass
def notifications_from_provider_governance_review(review): pass

# Phase 113 Notifications dummy
def format_provider_governance_report_message(review): pass
def format_data_lineage_warning_message(graph): pass
def format_audit_trail_warning_message(manifest): pass
def notifications_from_provider_governance_review(review): pass


def format_factor_validation_report_message(review) -> dict:
    return {"message": "Dry-run factor validation report", "type": "FACTOR_VALIDATION_REPORT"}

def format_factor_drift_warning_message(reports) -> dict:
    return {"message": "Dry-run factor drift warning", "type": "FACTOR_DRIFT_WARNING"}

def format_factor_store_hardening_warning_message(result) -> dict:
    return {"message": "Dry-run factor store hardening warning", "type": "FACTOR_STORE_HARDENING_WARNING"}

def notifications_from_factor_validation_review(review) -> list:
    return [format_factor_validation_report_message(review)]

# Phase 113 Notifications dummy
def format_provider_governance_report_message(review): pass
def format_data_lineage_warning_message(graph): pass
def format_audit_trail_warning_message(manifest): pass
def notifications_from_provider_governance_review(review): pass

# Phase 113 Notifications dummy
def format_provider_governance_report_message(review): pass
def format_data_lineage_warning_message(graph): pass
def format_audit_trail_warning_message(manifest): pass
def notifications_from_provider_governance_review(review): pass

# Phase 113 Notifications dummy
def format_provider_governance_report_message(review): pass
def format_data_lineage_warning_message(graph): pass
def format_audit_trail_warning_message(manifest): pass
def notifications_from_provider_governance_review(review): pass

def format_freeze_preparation_report_message(review) -> dict:
    return {"message": "Freeze Preparation Report - DRY RUN", "type": "FREEZE_PREPARATION_REPORT"}

def format_integration_rehearsal_warning_message(result) -> dict:
    return {"message": "Integration Rehearsal Warning", "type": "INTEGRATION_REHEARSAL_WARNING"}

def format_freeze_readiness_warning_message(gate) -> dict:
    return {"message": "Freeze Readiness Warning", "type": "FREEZE_READINESS_WARNING"}

def notifications_from_freeze_preparation_review(review) -> list:
    return [format_freeze_preparation_report_message(review)]

# Phase 113 Notifications dummy
def format_provider_governance_report_message(review): pass
def format_data_lineage_warning_message(graph): pass
def format_audit_trail_warning_message(manifest): pass
def notifications_from_provider_governance_review(review): pass


# Phase 125 Notification Templates
def format_final_closure_report_message(review: Any) -> NotificationMessage:
    return NotificationMessage("Final Closure Report", "Ready for Phase 126", "FINAL_CLOSURE_REPORT")

def format_freeze_seal_warning_message(seal: Any) -> NotificationMessage:
    return NotificationMessage("Freeze Seal Warning", "Seal is invalid", "FREEZE_SEAL_WARNING")

def format_phase126_kickoff_warning_message(gate: Any) -> NotificationMessage:
    return NotificationMessage("Phase 126 Kickoff Warning", "Gate failed", "PHASE126_KICKOFF_WARNING")

def notifications_from_final_closure_review(review: Any) -> List[NotificationMessage]:
    return [format_final_closure_report_message(review)]


# Phase 125 Notification Templates
def format_final_closure_report_message(review: Any) -> NotificationMessage:
    return NotificationMessage("Final Closure Report", "Ready for Phase 126", "FINAL_CLOSURE_REPORT")

def format_freeze_seal_warning_message(seal: Any) -> NotificationMessage:
    return NotificationMessage("Freeze Seal Warning", "Seal is invalid", "FREEZE_SEAL_WARNING")

def format_phase126_kickoff_warning_message(gate: Any) -> NotificationMessage:
    return NotificationMessage("Phase 126 Kickoff Warning", "Gate failed", "PHASE126_KICKOFF_WARNING")

def notifications_from_final_closure_review(review: Any) -> List[NotificationMessage]:
    return [format_final_closure_report_message(review)]

# Phase 113 Notifications dummy
def format_provider_governance_report_message(review): pass
def format_data_lineage_warning_message(graph): pass
def format_audit_trail_warning_message(manifest): pass
def notifications_from_provider_governance_review(review): pass

# Phase 128 templates
def format_regime_labeling_report_message(review): pass

def format_regime_transition_analytics_report_message(review):
    return {'type': 'REGIME_TRANSITION_ANALYTICS_REPORT', 'text': 'Dry Run Preview: Analytics Report'}
def format_regime_stability_warning_message(items):
    return {'type': 'REGIME_STABILITY_WARNING', 'text': 'Dry Run Preview: Stability Warning'}
def format_regime_churn_warning_message(items):
    return {'type': 'REGIME_CHURN_WARNING', 'text': 'Dry Run Preview: Churn Warning'}
def notifications_from_regime_transition_review(review):
    return [format_regime_transition_analytics_report_message(review)]

# Phase 113 Notifications dummy
def format_provider_governance_report_message(review): pass
def format_data_lineage_warning_message(graph): pass
def format_audit_trail_warning_message(manifest): pass
def notifications_from_provider_governance_review(review): pass


from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import (
    MarketBehaviorFullReview, BehaviorReportQaRuleResult, MarketBehaviorProfile
)

def format_market_behavior_report_message(review: MarketBehaviorFullReview) -> NotificationMessage:
    return NotificationMessage(
        title=f"Market Behavior Report: {review.review_id}",
        body=f"Ready for Phase 131: {review.readiness_gate.ready_for_phase131 if review.readiness_gate else False}",
        type="MARKET_BEHAVIOR_REPORT"
    )

def format_behavior_report_qa_warning_message(results: list[BehaviorReportQaRuleResult]) -> NotificationMessage:
    return NotificationMessage(
        title="Behavior Report QA Warning",
        body=f"Failed rules: {len([r for r in results if not r.passed])}",
        type="BEHAVIOR_REPORT_QA_WARNING"
    )

def format_market_behavior_profile_warning_message(profiles: list[MarketBehaviorProfile]) -> NotificationMessage:
    return NotificationMessage(
        title="Market Behavior Profile Warning",
        body=f"Profiles with warnings/errors: {len([p for p in profiles if p.errors or p.warnings])}",
        type="MARKET_BEHAVIOR_PROFILE_WARNING"
    )

def notifications_from_market_behavior_review(review: MarketBehaviorFullReview) -> list[NotificationMessage]:
    msgs = [format_market_behavior_report_message(review)]
    if review.qa_results and not all(r.passed for r in review.qa_results):
        msgs.append(format_behavior_report_qa_warning_message(review.qa_results))
    if any(p.errors or p.warnings for p in review.behavior_profiles):
        msgs.append(format_market_behavior_profile_warning_message(review.behavior_profiles))
    return msgs

def format_regime_alignment_report_message(review: Any) -> NotificationMessage:
    return NotificationMessage(text="Regime alignment report")
def format_compatibility_warning_message(results: Any) -> NotificationMessage:
    return NotificationMessage(text="Compatibility warning")
def format_behavior_overlay_warning_message(results: Any) -> NotificationMessage:
    return NotificationMessage(text="Overlay warning")
def notifications_from_regime_alignment_review(review: Any) -> list[NotificationMessage]:
    return [format_regime_alignment_report_message(review)]
