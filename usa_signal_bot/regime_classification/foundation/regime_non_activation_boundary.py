from typing import Any, Dict, List
import re

from usa_signal_bot.core.enums import RegimeBoundaryRuleKind, RegimeBoundaryStatus, RegimeFoundationRiskFlag
from usa_signal_bot.regime_classification.foundation.phase126_models import (
    RegimeBoundaryRule,
    RegimeNonActivationBoundaryResult,
    create_regime_boundary_rule_id,
    create_regime_non_activation_boundary_id,
    _now
)
from usa_signal_bot.regime_classification.foundation.market_state_dataset_schema import FORBIDDEN_COLUMNS

def check_safe_columns(columns: List[str]) -> bool:
    for col in columns:
        if col.lower() in FORBIDDEN_COLUMNS:
            return False
    return True

def check_safe_language(text: str) -> bool:
    unsafe_phrases = [
        "kesin al", "kesin sat", "güçlü al", "güçlü sat", "garanti kâr", "risksiz kazanç",
        "buy signal", "sell signal", "strong buy", "strong sell", "emir gönderildi",
        "aktif trading başladı", "paper’a alındı", "canlıya alındı", "deploy edildi",
        "production’a alındı", "sent_to_broker", "live_order"
    ]

    text_lower = text.lower()
    for phrase in unsafe_phrases:
        if phrase in text_lower:
            return False

    forbidden_words = ["buy", "sell", "entry", "exit", "order", "portfolio_weight"]
    for word in forbidden_words:
        if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
            return False

    return True

def build_regime_boundary_rules(context_payload: dict[str, Any] | None = None, columns: List[str] | None = None, text: str | None = None) -> List[RegimeBoundaryRule]:
    if context_payload is None:
        context_payload = {}
    if columns is None:
        columns = []
    if text is None:
        text = ""

    rules = []

    rule_defs = [
        (RegimeBoundaryRuleKind.NO_TRADE_SIGNAL, False, lambda: context_payload.get("produces_trade_signal", False), "Cannot produce trade signals"),
        (RegimeBoundaryRuleKind.NO_STRATEGY_ACTIVATION, False, lambda: context_payload.get("strategy_activation_allowed", False) or context_payload.get("activation_allowed", False), "Cannot activate strategies"),
        (RegimeBoundaryRuleKind.NO_ORDER_DECISION, False, lambda: context_payload.get("produces_order_decision", False), "Cannot produce order decisions"),
        (RegimeBoundaryRuleKind.NO_PORTFOLIO_WEIGHT, False, lambda: context_payload.get("produces_portfolio_weights", False), "Cannot produce portfolio weights"),
        (RegimeBoundaryRuleKind.NO_BROKER_EXECUTION, False, lambda: context_payload.get("broker_execution_enabled", False), "Cannot enable broker execution"),
        (RegimeBoundaryRuleKind.NO_PAPER_MUTATION, False, lambda: context_payload.get("paper_state_mutation_enabled", False) or context_payload.get("active_paper_enabled", False), "Cannot mutate paper state"),
        (RegimeBoundaryRuleKind.NO_TELEGRAM_REAL_SEND, False, lambda: context_payload.get("telegram_real_send_enabled", False), "Cannot send real Telegram messages"),
        (RegimeBoundaryRuleKind.NO_INVESTMENT_ADVICE, False, lambda: context_payload.get("investment_advice", False), "Cannot provide investment advice"),
        (RegimeBoundaryRuleKind.NO_DEPLOYMENT, False, lambda: context_payload.get("deployment_allowed", False), "Cannot allow deployment"),
        (RegimeBoundaryRuleKind.NO_NETWORK_FETCH, False, lambda: context_payload.get("network_used", False) or context_payload.get("network_default_enabled", False), "Cannot fetch from network"),
        (RegimeBoundaryRuleKind.NO_SCRAPING, False, lambda: context_payload.get("scraping_enabled", False) or context_payload.get("scraping_used", False), "Cannot scrape"),
        (RegimeBoundaryRuleKind.NO_HTML_PARSE, False, lambda: context_payload.get("html_parse_enabled", False) or context_payload.get("html_parsing_used", False), "Cannot parse HTML"),
        (RegimeBoundaryRuleKind.NO_PAID_API, False, lambda: context_payload.get("paid_api_enabled", False) or context_payload.get("paid_api_used", False), "Cannot use paid APIs"),
        (RegimeBoundaryRuleKind.SAFE_COLUMN_NAMES, True, lambda: check_safe_columns(columns), "Columns must be safe"),
        (RegimeBoundaryRuleKind.SAFE_LANGUAGE, True, lambda: check_safe_language(text), "Text must use safe language"),
    ]

    for kind, expected, eval_func, rationale in rule_defs:
        observed = eval_func()
        passed = observed == expected

        rules.append(
            RegimeBoundaryRule(
                rule_id=create_regime_boundary_rule_id(),
                created_at_utc=_now(),
                rule_kind=kind,
                name=kind.value,
                status=RegimeBoundaryStatus.PASSED if passed else RegimeBoundaryStatus.FAILED,
                required=True,
                passed=passed,
                expected_value=expected,
                observed_value=observed,
                rationale=rationale,
                warnings=[],
                errors=[] if passed else [f"Rule failed: Expected {expected}, got {observed}"],
                risk_flags=[] if passed else [RegimeFoundationRiskFlag.NON_ACTIVATION_BOUNDARY_FAILED],
                metadata={}
            )
        )

    return rules

def build_regime_non_activation_boundary_result(context_payload: dict[str, Any] | None = None, columns: List[str] | None = None, text: str | None = None) -> RegimeNonActivationBoundaryResult:
    rules = build_regime_boundary_rules(context_payload, columns, text)

    total_rules = len(rules)
    passed_rules = len([r for r in rules if r.passed])
    failed_rules = total_rules - passed_rules
    boundary_passed = failed_rules == 0

    risk_flags = []
    if not boundary_passed:
        risk_flags.append(RegimeFoundationRiskFlag.NON_ACTIVATION_BOUNDARY_FAILED)

    return RegimeNonActivationBoundaryResult(
        boundary_id=create_regime_non_activation_boundary_id(),
        created_at_utc=_now(),
        status=RegimeBoundaryStatus.PASSED if boundary_passed else RegimeBoundaryStatus.FAILED,
        rules=rules,
        total_rules=total_rules,
        passed_rules=passed_rules,
        failed_rules=failed_rules,
        blocked_rules=failed_rules,
        boundary_passed=boundary_passed,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        broker_execution_enabled=False,
        order_creation_enabled=False,
        paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        warnings=[],
        errors=[] if boundary_passed else [f"Boundary failed {failed_rules} rules."],
        risk_flags=risk_flags,
        metadata={}
    )

def regime_boundary_passed(result: RegimeNonActivationBoundaryResult) -> bool:
    return result.boundary_passed

def validate_regime_boundary_result(result: RegimeNonActivationBoundaryResult) -> List[str]:
    errors = []
    if result.activation_allowed or result.strategy_activation_allowed or result.deployment_allowed:
        errors.append("Boundary illegally allows activation or deployment")
    if result.broker_execution_enabled or result.order_creation_enabled or result.paper_state_mutation_enabled:
        errors.append("Boundary illegally allows execution or paper mutation")
    if result.telegram_real_send_enabled:
        errors.append("Boundary illegally allows Telegram real send")
    if result.produces_trade_signal or result.produces_order_decision or result.produces_portfolio_weights:
        errors.append("Boundary illegally produces execution outputs")
    if result.investment_advice:
        errors.append("Boundary illegally provides investment advice")
    return errors

def regime_boundary_summary(result: RegimeNonActivationBoundaryResult) -> dict[str, Any]:
    return {
        "boundary_id": result.boundary_id,
        "status": result.status.value,
        "total": result.total_rules,
        "passed": result.passed_rules,
        "failed": result.failed_rules
    }

def regime_boundary_to_text(result: RegimeNonActivationBoundaryResult, limit: int = 300) -> str:
    lines = [
        f"Boundary ID: {result.boundary_id}",
        f"Status: {result.status.value}",
        f"Rules: {result.passed_rules}/{result.total_rules} passed"
    ]
    if not result.boundary_passed:
        lines.append("Failed Rules:")
        for r in result.rules:
            if not r.passed:
                lines.append(f"  - {r.name}: {r.errors[0]}")
    return "\n".join(lines)
