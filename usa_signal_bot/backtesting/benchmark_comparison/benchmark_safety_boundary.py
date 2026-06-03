from typing import Any, Dict, List, Optional
import datetime
from usa_signal_bot.backtesting.benchmark_comparison.phase149_models import BenchmarkSafetyBoundaryResult, BenchmarkSafetyBoundaryRule, BenchmarkSafetyRuleKind, create_benchmark_safety_boundary_result_id, create_benchmark_safety_boundary_rule_id
def build_benchmark_safety_boundary_rules(ctx: Optional[Dict[str, Any]] = None) -> List[BenchmarkSafetyBoundaryRule]:
    return [BenchmarkSafetyBoundaryRule(rule_id=create_benchmark_safety_boundary_rule_id(), created_at_utc="", rule_kind=BenchmarkSafetyRuleKind.NO_LIVE_TRADING, name="NO_LIVE_TRADING", passed=True if not ctx or not ctx.get("live_trading_enabled") else False)]
def build_benchmark_safety_boundary_result(rules: List[BenchmarkSafetyBoundaryRule]) -> BenchmarkSafetyBoundaryResult:
    return BenchmarkSafetyBoundaryResult(boundary_id=create_benchmark_safety_boundary_result_id(), created_at_utc="", rules=rules, boundary_passed=all(r.passed for r in rules))
def benchmark_safety_boundary_to_text(r: BenchmarkSafetyBoundaryResult, limit=300) -> str: return "boundary"
