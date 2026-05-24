from typing import Any
from usa_signal_bot.quality.quality_models import QualityScorecard

def evaluate_board_dossier_quality(review: Any) -> QualityScorecard:
    scorecard = QualityScorecard(scorecard_id="qs_1")
    if not review.errors:
        scorecard.paper_readiness_board_dossier_quality_score = 100.0
        scorecard.acceptance_board_seal_score = 100.0
        scorecard.shadow_launch_blocker_score = 100.0
        scorecard.board_dossier_continuity_score = 100.0
        scorecard.board_dossier_non_execution_compliance_score = 100.0
    return scorecard

def score_pre_paper_handoff_freeze_quality(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    issues = []
    handoff_data = artifacts.get("pre_paper_handoff_freeze", {})
    if not handoff_data:
        issues.append(QualityIssue(
            issue_id=create_quality_issue_id(),
            dimension=QualityDimension.GOVERNANCE,
            severity=QualitySeverity.LOW,
            status=QualityStatus.WARN,
            title="Missing Handoff Freeze Data",
            message="No pre_paper_handoff_freeze found in artifacts. Score penalized."
        ))
        return 0.0, issues

    score = 100.0
    if not handoff_data.get("passed", False):
        score = 0.0
        issues.append(QualityIssue(
            issue_id=create_quality_issue_id(),
            dimension=QualityDimension.GOVERNANCE,
            severity=QualitySeverity.HIGH,
            status=QualityStatus.ERROR,
            title="Handoff Freeze Validation Failed",
            message="Pre-paper handoff freeze validation failed."
        ))

    return score, issues

def evaluate_advanced_transition_quality(context: Any) -> QualityScorecard:
    scorecard = QualityScorecard(scorecard_id="qs_advanced_transition")
    if getattr(context, 'activation_allowed', False) or getattr(context, 'active_paper_enabled', False) or getattr(context, 'broker_execution_enabled', False) or getattr(context, 'paper_state_mutation_enabled', False) or getattr(context, 'telegram_real_send_enabled', False) or getattr(context, 'scraping_enabled', False) or getattr(context, 'dashboard_enabled', False):
        scorecard.phase101_non_execution_compliance_score = 0.0
    else:
        scorecard.phase101_non_execution_compliance_score = 100.0
        scorecard.advanced_transition_context_score = 100.0
        scorecard.handoff_freeze_ingestion_score = 100.0
        scorecard.runtime_boundary_score = 100.0
        scorecard.module_inventory_score = 100.0
        scorecard.config_consolidation_score = 100.0
    return scorecard
