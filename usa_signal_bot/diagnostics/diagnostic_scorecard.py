from typing import Any, Dict, List
from usa_signal_bot.diagnostics.diagnostic_models import (
    DiagnosticEvent, FailureModeAssessment, FailureCluster, StrategyDiagnosticResult,
    DiagnosticScorecard, create_diagnostic_scorecard_id
)
from usa_signal_bot.core.enums import DiagnosticStatus, DiagnosticEvidenceQuality
from datetime import datetime, timezone

def calculate_failure_rate(events: List[DiagnosticEvent]) -> float:
    if not events:
        return 0.0
    failures = [e for e in events if e.net_pnl_usd is not None and e.net_pnl_usd < 0]
    return (len(failures) / len(events)) * 100

def calculate_high_severity_ratio(assessments: List[FailureModeAssessment]) -> float:
    if not assessments:
        return 0.0
    high_sev = [a for a in assessments if a.severity.value in ["HIGH", "CRITICAL"]]
    return (len(high_sev) / len(assessments)) * 100

def calculate_diagnostics_quality_score(events: List[DiagnosticEvent], assessments: List[FailureModeAssessment]) -> float:
    score = 100.0
    if len(events) < 50:
        score -= 20.0

    noisy = [a for a in assessments if a.evidence_quality == DiagnosticEvidenceQuality.NOISY]
    if noisy:
        score -= (len(noisy) * 5)

    return max(0.0, score)

def classify_overall_diagnostic_status(scorecard: DiagnosticScorecard) -> DiagnosticStatus:
    components = scorecard.score_components
    failure_rate = components.get("failure_rate", 0) or 0
    high_severity_ratio = components.get("high_severity_ratio", 0) or 0

    if scorecard.total_event_count < 10:
        return DiagnosticStatus.INSUFFICIENT_DATA

    if failure_rate > 60 or high_severity_ratio > 30 or scorecard.critical_severity_count > 0:
        return DiagnosticStatus.FAILING
    elif failure_rate > 40 or high_severity_ratio > 10 or scorecard.degraded_strategy_count > 0:
        return DiagnosticStatus.DEGRADED

    return DiagnosticStatus.HEALTHY

def build_diagnostic_scorecard(events: List[DiagnosticEvent], assessments: List[FailureModeAssessment], clusters: List[FailureCluster], strategy_results: List[StrategyDiagnosticResult]) -> DiagnosticScorecard:
    fail_rate = calculate_failure_rate(events)
    high_sev_ratio = calculate_high_severity_ratio(assessments)
    qual_score = calculate_diagnostics_quality_score(events, assessments)

    high_sev_count = len([a for a in assessments if a.severity.value == "HIGH"])
    crit_sev_count = len([a for a in assessments if a.severity.value == "CRITICAL"])
    deg_strat_count = len([s for s in strategy_results if s.status.value in ["DEGRADED", "FAILING"]])
    noisy_count = len([a for a in assessments if a.evidence_quality == DiagnosticEvidenceQuality.NOISY])

    scorecard = DiagnosticScorecard(
        scorecard_id=create_diagnostic_scorecard_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        diagnostic_status=DiagnosticStatus.UNKNOWN,
        total_event_count=len(events),
        total_failure_count=len([e for e in events if e.net_pnl_usd is not None and e.net_pnl_usd < 0]),
        high_severity_count=high_sev_count,
        critical_severity_count=crit_sev_count,
        degraded_strategy_count=deg_strat_count,
        noisy_evidence_count=noisy_count,
        score_components={
            "failure_rate": fail_rate,
            "high_severity_ratio": high_sev_ratio,
            "quality_score": qual_score
        }
    )
    scorecard.diagnostic_status = classify_overall_diagnostic_status(scorecard)
    return scorecard

def diagnostic_scorecard_to_text(scorecard: DiagnosticScorecard) -> str:
    lines = [
        "Diagnostic Scorecard:",
        f"  Overall Status: {scorecard.diagnostic_status.value}",
        f"  Events Analyzed: {scorecard.total_event_count}",
        f"  Total Failures: {scorecard.total_failure_count}",
        f"  High Severity Failures: {scorecard.high_severity_count}",
        f"  Critical Severity Failures: {scorecard.critical_severity_count}",
        f"  Degraded Strategies: {scorecard.degraded_strategy_count}",
        f"  Quality Score: {scorecard.score_components.get('quality_score')}"
    ]
    return "\n".join(lines)
