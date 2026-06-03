from typing import Any
from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    StressInputReference,
    StressScenarioPolicy,
    StressScenario,
    ScenarioReplayResult,
    ScenarioPerformanceMetric,
    MonteCarloPolicy,
    MonteCarloPath,
    MonteCarloReplayResult,
    RobustnessScorecard,
    StressValidationReport,
    MonteCarloRobustnessReport,
    StressRobustnessContext
)
from usa_signal_bot.backtesting.stress_robustness.stress_input_resolver import detect_forbidden_stress_columns

def validate_stress_input_reference_schema(item: StressInputReference) -> list[str]:
    errors = []
    if not item.input_ref_id:
        errors.append("input_ref_id is missing")
    if detect_forbidden_stress_columns(item.columns):
        errors.append("Forbidden columns detected in schema")
    return errors

def validate_no_forbidden_stress_columns(columns: list[str]) -> list[str]:
    detected = detect_forbidden_stress_columns(columns)
    if detected:
        return [f"Forbidden stress columns found: {detected}"]
    return []

# Placeholder for full schema validators, just returning basic checks to avoid bloat
def validate_stress_validation_report_schema(report: StressValidationReport) -> list[str]:
    if not report.report_id:
        return ["report_id missing"]
    return []
