import os
import re

def ensure_dir(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

def write_file(file_path, content):
    ensure_dir(file_path)
    with open(file_path, 'w') as f:
        f.write(content)

# ---------------------------------------------------------
# STORAGE (cost_robustness/robustness_store.py)
# ---------------------------------------------------------
store_content = """
import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from usa_signal_bot.cost_robustness.robustness_models import (
    CostStressScenario, CostStressedBacktestResult, ExecutionSensitivityMatrix,
    WalkForwardCostRobustnessResult, CostFragilityAssessment, CostRobustnessReview,
    cost_stress_scenario_to_dict, cost_stressed_backtest_result_to_dict,
    execution_sensitivity_matrix_to_dict, walk_forward_cost_robustness_result_to_dict,
    cost_fragility_assessment_to_dict, cost_robustness_review_to_dict
)

def robustness_store_dir(data_root: Path) -> Path:
    d = data_root / "cost_robustness"
    d.mkdir(parents=True, exist_ok=True)
    return d

def stress_scenarios_dir(data_root: Path) -> Path:
    d = robustness_store_dir(data_root) / "scenarios"
    d.mkdir(parents=True, exist_ok=True)
    return d

def stressed_results_dir(data_root: Path) -> Path:
    d = robustness_store_dir(data_root) / "stressed_results"
    d.mkdir(parents=True, exist_ok=True)
    return d

def sensitivity_matrices_dir(data_root: Path) -> Path:
    d = robustness_store_dir(data_root) / "sensitivity_matrices"
    d.mkdir(parents=True, exist_ok=True)
    return d

def walk_forward_cost_robustness_dir(data_root: Path) -> Path:
    d = robustness_store_dir(data_root) / "walk_forward"
    d.mkdir(parents=True, exist_ok=True)
    return d

def fragility_assessments_dir(data_root: Path) -> Path:
    d = robustness_store_dir(data_root) / "fragility"
    d.mkdir(parents=True, exist_ok=True)
    return d

def robustness_reviews_dir(data_root: Path) -> Path:
    d = robustness_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_cost_stress_scenarios_json(path: Path, scenarios: List[CostStressScenario]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump([cost_stress_scenario_to_dict(s) for s in scenarios], f, indent=2)
    return path

def write_cost_stressed_backtest_result_json(path: Path, result: CostStressedBacktestResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(cost_stressed_backtest_result_to_dict(result), f, indent=2)
    return path

def write_execution_sensitivity_matrix_json(path: Path, matrix: ExecutionSensitivityMatrix) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(execution_sensitivity_matrix_to_dict(matrix), f, indent=2)
    return path

def write_walk_forward_cost_robustness_result_json(path: Path, result: WalkForwardCostRobustnessResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(walk_forward_cost_robustness_result_to_dict(result), f, indent=2)
    return path

def write_cost_fragility_assessment_json(path: Path, assessment: CostFragilityAssessment) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(cost_fragility_assessment_to_dict(assessment), f, indent=2)
    return path

def write_cost_robustness_review_json(path: Path, review: CostRobustnessReview) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(cost_robustness_review_to_dict(review), f, indent=2)
    return path

def read_cost_robustness_review_json(path: Path) -> Dict[str, Any]:
    with open(path, 'r') as f:
        return json.load(f)

def list_cost_robustness_reviews(data_root: Path) -> List[Path]:
    d = robustness_reviews_dir(data_root)
    return sorted(d.glob("*.json"))

def get_latest_cost_robustness_review(data_root: Path) -> Optional[Path]:
    files = list_cost_robustness_reviews(data_root)
    return files[-1] if files else None

def robustness_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "reviews_count": len(list_cost_robustness_reviews(data_root))
    }
"""
write_file("usa_signal_bot/cost_robustness/robustness_store.py", store_content)

# ---------------------------------------------------------
# VALIDATION (cost_robustness/robustness_validation.py)
# ---------------------------------------------------------
valid_content = """
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import json
from usa_signal_bot.cost_robustness.robustness_models import (
    CostStressScenario, CostStressedBacktestResult, ExecutionSensitivityMatrix,
    WalkForwardCostRobustnessResult, CostFragilityAssessment, CostRobustnessReview
)
from usa_signal_bot.core.exceptions import CostRobustnessValidationError

@dataclass
class CostRobustnessValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CostRobustnessValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[CostRobustnessValidationIssue]
    warnings: List[str]
    errors: List[str]

def _create_report(issues: List[CostRobustnessValidationIssue]) -> CostRobustnessValidationReport:
    errors = [i.message for i in issues if i.severity in ("ERROR", "BLOCKED")]
    warnings = [i.message for i in issues if i.severity == "WARNING"]
    return CostRobustnessValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=sum(1 for i in issues if i.severity == "ERROR"),
        blocked_count=sum(1 for i in issues if i.severity == "BLOCKED"),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_cost_stress_scenarios_report(scenarios: List[CostStressScenario]) -> CostRobustnessValidationReport:
    issues = []
    for s in scenarios:
        if s.slippage_multiplier < 0 or s.spread_multiplier < 0 or s.impact_multiplier < 0:
            issues.append(CostRobustnessValidationIssue("ERROR", "multipliers", f"Negative multiplier in {s.name}"))
    return _create_report(issues)

def validate_cost_stressed_backtest_result_report(result: CostStressedBacktestResult) -> CostRobustnessValidationReport:
    return _create_report([])

def validate_execution_sensitivity_matrix_report(matrix: ExecutionSensitivityMatrix) -> CostRobustnessValidationReport:
    return _create_report([])

def validate_walk_forward_cost_robustness_report(result: WalkForwardCostRobustnessResult) -> CostRobustnessValidationReport:
    return _create_report([])

def validate_cost_fragility_assessment_report(assessment: CostFragilityAssessment) -> CostRobustnessValidationReport:
    issues = []
    if assessment.fragility_score is not None and not (0 <= assessment.fragility_score <= 100):
        issues.append(CostRobustnessValidationIssue("ERROR", "fragility_score", "Score out of bounds 0-100"))
    return _create_report(issues)

def validate_cost_robustness_review_report(review: CostRobustnessReview) -> CostRobustnessValidationReport:
    return _create_report([])

def validate_no_sensitive_data_in_cost_robustness_payload(payload: Dict[str, Any]) -> CostRobustnessValidationReport:
    issues = []
    payload_str = json.dumps(payload).lower()
    if 'secret' in payload_str or 'token' in payload_str or 'api_key' in payload_str:
        issues.append(CostRobustnessValidationIssue("ERROR", "sensitive_data", "Possible token or secret leaked in payload"))
    return _create_report(issues)

def validate_no_live_execution_language_in_cost_robustness(text: str) -> CostRobustnessValidationReport:
    issues = []
    lower_text = text.lower()
    forbidden = ["live approved", "sent to broker", "kesin al", "garanti", "guaranteed fill", "kesin maliyet", "kesin kâr"]
    for f in forbidden:
        if f in lower_text:
            issues.append(CostRobustnessValidationIssue("ERROR", "language", f"Forbidden live execution language detected: {f}"))
    return _create_report(issues)

def validate_no_broker_execution_fields_in_cost_robustness(payload: Dict[str, Any]) -> CostRobustnessValidationReport:
    issues = []
    payload_str = json.dumps(payload).lower()
    forbidden_keys = ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]
    for k in forbidden_keys:
        if f'"{k}"' in payload_str:
            issues.append(CostRobustnessValidationIssue("ERROR", "broker_fields", f"Forbidden broker execution field detected: {k}"))
    return _create_report(issues)

def cost_robustness_validation_report_to_text(report: CostRobustnessValidationReport) -> str:
    return f"Valid: {report.valid} | Errors: {report.error_count} | Warnings: {report.warning_count}"

def assert_cost_robustness_valid(report: CostRobustnessValidationReport) -> None:
    if not report.valid:
        raise CostRobustnessValidationError(f"Validation failed: {report.errors}")
"""
write_file("usa_signal_bot/cost_robustness/robustness_validation.py", valid_content)
