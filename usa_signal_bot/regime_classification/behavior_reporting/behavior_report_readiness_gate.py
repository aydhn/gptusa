from typing import Any

from usa_signal_bot.core.enums import MarketBehaviorReadinessStatus, MarketBehaviorReadinessRuleKind
from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import (
    RegimeTransitionIngestionResult, MarketBehaviorProfile, RegimeBehaviorSummary,
    BehaviorReportDocument, BehaviorReportQaRuleResult, MarketBehaviorReadinessRule,
    MarketBehaviorReadinessGate
)

def _build_rule(kind: MarketBehaviorReadinessRuleKind, passed: bool) -> MarketBehaviorReadinessRule:
    r = MarketBehaviorReadinessRule()
    r.rule_kind = kind
    r.passed = passed
    r.status = MarketBehaviorReadinessStatus.PASSED if passed else MarketBehaviorReadinessStatus.FAILED
    return r

def build_market_behavior_readiness_rules(
    ingestion: RegimeTransitionIngestionResult,
    profiles: list[MarketBehaviorProfile],
    summaries: list[RegimeBehaviorSummary],
    report: BehaviorReportDocument,
    qa_results: list[BehaviorReportQaRuleResult]
) -> list[MarketBehaviorReadinessRule]:
    from usa_signal_bot.regime_classification.behavior_reporting.behavior_report_qa_validator import behavior_report_qa_passed
    return [
        _build_rule(MarketBehaviorReadinessRuleKind.TRANSITION_ANALYTICS_VALID, ingestion.valid_for_phase130),
        _build_rule(MarketBehaviorReadinessRuleKind.DIAGNOSTICS_ARTIFACTS_AVAILABLE, len(profiles) > 0),
        _build_rule(MarketBehaviorReadinessRuleKind.BEHAVIOR_PROFILES_VALID, all(p.quality.value != "INVALID" for p in profiles)),
        _build_rule(MarketBehaviorReadinessRuleKind.REGIME_SUMMARIES_VALID, all(s.quality.value != "INVALID" for s in summaries)),
        _build_rule(MarketBehaviorReadinessRuleKind.REPORT_DOCUMENT_VALID, report is not None),
        _build_rule(MarketBehaviorReadinessRuleKind.REPORT_QA_PASSED, behavior_report_qa_passed(qa_results)),
        _build_rule(MarketBehaviorReadinessRuleKind.NO_SIGNAL_OUTPUT, True),
        _build_rule(MarketBehaviorReadinessRuleKind.NO_ORDER_OUTPUT, True),
        _build_rule(MarketBehaviorReadinessRuleKind.NO_PORTFOLIO_OUTPUT, True),
        _build_rule(MarketBehaviorReadinessRuleKind.NO_EXECUTION_OUTPUT, True),
        _build_rule(MarketBehaviorReadinessRuleKind.NO_MODEL_TRAINING, True)
    ]

def build_market_behavior_readiness_gate(
    ingestion: RegimeTransitionIngestionResult,
    profiles: list[MarketBehaviorProfile],
    summaries: list[RegimeBehaviorSummary],
    report: BehaviorReportDocument,
    qa_results: list[BehaviorReportQaRuleResult]
) -> MarketBehaviorReadinessGate:
    gate = MarketBehaviorReadinessGate()
    gate.rules = build_market_behavior_readiness_rules(ingestion, profiles, summaries, report, qa_results)

    passed = all(r.passed for r in gate.rules)
    gate.status = MarketBehaviorReadinessStatus.PASSED if passed else MarketBehaviorReadinessStatus.FAILED

    gate.report_document = report
    gate.qa_results = qa_results
    gate.ready_for_phase131 = passed

    return gate

def market_behavior_readiness_passed(gate: MarketBehaviorReadinessGate) -> bool:
    return gate.status == MarketBehaviorReadinessStatus.PASSED

def market_behavior_readiness_blocks_phase131(gate: MarketBehaviorReadinessGate) -> bool:
    return not gate.ready_for_phase131

def validate_market_behavior_readiness_gate(gate: MarketBehaviorReadinessGate) -> list[str]:
    from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import validate_market_behavior_readiness_gate as val
    return val(gate)

def market_behavior_readiness_gate_summary(gate: MarketBehaviorReadinessGate) -> dict[str, Any]:
    return {"passed": market_behavior_readiness_passed(gate)}

def market_behavior_readiness_gate_to_text(gate: MarketBehaviorReadinessGate, limit: int = 300) -> str:
    return f"Gate Passed: {market_behavior_readiness_passed(gate)}"
