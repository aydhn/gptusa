"""Production Readiness Gate."""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import logging

from usa_signal_bot.core.enums import AcceptanceScope, ReadinessGateStatus
from usa_signal_bot.quality.quality_models import (
    ResearchQualityScorecard,
    GateRule,
    GateRuleResult,
    ProductionReadinessGateResult,
    create_gate_id,
)
from usa_signal_bot.quality.gate_rules import default_gate_rules, evaluate_gate_rules

logger = logging.getLogger(__name__)

class ProductionReadinessGate:
    def __init__(self, rules: Optional[List[GateRule]] = None, scope: AcceptanceScope = AcceptanceScope.FULL_LOCAL_STACK):
        self.scope = scope
        self.rules = rules if rules is not None else default_gate_rules(self.scope)

    def decide_gate_status(self, rule_results: List[GateRuleResult]) -> ReadinessGateStatus:
        if not rule_results:
            return ReadinessGateStatus.UNKNOWN

        failed_required = [r for r in rule_results if r.status == ReadinessGateStatus.FAILED]
        warnings = [r for r in rule_results if r.status == ReadinessGateStatus.WARNING]

        for f in failed_required:
            if f.severity.name == "CRITICAL":
                return ReadinessGateStatus.BLOCKED

        if failed_required:
            return ReadinessGateStatus.FAILED

        if warnings:
            return ReadinessGateStatus.WARNING

        return ReadinessGateStatus.PASSED

    def evaluate(self, scorecard: ResearchQualityScorecard, artifacts: Dict[str, Any]) -> ProductionReadinessGateResult:
        rule_results = evaluate_gate_rules(self.rules, scorecard, artifacts)

        passed_count = sum(1 for r in rule_results if r.status == ReadinessGateStatus.PASSED)
        warning_count = sum(1 for r in rule_results if r.status == ReadinessGateStatus.WARNING)
        failed_count = sum(1 for r in rule_results if r.status == ReadinessGateStatus.FAILED)
        blocked_count = sum(1 for r in rule_results if r.status == ReadinessGateStatus.BLOCKED)

        status = self.decide_gate_status(rule_results)

        warnings = [r.message for r in rule_results if r.status == ReadinessGateStatus.WARNING]
        errors = [r.message for r in rule_results if r.status in (ReadinessGateStatus.FAILED, ReadinessGateStatus.BLOCKED)]

        if scorecard.overall_status.name == "INSUFFICIENT_DATA" if hasattr(scorecard.overall_status, "name") else scorecard.overall_status == "insufficient_data":
            status = ReadinessGateStatus.INSUFFICIENT_DATA
            errors.append("Insufficient data to evaluate readiness.")

        return ProductionReadinessGateResult(
            gate_id=create_gate_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            scope=self.scope,
            status=status,
            rule_results=rule_results,
            passed_count=passed_count,
            warning_count=warning_count,
            failed_count=failed_count,
            blocked_count=blocked_count,
            warnings=warnings,
            errors=errors
        )

def summarize_gate(result: ProductionReadinessGateResult) -> str:
    lines = [
        f"--- Production Readiness Gate ({result.gate_id}) ---",
        f"Scope: {result.scope.name}",
        f"Status: {result.status.name}",
        f"Rules: {result.passed_count} Passed, {result.warning_count} Warnings, {result.failed_count} Failed, {result.blocked_count} Blocked",
    ]
    if result.errors:
        lines.append("\nErrors:")
        for e in result.errors:
            lines.append(f" - {e}")
    return "\n".join(lines)
