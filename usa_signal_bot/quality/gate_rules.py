"""Gate Rule evaluator."""

from typing import Any, Dict, List
from usa_signal_bot.core.enums import QualityDimension, GateRuleOperator, ReadinessGateStatus, QualitySeverity, AcceptanceScope
from usa_signal_bot.quality.quality_models import GateRule, GateRuleResult, ResearchQualityScorecard

def default_gate_rules(scope: AcceptanceScope = AcceptanceScope.FULL_LOCAL_STACK) -> List[GateRule]:
    rules = [
        GateRule(
            rule_id="r_overall_score",
            name="Overall Score >= 70",
            dimension=QualityDimension.OVERALL,
            operator=GateRuleOperator.GTE,
            field_path="overall_score",
            threshold=70.0,
            required=True
        ),
        GateRule(
            rule_id="r_no_critical_issues",
            name="No Critical Issues",
            dimension=QualityDimension.OVERALL,
            operator=GateRuleOperator.EQ,
            field_path="critical_count",
            threshold=0,
            required=True
        ),
        GateRule(
            rule_id="r_data_score",
            name="Data Score >= 50",
            dimension=QualityDimension.DATA,
            operator=GateRuleOperator.GTE,
            field_path="dimensions.data.score",
            threshold=50.0,
            required=True
        ),
        GateRule(
            rule_id="r_backtest_score",
            name="Backtest Score >= 50",
            dimension=QualityDimension.BACKTEST,
            operator=GateRuleOperator.GTE,
            field_path="dimensions.backtest.score",
            threshold=50.0,
            required=True
        ),
        GateRule(
            rule_id="r_risk_score",
            name="Risk Score >= 50",
            dimension=QualityDimension.RISK,
            operator=GateRuleOperator.GTE,
            field_path="dimensions.risk.score",
            threshold=50.0,
            required=True
        )
    ]

    if scope in [AcceptanceScope.LOCAL_PAPER_SIMULATION, AcceptanceScope.FULL_LOCAL_STACK]:
        rules.append(GateRule(
            rule_id="r_paper_score",
            name="Paper Score >= 40",
            dimension=QualityDimension.PAPER,
            operator=GateRuleOperator.GTE,
            field_path="dimensions.paper.score",
            threshold=40.0,
            required=True
        ))

    if scope == AcceptanceScope.FULL_LOCAL_STACK:
        rules.append(GateRule(
            rule_id="r_comparison_score",
            name="Comparison Score >= 40",
            dimension=QualityDimension.COMPARISON,
            operator=GateRuleOperator.GTE,
            field_path="dimensions.comparison.score",
            threshold=40.0,
            required=True
        ))

    return rules

def safe_gate_compare(value: Any, rule: GateRule) -> bool:
    if value is None:
        if rule.operator == GateRuleOperator.EXISTS:
            return False
        return False

    try:
        if rule.operator == GateRuleOperator.EXISTS:
            return True
        elif rule.operator == GateRuleOperator.IS_TRUE:
            return bool(value) is True
        elif rule.operator == GateRuleOperator.IS_FALSE:
            return bool(value) is False
        elif rule.operator == GateRuleOperator.EQ:
            return value == rule.threshold
        elif rule.operator == GateRuleOperator.NEQ:
            return value != rule.threshold
        elif rule.operator == GateRuleOperator.GT:
            return float(value) > float(rule.threshold) # type: ignore
        elif rule.operator == GateRuleOperator.GTE:
            return float(value) >= float(rule.threshold) # type: ignore
        elif rule.operator == GateRuleOperator.LT:
            return float(value) < float(rule.threshold) # type: ignore
        elif rule.operator == GateRuleOperator.LTE:
            return float(value) <= float(rule.threshold) # type: ignore
        elif rule.operator == GateRuleOperator.BETWEEN:
            return float(rule.lower) <= float(value) <= float(rule.upper) # type: ignore
    except (TypeError, ValueError):
        return False

    return False

def get_scorecard_field(scorecard: ResearchQualityScorecard, field_path: str) -> Any:
    if field_path == "overall_score":
        return scorecard.overall_score
    if field_path == "critical_count":
        return sum(1 for i in scorecard.issues if i.severity.name == "CRITICAL")

    parts = field_path.split(".")
    if parts[0] == "dimensions" and len(parts) >= 3:
        dim_name = parts[1].upper()
        field_name = parts[2]

        for d in scorecard.dimensions:
            if d.dimension.name == dim_name:
                return getattr(d, field_name, None)

    return None

def get_artifact_field(artifacts: Dict[str, Any], field_path: str) -> Any:
    return artifacts.get(field_path)

def evaluate_gate_rule(rule: GateRule, scorecard: ResearchQualityScorecard, artifacts: Dict[str, Any]) -> GateRuleResult:
    value = get_scorecard_field(scorecard, rule.field_path)
    if value is None and rule.field_path in artifacts:
        value = artifacts.get(rule.field_path)

    passed = safe_gate_compare(value, rule)
    status = ReadinessGateStatus.PASSED if passed else ReadinessGateStatus.FAILED
    if not passed and not rule.required:
        status = ReadinessGateStatus.WARNING

    return GateRuleResult(
        rule_id=rule.rule_id,
        name=rule.name,
        dimension=rule.dimension,
        status=status,
        observed_value=value,
        message=f"Rule '{rule.name}' evaluated to {passed}. Value: {value}, Threshold: {rule.threshold}",
        severity=rule.severity
    )

def evaluate_gate_rules(rules: List[GateRule], scorecard: ResearchQualityScorecard, artifacts: Dict[str, Any]) -> List[GateRuleResult]:
    return [evaluate_gate_rule(r, scorecard, artifacts) for r in rules if r.enabled]

def gate_rule_results_to_text(results: List[GateRuleResult]) -> str:
    lines = ["--- Gate Rules Results ---"]
    for r in results:
        lines.append(f"[{r.status.name}] {r.name}: {r.observed_value} (Threshold: {r.message})")
    return "\n".join(lines)
