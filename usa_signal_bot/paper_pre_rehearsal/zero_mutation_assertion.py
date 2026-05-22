from typing import Any, Dict, List
from usa_signal_bot.paper_pre_rehearsal.paper_baseline_loader import paper_baseline_hash
from usa_signal_bot.core.enums import PrePaperRiskFlag

def compare_paper_baseline_hashes(before: Dict[str, Any], after: Dict[str, Any]) -> Dict[str, Any]:
    hash_before = paper_baseline_hash(before)
    hash_after = paper_baseline_hash(after)
    return {
        "before": hash_before,
        "after": hash_after,
        "match": hash_before == hash_after
    }

def assert_zero_paper_mutation_before_after(before: Dict[str, Any], after: Dict[str, Any]) -> List[str]:
    violations = []
    hashes = compare_paper_baseline_hashes(before, after)
    if not hashes["match"]:
        violations.append(f"Baseline hash mismatch (before: {hashes['before']}, after: {hashes['after']})")

    for key in ["paper_state_committed", "paper_order_executed", "portfolio_state_mutated"]:
        if after.get(key, False):
            violations.append(f"{key} is True in after state")

    return violations

def detect_zero_mutation_violations(payload: Dict[str, Any]) -> List[PrePaperRiskFlag]:
    flags = []
    if payload.get("paper_state_committed", False):
        flags.append(PrePaperRiskFlag.PAPER_STATE_MUTATION_RISK)
    if payload.get("paper_order_executed", False):
        flags.append(PrePaperRiskFlag.PAPER_ORDER_RISK)
    if payload.get("portfolio_state_mutated", False):
        flags.append(PrePaperRiskFlag.PAPER_PORTFOLIO_MUTATION_RISK)
    if payload.get("position_mutated", False):
        flags.append(PrePaperRiskFlag.PAPER_POSITION_MUTATION_RISK)
    if payload.get("cash_mutated", False) or payload.get("equity_mutated", False):
        flags.append(PrePaperRiskFlag.PAPER_CASH_MUTATION_RISK)
    return flags

def zero_mutation_assertion_summary(before: Dict[str, Any], after: Dict[str, Any]) -> Dict[str, Any]:
    violations = assert_zero_paper_mutation_before_after(before, after)
    return {
        "is_zero_mutation": len(violations) == 0,
        "violation_count": len(violations),
        "hash_match": compare_paper_baseline_hashes(before, after)["match"]
    }

def zero_mutation_assertion_to_text(payload: Dict[str, Any]) -> str:
    return f"Zero Mutation: {payload['is_zero_mutation']} ({payload['violation_count']} violations), Hash Match: {payload['hash_match']}"
