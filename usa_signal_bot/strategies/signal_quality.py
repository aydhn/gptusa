"""Signal quality guard system."""

import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import uuid

from usa_signal_bot.core.enums import SignalQualityStatus, SignalRejectionReason, SignalLifecycleStatus
from usa_signal_bot.core.config_schema import SignalQualityConfig
from usa_signal_bot.strategies.signal_contract import StrategySignal
from usa_signal_bot.strategies.signal_scoring import SignalScoringResult
from usa_signal_bot.core.exceptions import SignalQualityGuardError

@dataclass
class SignalQualityRuleResult:
    rule_name: str
    passed: bool
    status: SignalQualityStatus
    rejection_reason: Optional[SignalRejectionReason] = None
    message: str = ""
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SignalQualityReport:
    report_id: str
    created_at_utc: str
    total_signals: int
    accepted_count: int
    rejected_count: int
    warning_count: int
    needs_review_count: int
    rule_results: List[SignalQualityRuleResult]
    accepted_signal_ids: List[str]
    rejected_signal_ids: List[str]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def evaluate_signal_quality(
    signal: StrategySignal,
    scoring_result: Optional[SignalScoringResult] = None,
    config: Optional[SignalQualityConfig] = None
) -> List[SignalQualityRuleResult]:

    if config is None:
        config = SignalQualityConfig()

    results = []

    # 1. Reject missing reasons
    if config.reject_missing_reasons:
        results.append(reject_missing_reasons(signal))

    # 2. Reject missing feature snapshot
    if config.reject_missing_feature_snapshot:
        results.append(reject_missing_feature_snapshot(signal))

    # 3. Reject expired signals
    if config.reject_expired_signals:
        results.append(reject_expired_signal(signal))

    # 4. Low confidence
    results.append(reject_low_confidence(signal, config.min_confidence_for_review))

    # 5. Low score (if scored)
    if scoring_result is not None:
        results.append(reject_low_score(scoring_result, config.min_score_for_review))

    # 6. Overconfidence warning
    if signal.confidence >= config.overconfidence_warning_threshold:
        results.append(SignalQualityRuleResult(
            rule_name="overconfidence_check",
            passed=True,
            status=SignalQualityStatus.WARNING,
            message="High confidence without backtest validation."
        ))

    return results

def evaluate_signal_quality_list(
    signals: List[StrategySignal],
    scoring_results: Optional[List[SignalScoringResult]] = None,
    config: Optional[SignalQualityConfig] = None
) -> SignalQualityReport:

    if config is None:
        config = SignalQualityConfig()

    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    report = SignalQualityReport(
        report_id=f"quality_{uuid.uuid4().hex[:8]}",
        created_at_utc=now_utc,
        total_signals=len(signals),
        accepted_count=0,
        rejected_count=0,
        warning_count=0,
        needs_review_count=0,
        rule_results=[],
        accepted_signal_ids=[],
        rejected_signal_ids=[],
        warnings=[],
        errors=[]
    )

    if not signals and not config.allow_empty_signal_list:
        report.warnings.append("Empty signal list provided.")
        return report

    score_map = {res.original_signal.signal_id: res for res in scoring_results} if scoring_results else {}

    for signal in signals:
        scoring_res = score_map.get(signal.signal_id)

        try:
            rule_results = evaluate_signal_quality(signal, scoring_res, config)
            report.rule_results.extend(rule_results)

            is_rejected = any(r.status == SignalQualityStatus.REJECTED for r in rule_results)
            needs_review = any(r.status == SignalQualityStatus.NEEDS_REVIEW for r in rule_results)
            has_warning = any(r.status == SignalQualityStatus.WARNING for r in rule_results)

            if is_rejected:
                signal.quality_status = SignalQualityStatus.REJECTED
                signal.lifecycle_status = SignalLifecycleStatus.REJECTED
                report.rejected_count += 1
                report.rejected_signal_ids.append(signal.signal_id)
            elif needs_review:
                signal.quality_status = SignalQualityStatus.NEEDS_REVIEW
                report.needs_review_count += 1
                report.accepted_signal_ids.append(signal.signal_id) # Still tracked, but needs review
            elif has_warning:
                signal.quality_status = SignalQualityStatus.WARNING
                report.warning_count += 1
                report.accepted_signal_ids.append(signal.signal_id)
                report.accepted_count += 1
            else:
                signal.quality_status = SignalQualityStatus.ACCEPTED
                report.accepted_count += 1
                report.accepted_signal_ids.append(signal.signal_id)

        except Exception as e:
            report.errors.append(f"Quality evaluation failed for {signal.signal_id}: {str(e)}")

    if len(signals) > 0 and report.rejected_count / len(signals) >= config.max_rejected_ratio_warning:
        report.warnings.append(f"High rejection ratio: {report.rejected_count}/{len(signals)} signals rejected.")

    return report

def reject_low_confidence(signal: StrategySignal, min_confidence: float) -> SignalQualityRuleResult:
    if signal.confidence < min_confidence:
        return SignalQualityRuleResult(
            rule_name="minimum_confidence",
            passed=False,
            status=SignalQualityStatus.REJECTED,
            rejection_reason=SignalRejectionReason.LOW_CONFIDENCE,
            message=f"Confidence {signal.confidence} is below minimum {min_confidence}"
        )
    return SignalQualityRuleResult(
        rule_name="minimum_confidence",
        passed=True,
        status=SignalQualityStatus.ACCEPTED,
        message="Confidence is acceptable"
    )

def reject_low_score(scoring_result: SignalScoringResult, min_score: float) -> SignalQualityRuleResult:
    if not scoring_result.accepted_for_review or scoring_result.scored_signal.score < min_score:
        return SignalQualityRuleResult(
            rule_name="minimum_score",
            passed=False,
            status=SignalQualityStatus.REJECTED,
            rejection_reason=SignalRejectionReason.LOW_SCORE,
            message=f"Score {scoring_result.scored_signal.score} is below minimum {min_score}"
        )
    return SignalQualityRuleResult(
        rule_name="minimum_score",
        passed=True,
        status=SignalQualityStatus.ACCEPTED,
        message="Score is acceptable"
    )

def reject_missing_reasons(signal: StrategySignal) -> SignalQualityRuleResult:
    if not signal.reasons:
        return SignalQualityRuleResult(
            rule_name="missing_reasons",
            passed=False,
            status=SignalQualityStatus.REJECTED,
            rejection_reason=SignalRejectionReason.MISSING_REASONS,
            message="Signal has no reasons provided"
        )
    return SignalQualityRuleResult(
        rule_name="missing_reasons",
        passed=True,
        status=SignalQualityStatus.ACCEPTED,
        message="Signal has reasons"
    )

def reject_missing_feature_snapshot(signal: StrategySignal) -> SignalQualityRuleResult:
    if not signal.feature_snapshot:
        return SignalQualityRuleResult(
            rule_name="missing_feature_snapshot",
            passed=False,
            status=SignalQualityStatus.REJECTED,
            rejection_reason=SignalRejectionReason.MISSING_FEATURE_SNAPSHOT,
            message="Signal has no feature snapshot"
        )
    return SignalQualityRuleResult(
        rule_name="missing_feature_snapshot",
        passed=True,
        status=SignalQualityStatus.ACCEPTED,
        message="Signal has feature snapshot"
    )

def reject_expired_signal(signal: StrategySignal, now_utc: Optional[str] = None) -> SignalQualityRuleResult:
    if not signal.expires_at_utc:
        return SignalQualityRuleResult(
            rule_name="expired_signal",
            passed=True,
            status=SignalQualityStatus.ACCEPTED,
            message="Signal does not expire"
        )

    if now_utc is None:
        now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

    if signal.expires_at_utc < now_utc:
        return SignalQualityRuleResult(
            rule_name="expired_signal",
            passed=False,
            status=SignalQualityStatus.REJECTED,
            rejection_reason=SignalRejectionReason.EXPIRED_SIGNAL,
            message=f"Signal expired at {signal.expires_at_utc}"
        )
    return SignalQualityRuleResult(
        rule_name="expired_signal",
        passed=True,
        status=SignalQualityStatus.ACCEPTED,
        message="Signal is not expired"
    )

def quality_report_to_text(report: SignalQualityReport) -> str:
    lines = [
        f"--- Signal Quality Report: {report.report_id} ---",
        f"Time: {report.created_at_utc}",
        f"Total Signals: {report.total_signals}",
        f"Accepted: {report.accepted_count}",
        f"Rejected: {report.rejected_count}",
        f"Warnings: {report.warning_count}",
        f"Needs Review: {report.needs_review_count}",
    ]
    if report.warnings:
        lines.append("Report Warnings:")
        for w in report.warnings:
            lines.append(f"  - {w}")
    if report.errors:
        lines.append("Report Errors:")
        for e in report.errors:
            lines.append(f"  - {e}")
    return "\n".join(lines)

def assert_signal_quality_acceptable(report: SignalQualityReport, allow_warnings: bool = True) -> None:
    if report.errors:
        raise SignalQualityGuardError(f"Quality report contains errors: {report.errors}")
    if not allow_warnings and report.warnings:
        raise SignalQualityGuardError(f"Quality report contains warnings: {report.warnings}")
