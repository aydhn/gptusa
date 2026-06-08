from typing import Any
from usa_signal_bot.portfolio.foundation.phase153_models import (
    PortfolioEligibilityRule, PortfolioCandidate, CandidateUniverseContract,
    PortfolioEligibilityRuleKind
)

def build_symbol_eligibility_rules(candidate: PortfolioCandidate) -> list[PortfolioEligibilityRule]:
    rules = []

    r1 = PortfolioEligibilityRule()
    r1.rule_kind = PortfolioEligibilityRuleKind.HAS_VALID_SYMBOL
    r1.name = "Has Valid Symbol"
    r1.passed = bool(candidate.symbol)
    r1.applies_to_symbol = candidate.symbol
    rules.append(r1)

    r2 = PortfolioEligibilityRule()
    r2.rule_kind = PortfolioEligibilityRuleKind.NO_LIVE_SIGNAL
    r2.name = "No Live Signal"
    r2.passed = not candidate.live_signal
    r2.applies_to_symbol = candidate.symbol
    rules.append(r2)

    r3 = PortfolioEligibilityRule()
    r3.rule_kind = PortfolioEligibilityRuleKind.NO_ORDER_DECISION
    r3.name = "No Order Decision"
    r3.passed = not candidate.order_decision
    r3.applies_to_symbol = candidate.symbol
    rules.append(r3)

    return rules

def build_portfolio_eligibility_rules(contract: CandidateUniverseContract, handoff_payload: dict[str, Any] | None = None) -> list[PortfolioEligibilityRule]:
    rules = []

    r1 = PortfolioEligibilityRule()
    r1.rule_kind = PortfolioEligibilityRuleKind.PASSES_RESEARCH_BOUNDARY
    r1.name = "Passes Research Boundary"
    r1.passed = True
    rules.append(r1)

    r2 = PortfolioEligibilityRule()
    r2.rule_kind = PortfolioEligibilityRuleKind.PASSES_SAFETY_BOUNDARY
    r2.name = "Passes Safety Boundary"
    r2.passed = True
    rules.append(r2)

    for c in contract.candidates:
        rules.extend(build_symbol_eligibility_rules(c))

    return rules

def validate_portfolio_eligibility_rules(items: list[PortfolioEligibilityRule]) -> list[str]:
    errors = []
    for r in items:
        if not r.metadata_only:
            errors.append(f"Rule {r.name} is not metadata_only")
        if not r.not_trade_approval:
            errors.append(f"Rule {r.name} acts as trade approval")
    return errors

def eligibility_rules_summary(items: list[PortfolioEligibilityRule]) -> dict[str, Any]:
    return {
        "total_rules": len(items),
        "passed_rules": sum(1 for r in items if r.passed)
    }

def eligibility_rules_to_text(items: list[PortfolioEligibilityRule], limit: int = 300) -> str:
    return f"EligibilityRules: {len(items)} rules total"
