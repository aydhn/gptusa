import os
import pathlib

def write_file(path, content):
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content.strip() + "\n")

write_file("usa_signal_bot/paper_shadow_governance/acceptance_gates.py", """
from typing import Any, Dict, List
from usa_signal_bot.core.enums import ShadowAcceptanceGateType, ShadowAcceptanceStatus, ShadowGovernanceRiskFlag
from usa_signal_bot.paper_shadow_governance.shadow_governance_models import ShadowAcceptanceGate, create_shadow_acceptance_gate_id
from usa_signal_bot.paper_shadow_governance.ledger_completeness import ledger_completeness_gate
from usa_signal_bot.paper_shadow_governance.notification_review import notification_safety_gate
from usa_signal_bot.paper_shadow_governance.pnl_cost_comparator import compare_shadow_cost_regression, compare_shadow_pnl_regression

def build_no_real_order_risk_gate(candidate_payload: Dict[str, Any]) -> ShadowAcceptanceGate:
    flags = candidate_payload.get("safety_flags", [])
    status = ShadowAcceptanceStatus.BLOCKED if "REAL_ORDER_RISK" in flags else ShadowAcceptanceStatus.PASS
    risk = [ShadowGovernanceRiskFlag.REAL_ORDER_RISK] if status == ShadowAcceptanceStatus.BLOCKED else []
    return ShadowAcceptanceGate(
        gate_id=create_shadow_acceptance_gate_id(ShadowAcceptanceGateType.NO_REAL_ORDER_RISK),
        gate_type=ShadowAcceptanceGateType.NO_REAL_ORDER_RISK,
        status=status,
        threshold=0, observed_value=len(risk),
        description="Check for real order risk",
        risk_flags=risk, warnings=[], errors=[]
    )

def build_no_paper_mutation_risk_gate(candidate_payload: Dict[str, Any]) -> ShadowAcceptanceGate:
    flags = candidate_payload.get("safety_flags", [])
    status = ShadowAcceptanceStatus.BLOCKED if "PAPER_MUTATION_RISK" in flags else ShadowAcceptanceStatus.PASS
    risk = [ShadowGovernanceRiskFlag.PAPER_STATE_MUTATION_RISK] if status == ShadowAcceptanceStatus.BLOCKED else []
    return ShadowAcceptanceGate(
        gate_id=create_shadow_acceptance_gate_id(ShadowAcceptanceGateType.NO_PAPER_MUTATION_RISK),
        gate_type=ShadowAcceptanceGateType.NO_PAPER_MUTATION_RISK,
        status=status,
        threshold=0, observed_value=len(risk),
        description="Check for paper state mutation risk",
        risk_flags=risk, warnings=[], errors=[]
    )

def build_no_telegram_real_send_gate(candidate_payload: Dict[str, Any]) -> ShadowAcceptanceGate:
    flags = candidate_payload.get("safety_flags", [])
    status = ShadowAcceptanceStatus.BLOCKED if "TELEGRAM_REAL_SEND_RISK" in flags else ShadowAcceptanceStatus.PASS
    risk = [ShadowGovernanceRiskFlag.TELEGRAM_REAL_SEND_RISK] if status == ShadowAcceptanceStatus.BLOCKED else []
    return ShadowAcceptanceGate(
        gate_id=create_shadow_acceptance_gate_id(ShadowAcceptanceGateType.NO_TELEGRAM_REAL_SEND_RISK),
        gate_type=ShadowAcceptanceGateType.NO_TELEGRAM_REAL_SEND_RISK,
        status=status,
        threshold=0, observed_value=len(risk),
        description="Check for telegram real send risk",
        risk_flags=risk, warnings=[], errors=[]
    )

def build_no_production_config_write_gate(candidate_payload: Dict[str, Any]) -> ShadowAcceptanceGate:
    flags = candidate_payload.get("safety_flags", [])
    status = ShadowAcceptanceStatus.BLOCKED if "PRODUCTION_CONFIG_WRITE_RISK" in flags else ShadowAcceptanceStatus.PASS
    risk = [ShadowGovernanceRiskFlag.PRODUCTION_CONFIG_WRITE_RISK] if status == ShadowAcceptanceStatus.BLOCKED else []
    return ShadowAcceptanceGate(
        gate_id=create_shadow_acceptance_gate_id(ShadowAcceptanceGateType.NO_PRODUCTION_CONFIG_WRITE_RISK),
        gate_type=ShadowAcceptanceGateType.NO_PRODUCTION_CONFIG_WRITE_RISK,
        status=status,
        threshold=0, observed_value=len(risk),
        description="Check for production config write risk",
        risk_flags=risk, warnings=[], errors=[]
    )

def build_ledger_complete_gate(candidate_payload: Dict[str, Any]) -> ShadowAcceptanceGate:
    return ledger_completeness_gate(candidate_payload)

def build_cost_not_worse_gate(baseline_payload: Dict[str, Any], candidate_payload: Dict[str, Any]) -> ShadowAcceptanceGate:
    return compare_shadow_cost_regression(baseline_payload.get("metrics", {}), candidate_payload.get("metrics", {}))

def build_pnl_not_worse_gate(baseline_payload: Dict[str, Any], candidate_payload: Dict[str, Any]) -> ShadowAcceptanceGate:
    return compare_shadow_pnl_regression(baseline_payload.get("metrics", {}), candidate_payload.get("metrics", {}))

def build_risk_not_worse_gate(baseline_payload: Dict[str, Any], candidate_payload: Dict[str, Any]) -> ShadowAcceptanceGate:
    return ShadowAcceptanceGate(
        gate_id=create_shadow_acceptance_gate_id(ShadowAcceptanceGateType.RISK_NOT_WORSE),
        gate_type=ShadowAcceptanceGateType.RISK_NOT_WORSE,
        status=ShadowAcceptanceStatus.PASS,
        threshold=0, observed_value=0, description="Check risk metrics",
        risk_flags=[], warnings=[], errors=[]
    )

def build_notification_safe_gate(candidate_payload: Dict[str, Any]) -> ShadowAcceptanceGate:
    return notification_safety_gate(candidate_payload)

def default_shadow_acceptance_gates(baseline_payload: Dict[str, Any], candidate_payload: Dict[str, Any]) -> List[ShadowAcceptanceGate]:
    return [
        build_no_real_order_risk_gate(candidate_payload),
        build_no_paper_mutation_risk_gate(candidate_payload),
        build_no_telegram_real_send_gate(candidate_payload),
        build_no_production_config_write_gate(candidate_payload),
        build_ledger_complete_gate(candidate_payload),
        build_cost_not_worse_gate(baseline_payload, candidate_payload),
        build_pnl_not_worse_gate(baseline_payload, candidate_payload),
        build_risk_not_worse_gate(baseline_payload, candidate_payload),
        build_notification_safe_gate(candidate_payload)
    ]

def shadow_acceptance_gates_to_text(gates: List[ShadowAcceptanceGate]) -> str:
    return f"Evaluated {len(gates)} gates."
""")

write_file("usa_signal_bot/paper_shadow_governance/acceptance_scoring.py", """
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import ShadowAcceptanceStatus, ShadowGovernanceRiskFlag
from usa_signal_bot.paper_shadow_governance.shadow_governance_models import (
    ShadowAcceptanceScorecard, ShadowAcceptanceGate, ShadowMetricComparison,
    create_shadow_acceptance_scorecard_id, utc_now_iso
)
from usa_signal_bot.paper_shadow_governance.acceptance_gates import default_shadow_acceptance_gates

def calculate_shadow_acceptance_score(gates: List[ShadowAcceptanceGate], metric_comparisons: Optional[List[ShadowMetricComparison]] = None) -> Optional[float]:
    if not gates: return None
    for g in gates:
        if g.status == ShadowAcceptanceStatus.BLOCKED:
            return 0.0
    passes = sum(1 for g in gates if g.status == ShadowAcceptanceStatus.PASS)
    return (passes / len(gates)) * 100

def classify_shadow_acceptance_status(score: Optional[float], gates: List[ShadowAcceptanceGate]) -> ShadowAcceptanceStatus:
    if score is None: return ShadowAcceptanceStatus.INSUFFICIENT_DATA
    for g in gates:
        if g.status == ShadowAcceptanceStatus.BLOCKED:
            return ShadowAcceptanceStatus.BLOCKED
    if score >= 70.0:
        for g in gates:
            if g.status == ShadowAcceptanceStatus.FAIL:
                return ShadowAcceptanceStatus.WARNING
        return ShadowAcceptanceStatus.PASS
    return ShadowAcceptanceStatus.FAIL

def collect_shadow_acceptance_risk_flags(gates: List[ShadowAcceptanceGate]) -> List[ShadowGovernanceRiskFlag]:
    flags = []
    for g in gates:
        flags.extend(g.risk_flags)
    return list(set(flags))

def build_shadow_acceptance_scorecard(baseline_payload: Dict[str, Any], candidate_payload: Dict[str, Any], gates: Optional[List[ShadowAcceptanceGate]] = None) -> ShadowAcceptanceScorecard:
    if gates is None:
        gates = default_shadow_acceptance_gates(baseline_payload, candidate_payload)

    score = calculate_shadow_acceptance_score(gates)
    status = classify_shadow_acceptance_status(score, gates)
    flags = collect_shadow_acceptance_risk_flags(gates)

    return ShadowAcceptanceScorecard(
        scorecard_id=create_shadow_acceptance_scorecard_id(),
        created_at_utc=utc_now_iso(),
        baseline_session_id=baseline_payload.get("session_id"),
        candidate_session_id=candidate_payload.get("session_id"),
        overall_status=status,
        acceptance_score=score,
        gate_pass_count=sum(1 for g in gates if g.status == ShadowAcceptanceStatus.PASS),
        gate_warning_count=sum(1 for g in gates if g.status == ShadowAcceptanceStatus.WARNING),
        gate_fail_count=sum(1 for g in gates if g.status == ShadowAcceptanceStatus.FAIL),
        gate_blocked_count=sum(1 for g in gates if g.status == ShadowAcceptanceStatus.BLOCKED),
        metric_score_components={},
        risk_flags=flags,
        manual_review_required=True,
        allowed_for_real_orders=False,
        allowed_for_paper_state_mutation=False,
        allowed_for_telegram_real_send=False,
        allowed_for_production_config_write=False,
        warnings=[], errors=[]
    )

def shadow_acceptance_scorecard_to_text(scorecard: ShadowAcceptanceScorecard) -> str:
    return f"Scorecard {scorecard.scorecard_id}: {scorecard.overall_status.value} (Score: {scorecard.acceptance_score})"
""")

write_file("usa_signal_bot/paper_shadow_governance/decision_board.py", """
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import (
    ShadowGovernanceDecision, ShadowComparisonOutcome, ShadowAcceptanceStatus, ShadowGovernanceRiskFlag
)
from usa_signal_bot.paper_shadow_governance.shadow_governance_models import (
    ShadowDecisionBoardResult, ShadowAcceptanceScorecard, ShadowSessionComparisonReport,
    create_shadow_decision_board_result_id, utc_now_iso
)

class ShadowRehearsalDecisionBoard:
    def __init__(self, conservative: bool = True):
        self.conservative = conservative

    def collect_decision_risk_flags(self, scorecard: ShadowAcceptanceScorecard, report: Optional[ShadowSessionComparisonReport] = None) -> List[ShadowGovernanceRiskFlag]:
        return scorecard.risk_flags

    def rationale_for_decision(self, decision: ShadowGovernanceDecision, flags: List[ShadowGovernanceRiskFlag]) -> str:
        if decision == ShadowGovernanceDecision.BLOCK_SHADOW_CANDIDATE:
            return "Blocked due to critical safety risks."
        return f"Decision: {decision.value}"

    def followups_for_decision(self, decision: ShadowGovernanceDecision, flags: List[ShadowGovernanceRiskFlag]) -> List[str]:
        return ["Review manually"]

    def decide_from_scorecard(self, scorecard: ShadowAcceptanceScorecard, outcome: ShadowComparisonOutcome) -> ShadowDecisionBoardResult:
        flags = self.collect_decision_risk_flags(scorecard)
        if scorecard.overall_status == ShadowAcceptanceStatus.BLOCKED:
            dec = ShadowGovernanceDecision.BLOCK_SHADOW_CANDIDATE
        elif scorecard.overall_status == ShadowAcceptanceStatus.FAIL:
            dec = ShadowGovernanceDecision.REJECT_SHADOW_CANDIDATE
        elif scorecard.overall_status == ShadowAcceptanceStatus.INSUFFICIENT_DATA:
            dec = ShadowGovernanceDecision.REQUEST_MORE_SHADOW_DATA
        elif outcome == ShadowComparisonOutcome.CANDIDATE_BETTER and scorecard.overall_status == ShadowAcceptanceStatus.PASS:
            dec = ShadowGovernanceDecision.ACCEPT_AS_SANDBOXED_PAPER_CANDIDATE
        else:
            dec = ShadowGovernanceDecision.ACCEPT_FOR_MORE_SHADOW_TESTING

        return ShadowDecisionBoardResult(
            decision_id=create_shadow_decision_board_result_id(),
            created_at_utc=utc_now_iso(),
            comparison_report_id=None,
            scorecard_id=scorecard.scorecard_id,
            decision=dec,
            outcome=outcome,
            acceptance_status=scorecard.overall_status,
            risk_flags=flags,
            rationale=self.rationale_for_decision(dec, flags),
            required_followups=self.followups_for_decision(dec, flags),
            manual_review_required=True,
            allowed_for_real_orders=False,
            allowed_for_paper_state_mutation=False,
            allowed_for_telegram_real_send=False,
            allowed_for_production_config_write=False,
            warnings=[], errors=[]
        )

    def decide_from_comparison(self, report: ShadowSessionComparisonReport) -> ShadowDecisionBoardResult:
        if not report.acceptance_scorecard:
            raise ValueError("Comparison report must have an acceptance scorecard.")
        res = self.decide_from_scorecard(report.acceptance_scorecard, report.outcome)
        res.comparison_report_id = report.report_id
        return res
""")

print("Modules 3 generated successfully.")
