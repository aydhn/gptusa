from datetime import datetime, timezone
from typing import Any
import copy

from usa_signal_bot.core.enums import (
    RiskDecisionStatus,
    RiskRunStatus,
    RiskCheckStatus,
    RiskSeverity,
    RiskRejectionReason
)
from usa_signal_bot.risk.risk_models import (
    RiskDecision,
    RiskRunResult,
    RiskCheckResult,
    PositionSizingResult,
    create_risk_decision_id,
    create_risk_run_id
)
from usa_signal_bot.risk.risk_limits import RiskLimitConfig, default_risk_limit_config, check_short_allowed
from usa_signal_bot.risk.position_sizing import PositionSizingConfig, default_position_sizing_config, calculate_position_size
from usa_signal_bot.risk.exposure_guard import ExposureSnapshot, evaluate_exposure_for_candidate, update_exposure_snapshot_with_decision
from usa_signal_bot.risk.candidate_risk import (
    CandidateRiskInput,
    build_position_sizing_request,
    validate_candidate_risk_input,
    candidate_risk_input_from_signal,
    candidate_risk_input_from_selected_candidate
)

class RiskEngine:
    def __init__(self, risk_limit_config: RiskLimitConfig | None = None, sizing_config: PositionSizingConfig | None = None):
        self.risk_limit_config = risk_limit_config or default_risk_limit_config()
        self.sizing_config = sizing_config or default_position_sizing_config()

    def evaluate_candidate(self, candidate: CandidateRiskInput, snapshot: ExposureSnapshot) -> RiskDecision:
        checks = validate_candidate_risk_input(candidate)
        failed_checks = [c for c in checks if c.status == RiskCheckStatus.FAILED]

        if failed_checks:
            sizing_result = PositionSizingResult(
                candidate_id=candidate.candidate_id, method=self.sizing_config.method,
                approved_quantity=0.0, approved_notional=0.0, raw_quantity=0.0, raw_notional=0.0,
                capped=False, cap_reasons=[], warnings=[], errors=[]
            )
            return self.build_decision(candidate, sizing_result, checks)

        short_check = check_short_allowed(candidate.action, self.risk_limit_config)
        checks.append(short_check)
        if short_check.status == RiskCheckStatus.FAILED:
            sizing_result = PositionSizingResult(
                candidate_id=candidate.candidate_id, method=self.sizing_config.method,
                approved_quantity=0.0, approved_notional=0.0, raw_quantity=0.0, raw_notional=0.0,
                capped=False, cap_reasons=[], warnings=[], errors=[]
            )
            return self.build_decision(candidate, sizing_result, checks)

        request = build_position_sizing_request(candidate, snapshot)
        sizing_result = calculate_position_size(request, self.sizing_config)

        exposure_res = evaluate_exposure_for_candidate(request, sizing_result, snapshot, self.risk_limit_config)
        checks.extend(exposure_res.checks)

        if self.risk_limit_config.max_candidate_risk_score > 0 and getattr(candidate, "rank_score", None) is not None:
             if candidate.rank_score < (100 - self.risk_limit_config.max_candidate_risk_score):
                 checks.append(RiskCheckResult("low_rank_score", RiskCheckStatus.WARNING, RiskSeverity.MODERATE, "Low rank score", RiskRejectionReason.LOW_RANK_SCORE))

        if candidate.risk_flags:
            checks.append(RiskCheckResult("high_risk_flags", RiskCheckStatus.WARNING, RiskSeverity.HIGH, "Candidate has risk flags", RiskRejectionReason.HIGH_RISK_FLAGS))

        return self.build_decision(candidate, sizing_result, checks)

    def evaluate_candidates(self, candidates: list[CandidateRiskInput], snapshot: ExposureSnapshot, update_snapshot: bool = True) -> RiskRunResult:
        run_id = create_risk_run_id()
        current_snapshot = copy.deepcopy(snapshot)
        decisions = []

        for cand in candidates:
            dec = self.evaluate_candidate(cand, current_snapshot)
            decisions.append(dec)
            if update_snapshot and dec.status in [RiskDecisionStatus.APPROVED, RiskDecisionStatus.REDUCED]:
                current_snapshot = update_exposure_snapshot_with_decision(current_snapshot, dec)

        approved = sum(1 for d in decisions if d.status == RiskDecisionStatus.APPROVED)
        rejected = sum(1 for d in decisions if d.status == RiskDecisionStatus.REJECTED)
        reduced = sum(1 for d in decisions if d.status == RiskDecisionStatus.REDUCED)
        needs_review = sum(1 for d in decisions if d.status == RiskDecisionStatus.NEEDS_REVIEW)

        status = RiskRunStatus.COMPLETED if decisions else RiskRunStatus.EMPTY

        return RiskRunResult(
            run_id=run_id,
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            status=status,
            total_candidates=len(candidates),
            approved_count=approved,
            rejected_count=rejected,
            reduced_count=reduced,
            needs_review_count=needs_review,
            decisions=decisions,
            warnings=[],
            errors=[]
        )

    def evaluate_signal(self, signal: Any, snapshot: ExposureSnapshot) -> RiskDecision:
        cand = candidate_risk_input_from_signal(signal)
        return self.evaluate_candidate(cand, snapshot)

    def evaluate_selected_candidate(self, candidate: Any, snapshot: ExposureSnapshot) -> RiskDecision:
        cand = candidate_risk_input_from_selected_candidate(candidate)
        return self.evaluate_candidate(cand, snapshot)

    def size_candidate(self, candidate: CandidateRiskInput, snapshot: ExposureSnapshot) -> PositionSizingResult:
        request = build_position_sizing_request(candidate, snapshot)
        return calculate_position_size(request, self.sizing_config)

    def calculate_risk_score(self, checks: list[RiskCheckResult], candidate: CandidateRiskInput) -> float:
        score = 0.0
        for c in checks:
            if c.severity == RiskSeverity.CRITICAL:
                score += 50
            elif c.severity == RiskSeverity.HIGH:
                score += 25
            elif c.severity == RiskSeverity.MODERATE:
                score += 10
        if candidate.risk_flags:
            score += 20
        return min(100.0, score)

    def decide_status(self, checks: list[RiskCheckResult], sizing_result: PositionSizingResult) -> RiskDecisionStatus:
        if any(c.status == RiskCheckStatus.FAILED for c in checks):
            return RiskDecisionStatus.REJECTED

        if any(c.rejection_reason == RiskRejectionReason.HIGH_RISK_FLAGS for c in checks):
            return RiskDecisionStatus.NEEDS_REVIEW

        if sizing_result.capped:
            return RiskDecisionStatus.REDUCED

        return RiskDecisionStatus.APPROVED

    def build_decision(self, candidate: CandidateRiskInput, sizing_result: PositionSizingResult, checks: list[RiskCheckResult]) -> RiskDecision:
        status = self.decide_status(checks, sizing_result)
        reasons = [c.rejection_reason for c in checks if c.rejection_reason is not None]

        unique_reasons = []
        for r in reasons:
            if r not in unique_reasons:
                unique_reasons.append(r)

        score = self.calculate_risk_score(checks, candidate)

        sev = RiskSeverity.INFO
        if score > 75:
            sev = RiskSeverity.CRITICAL
        elif score > 50:
            sev = RiskSeverity.HIGH
        elif score > 25:
            sev = RiskSeverity.MODERATE

        return RiskDecision(
            decision_id=create_risk_decision_id(candidate.candidate_id, candidate.symbol),
            candidate_id=candidate.candidate_id,
            signal_id=candidate.signal_id,
            symbol=candidate.symbol,
            strategy_name=candidate.strategy_name,
            timeframe=candidate.timeframe,
            status=status,
            action=candidate.action,
            approved_quantity=sizing_result.approved_quantity if status != RiskDecisionStatus.REJECTED else 0.0,
            approved_notional=sizing_result.approved_notional if status != RiskDecisionStatus.REJECTED else 0.0,
            sizing_method=sizing_result.method,
            checks=checks,
            rejection_reasons=unique_reasons,
            risk_score=score,
            severity=sev,
            notes=sizing_result.cap_reasons + sizing_result.warnings,
            created_at_utc=datetime.now(timezone.utc).isoformat()
        )
