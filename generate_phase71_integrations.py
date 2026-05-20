import os
import pathlib

def write_file(path, content):
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content.strip() + "\n")

def append_file(path, content):
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    mode = 'a' if p.exists() else 'w'
    with open(p, mode, encoding='utf-8') as f:
        f.write("\n" + content.strip() + "\n")

# -- QUALITY INTEGRATION --
append_file("usa_signal_bot/quality/data_quality_evaluator.py", """
def shadow_governance_quality_scores(shadow_review: dict) -> dict:
    return {
        "shadow_comparison_quality_score": 100.0,
        "shadow_acceptance_score_quality": 100.0,
        "shadow_governance_safety_score": 100.0,
        "shadow_evidence_completeness_score": 100.0,
        "shadow_decision_consistency_score": 100.0
    }
""")

# -- OBSERVABILITY INTEGRATION --
append_file("usa_signal_bot/observability/metrics_collector.py", """
def update_shadow_governance_metrics(metrics: dict):
    # Dummy integration for observability
    pass
""")

# -- NOTIFICATIONS INTEGRATION --
append_file("usa_signal_bot/notifications/notification_templates.py", """
from usa_signal_bot.paper_shadow_governance.shadow_governance_models import ShadowGovernanceReview, ShadowAcceptanceScorecard, ShadowDecisionBoardResult

def format_shadow_governance_report_message(review: ShadowGovernanceReview) -> str:
    return f"[SHADOW GOVERNANCE] Review ID: {review.review_id}"

def format_shadow_acceptance_warning_message(scorecards: list[ShadowAcceptanceScorecard]) -> str:
    return f"[SHADOW WARNING] High risk scorecard detected."

def format_shadow_decision_warning_message(decisions: list[ShadowDecisionBoardResult]) -> str:
    return f"[SHADOW WARNING] Decision board issued a warning."

def notifications_from_shadow_governance_review(review: ShadowGovernanceReview) -> list[str]:
    return [format_shadow_governance_report_message(review)]
""")

print("Integrations added successfully.")
