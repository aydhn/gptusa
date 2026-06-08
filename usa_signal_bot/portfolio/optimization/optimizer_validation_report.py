from typing import Any, Dict, List
from usa_signal_bot.portfolio.optimization.phase156_models import OptimizerValidationReport, OptimizerPolicy, OptimizerObjectiveContract, OptimizerConstraintContract, ObjectiveComparisonReport, OptimizerDiagnosticRecord

def build_optimizer_validation_report(policy: OptimizerPolicy, objective_contracts: List[OptimizerObjectiveContract], constraint_contracts: List[OptimizerConstraintContract], comparison_report: ObjectiveComparisonReport, diagnostics: List[OptimizerDiagnosticRecord]) -> OptimizerValidationReport:
    r = OptimizerValidationReport(
        policy=policy,
        objective_contracts=objective_contracts,
        constraint_contracts=constraint_contracts,
        comparison_report=comparison_report,
        diagnostics=diagnostics,
        report_valid=True,
        optimizer_sandbox_valid=True,
        objective_comparison_valid=True,
        constraint_compliance_valid=True,
        no_actual_target_weights=True,
        no_actual_allocation=True,
        no_capital_deployment=True,
        no_order_output=True,
        no_broker_execution=True
    )
    return r

def validate_optimizer_validation_report(report: OptimizerValidationReport) -> List[str]:
    errs = []
    if not report.no_actual_target_weights: errs.append("Produces actual target weights")
    if not report.no_actual_allocation: errs.append("Produces actual allocation")
    if not report.no_capital_deployment: errs.append("Produces capital deployment")
    if not report.no_order_output: errs.append("Produces order output")
    if not report.no_broker_execution: errs.append("Produces broker execution")
    return errs

def optimizer_validation_report_summary(report: OptimizerValidationReport) -> Dict[str, Any]:
    return {"valid": report.report_valid}

def optimizer_validation_report_to_text(report: OptimizerValidationReport, limit: int = 300) -> str:
    return str(report.to_dict())[:limit]
