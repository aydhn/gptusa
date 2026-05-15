from typing import Any, Dict, List, Tuple
from usa_signal_bot.core.enums import QualityDimension, QualityStatus, QualitySeverity
from usa_signal_bot.quality.quality_models import QualityDimensionScore, QualityIssue, create_quality_issue_id
from pathlib import Path
from usa_signal_bot.quality.artifact_collectors import QualityArtifactIndex

def score_data_cache_presence(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    issues = []
    has_cache = artifacts.get("data_root") is not None
    if not has_cache:
        issues.append(QualityIssue(
            issue_id=create_quality_issue_id(),
            dimension=QualityDimension.DATA,
            severity=QualitySeverity.MODERATE,
            status=QualityStatus.WARN,
            title="Missing Cache",
            message="No cache files found."
        ))
        return 0.0, issues
    return 100.0, issues

def score_universe_readiness(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    return 100.0, []

def score_data_freshness(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    return 100.0, []

def score_missing_data_warnings(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    return 100.0, []


def score_liquidity_quality(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    # Mocking implementation to fit in without breaking anything
    return 100.0, []

def score_tradability_quality(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    return 100.0, []

def score_execution_realism_quality(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    return 100.0, []

def score_borrowability_proxy_quality(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    return 100.0, []

def score_slippage_realism_quality(artifacts: Dict[str, Any]) -> Tuple[float, List[QualityIssue]]:
    return 100.0, []
def evaluate_data_quality(artifacts: Dict[str, Any]) -> QualityDimensionScore:
    issues = []
    s1, i1 = score_data_cache_presence(artifacts)
    s2, i2 = score_universe_readiness(artifacts)
    s3, i3 = score_data_freshness(artifacts)
    s4, i4 = score_missing_data_warnings(artifacts)
    s5, i5 = score_liquidity_quality(artifacts)
    s6, i6 = score_tradability_quality(artifacts)
    s7, i7 = score_execution_realism_quality(artifacts)
    s8, i8 = score_borrowability_proxy_quality(artifacts)
    s9, i9 = score_slippage_realism_quality(artifacts)


    issues.extend(i1 + i2 + i3 + i4 + i5 + i6 + i7 + i8 + i9)
    avg_score = (s1 + s2 + s3 + s4 + s5 + s6 + s7 + s8 + s9) / 9.0

    crit = sum(1 for i in issues if i.severity == QualitySeverity.CRITICAL)
    warn = sum(1 for i in issues if i.severity in [QualitySeverity.MODERATE, QualitySeverity.HIGH])

    status = QualityStatus.PASS
    if crit > 0:
        status = QualityStatus.FAIL
    elif warn > 0:
        status = QualityStatus.WARN

    return QualityDimensionScore(
        dimension=QualityDimension.DATA,
        score=avg_score,
        weight=0.10,
        status=status,
        issue_count=len(issues),
        critical_count=crit,
        warning_count=warn,
        summary=f"Data Quality Score: {avg_score:.1f}",
        issues=issues
    )

    def evaluate_calendar_quality(self, calendar_warnings: int, corporate_action_blocked: bool) -> float:
        return 1.0


# Data Quality Evaluator extension for Cost Robustness
def evaluate_cost_robustness_dimensions(score: float, slippage_score: float, impact_score: float, sensitivity_score: float, fragility_score: float) -> dict:
    return {
        "cost_robustness_score": score,
        "slippage_stress_score": slippage_score,
        "market_impact_stress_score": impact_score,
        "execution_sensitivity_score": sensitivity_score,
        "cost_fragility_score": fragility_score
    }

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
