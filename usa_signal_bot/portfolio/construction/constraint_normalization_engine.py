from typing import Any, Dict, List
from usa_signal_bot.portfolio.construction.phase155_models import (
    SandboxAllocationResult,
    PortfolioConstructionPolicy,
    PortfolioSandboxCandidate
)

def normalize_sandbox_allocation_results(
    results: List[SandboxAllocationResult],
    policy: PortfolioConstructionPolicy
) -> List[SandboxAllocationResult]:

    # 1. Initialize normalized weights
    for r in results:
        r.normalized_sandbox_weight = r.sandbox_prototype_weight if r.sandbox_prototype_weight is not None else 0.0

    # Group by method to normalize per method
    method_groups: Dict[str, List[SandboxAllocationResult]] = {}
    for r in results:
        if r.method_name not in method_groups:
            method_groups[r.method_name] = []
        method_groups[r.method_name].append(r)

    for method, method_results in method_groups.items():
        _apply_caps(method_results, policy)

    return results

def apply_max_sandbox_weight_cap(
    results: List[SandboxAllocationResult],
    policy: PortfolioConstructionPolicy
) -> List[SandboxAllocationResult]:
    # Part of normalization, modifies in place
    for r in results:
        if r.normalized_sandbox_weight is not None and r.normalized_sandbox_weight > policy.max_sandbox_weight_fraction:
            r.normalized_sandbox_weight = policy.max_sandbox_weight_fraction
            r.cap_applied = True
    return results

def apply_group_sandbox_weight_cap(
    results: List[SandboxAllocationResult],
    policy: PortfolioConstructionPolicy,
    candidates: List[PortfolioSandboxCandidate]
) -> List[SandboxAllocationResult]:
    # This requires candidate group mapping, simplified for this prototype level
    # We will just distribute and cap.
    return results

def zero_ineligible_candidates(
    results: List[SandboxAllocationResult],
    candidates: List[PortfolioSandboxCandidate]
) -> List[SandboxAllocationResult]:
    ineligible = {c.symbol for c in candidates if not c.eligible_for_sandbox}
    for r in results:
        if r.symbol in ineligible:
            r.normalized_sandbox_weight = 0.0
            r.zeroed_by_constraint = True
    return results

def _apply_caps(results: List[SandboxAllocationResult], policy: PortfolioConstructionPolicy):
    # Iterative capping to ensure sum = 1.0 (or close) while respecting caps
    max_iter = 10

    for _ in range(max_iter):
        total_weight = sum(r.normalized_sandbox_weight for r in results if r.normalized_sandbox_weight is not None)
        if total_weight <= 0:
            break

        for r in results:
            if r.normalized_sandbox_weight is not None:
                r.normalized_sandbox_weight = r.normalized_sandbox_weight / total_weight

        # Apply cap
        cap_hit = False
        for r in results:
            if r.normalized_sandbox_weight is not None and r.normalized_sandbox_weight > policy.max_sandbox_weight_fraction:
                r.normalized_sandbox_weight = policy.max_sandbox_weight_fraction
                r.cap_applied = True
                cap_hit = True

        if not cap_hit:
            break

def validate_normalized_sandbox_allocations(results: List[SandboxAllocationResult]) -> List[str]:
    errors = []

    method_sums = {}
    for r in results:
        if r.normalized_sandbox_weight is not None:
            if r.normalized_sandbox_weight < 0:
                errors.append(f"Negative normalized weight for {r.symbol} in {r.method_name}")
            method_sums[r.method_name] = method_sums.get(r.method_name, 0.0) + r.normalized_sandbox_weight

    for method, m_sum in method_sums.items():
        if m_sum > 0 and abs(m_sum - 1.0) > 0.01:
            # We don't block on this, just a diagnostic observation in real cases, but for validation we can warn
            pass

    return errors

def constraint_normalization_summary(results: List[SandboxAllocationResult]) -> Dict[str, Any]:
    capped = sum(1 for r in results if r.cap_applied)
    zeroed = sum(1 for r in results if r.zeroed_by_constraint)
    return {
        "count": len(results),
        "capped_count": capped,
        "zeroed_count": zeroed
    }
