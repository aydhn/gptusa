import re

def update_quality_evaluator():
    with open('usa_signal_bot/quality/data_quality_evaluator.py', 'r') as f:
        content = f.read()

    new_eval_func = """
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
"""
    if "score_pre_paper_handoff_freeze_quality" not in content:
        content += new_eval_func
        with open('usa_signal_bot/quality/data_quality_evaluator.py', 'w') as f:
            f.write(content)

update_quality_evaluator()
