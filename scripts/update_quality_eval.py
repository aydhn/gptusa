import re

def update_quality_evaluator():
    with open('usa_signal_bot/quality/data_quality_evaluator.py', 'r') as f:
        content = f.read()

    new_eval_func = """
def score_regime_aware_execution_quality(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    issues = []
    regime_data = artifacts.get("regime_costs", {})
    if not regime_data:
        issues.append(QualityIssue(
            issue_id=create_quality_issue_id(),
            dimension=QualityDimension.EXECUTION,
            severity=QualitySeverity.LOW,
            status=QualityStatus.WARN,
            title="Missing Regime Cost Data",
            message="No regime-aware cost snapshots found in artifacts. Score penalized."
        ))
        return 50.0, issues

    blocked = regime_data.get("blocked_count", 0)
    high_risk = regime_data.get("high_risk_count", 0)

    score = 100.0
    if blocked > 0:
        score -= 20.0
        issues.append(QualityIssue(
            issue_id=create_quality_issue_id(),
            dimension=QualityDimension.EXECUTION,
            severity=QualitySeverity.HIGH,
            status=QualityStatus.WARN,
            title="Blocked Regimes Detected",
            message=f"{blocked} symbols blocked by regime cost checks."
        ))
    if high_risk > 0:
        score -= 10.0

    return max(0.0, score), issues
"""
    if "score_regime_aware_execution_quality" not in content:
        content += new_eval_func
        with open('usa_signal_bot/quality/data_quality_evaluator.py', 'w') as f:
            f.write(content)

update_quality_evaluator()
