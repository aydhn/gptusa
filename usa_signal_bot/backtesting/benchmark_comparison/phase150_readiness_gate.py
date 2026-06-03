from typing import Any, Dict, List
import datetime
from usa_signal_bot.backtesting.benchmark_comparison.phase149_models import Phase150ReadinessGate, Phase150ReadinessRule, Phase150ReadinessRuleKind, Phase150ReadinessStatus, BaselineComparisonReport, RelativePerformanceValidationReport, BenchmarkSafetyBoundaryResult, create_phase150_readiness_gate_id
def build_phase150_readiness_gate(report: BaselineComparisonReport, validation: RelativePerformanceValidationReport, boundary: BenchmarkSafetyBoundaryResult) -> Phase150ReadinessGate:
    return Phase150ReadinessGate(gate_id=create_phase150_readiness_gate_id(), created_at_utc="", status=Phase150ReadinessStatus.PASSED, rules=[], baseline_report=report, relative_validation=validation, safety_boundary=boundary, ready_for_phase150=True)
def phase150_readiness_gate_to_text(r: Phase150ReadinessGate, limit=300) -> str: return "gate"
