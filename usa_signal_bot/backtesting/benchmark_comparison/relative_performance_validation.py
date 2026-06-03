from typing import Any, Dict, List
import datetime
from usa_signal_bot.backtesting.benchmark_comparison.phase149_models import RelativePerformanceValidationReport, RelativePerformanceValidationRule, BaselineComparisonReport, RelativePerformanceValidationRuleKind, BaselineComparisonStatus, create_relative_performance_validation_report_id, create_relative_performance_validation_rule_id
def build_relative_performance_validation_report(report: BaselineComparisonReport) -> RelativePerformanceValidationReport:
    return RelativePerformanceValidationReport(validation_id=create_relative_performance_validation_report_id(), created_at_utc="", rules=[], baseline_report=report, validation_passed=False, validation_status=BaselineComparisonStatus.FAILED)
def relative_performance_validation_to_text(r: RelativePerformanceValidationReport, limit=300) -> str: return "validation"
