from typing import Any, List
from datetime import datetime, timezone
from usa_signal_bot.paper_firewall_audit.firewall_audit_models import ZeroMutationBaseline, ZeroMutationAuditReport, create_zero_mutation_audit_id
from usa_signal_bot.core.enums import ZeroMutationAuditStatus, ZeroMutationAuditDecision, FirewallAuditRiskFlag
from usa_signal_bot.paper_firewall_audit.mutation_invariant_checker import check_zero_mutation_invariants, failed_zero_mutation_invariants, invariant_results_to_risk_flags
from usa_signal_bot.paper_firewall_audit.baseline_hash_comparison import baseline_hash_changed

def run_zero_mutation_audit(before: ZeroMutationBaseline, after: ZeroMutationBaseline) -> ZeroMutationAuditReport:
    invariants = check_zero_mutation_invariants(before, after)
    failed = failed_zero_mutation_invariants(invariants)
    hash_chg = baseline_hash_changed(before, after)
    flags = invariant_results_to_risk_flags(invariants)
    if hash_chg:
        flags.append(FirewallAuditRiskFlag.BASELINE_HASH_CHANGED)

    passed = len(failed) == 0 and not hash_chg

    return ZeroMutationAuditReport(
        audit_id=create_zero_mutation_audit_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        candidate_id=before.candidate_id,
        status=ZeroMutationAuditStatus.PASSED if passed else ZeroMutationAuditStatus.FAILED,
        decision=determine_zero_mutation_decision(failed, flags),
        before_baseline=before,
        after_baseline=after,
        hash_changed=hash_chg,
        mutation_detected=len(failed) > 0,
        invariant_violations=failed,
        risk_flags=flags,
        passed=passed,
        warnings=[],
        errors=[]
    )

def detect_zero_mutation_invariant_violations(before: ZeroMutationBaseline, after: ZeroMutationBaseline) -> List[str]:
    return failed_zero_mutation_invariants(check_zero_mutation_invariants(before, after))

def collect_zero_mutation_risk_flags(before: ZeroMutationBaseline, after: ZeroMutationBaseline) -> List[FirewallAuditRiskFlag]:
    flags = invariant_results_to_risk_flags(check_zero_mutation_invariants(before, after))
    if baseline_hash_changed(before, after):
        flags.append(FirewallAuditRiskFlag.BASELINE_HASH_CHANGED)
    return flags

def determine_zero_mutation_decision(violations: List[str], flags: List[FirewallAuditRiskFlag]) -> ZeroMutationAuditDecision:
    if len(violations) > 0 or len(flags) > 0:
        return ZeroMutationAuditDecision.BLOCK
    return ZeroMutationAuditDecision.PASS_ZERO_MUTATION_AUDIT

def zero_mutation_audit_summary(report: ZeroMutationAuditReport) -> dict[str, Any]:
    return {
        "id": report.audit_id,
        "passed": report.passed,
        "violations": len(report.invariant_violations)
    }

def zero_mutation_audit_to_text(report: ZeroMutationAuditReport) -> str:
    return f"Audit {report.audit_id} passed: {report.passed}"
