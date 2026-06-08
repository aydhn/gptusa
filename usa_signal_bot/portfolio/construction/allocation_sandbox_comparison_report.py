import json
import hashlib
from typing import Any, Dict, List
from usa_signal_bot.portfolio.construction.phase155_models import (
    AllocationSandboxComparisonReport,
    SandboxAllocationResult,
    PrototypeExposureTable,
    PortfolioSandboxDiagnosticRecord,
    create_allocation_sandbox_comparison_report_id,
    _now_str
)
from usa_signal_bot.core.enums import PortfolioConstructionRiskFlag

def build_allocation_sandbox_comparison_report(
    results: List[SandboxAllocationResult],
    table: PrototypeExposureTable,
    diagnostics: List[PortfolioSandboxDiagnosticRecord]
) -> AllocationSandboxComparisonReport:

    report = AllocationSandboxComparisonReport(
        report_id=create_allocation_sandbox_comparison_report_id(),
        created_at_utc=_now_str(),
        allocation_results=results,
        exposure_table=table,
        diagnostics=diagnostics,
        method_count=len(set(r.method_kind for r in results)),
        symbol_count=len(set(r.symbol for r in results)),
        report_hash=None,
        report_valid=True,
        research_allocation_sandbox=True,
        actual_target_weight_detected=False,
        actual_portfolio_weight_detected=False,
        actual_allocation_detected=False,
        actual_position_size_detected=False,
        order_size_detected=False,
        capital_allocation_detected=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    report.report_hash = compute_allocation_sandbox_comparison_report_hash(report)
    return report

def compute_allocation_sandbox_comparison_report_hash(report: AllocationSandboxComparisonReport) -> str:
    data = {
        "results": len(report.allocation_results),
        "diagnostics": len(report.diagnostics),
        "table_hash": report.exposure_table.table_hash,
        "method_count": report.method_count,
        "symbol_count": report.symbol_count
    }
    s = json.dumps(data, sort_keys=True)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def validate_allocation_sandbox_comparison_report(report: AllocationSandboxComparisonReport) -> List[str]:
    errors = []

    # Check flags
    if report.actual_target_weight_detected:
        errors.append("actual_target_weight_detected is True.")
        report.risk_flags.append(PortfolioConstructionRiskFlag.ACTUAL_TARGET_WEIGHT_RISK)
    if report.actual_portfolio_weight_detected:
        errors.append("actual_portfolio_weight_detected is True.")
        report.risk_flags.append(PortfolioConstructionRiskFlag.ACTUAL_PORTFOLIO_WEIGHT_RISK)
    if report.actual_allocation_detected:
        errors.append("actual_allocation_detected is True.")
        report.risk_flags.append(PortfolioConstructionRiskFlag.ACTUAL_ALLOCATION_RISK)
    if report.actual_position_size_detected:
        errors.append("actual_position_size_detected is True.")
        report.risk_flags.append(PortfolioConstructionRiskFlag.ACTUAL_POSITION_SIZE_RISK)
    if report.order_size_detected:
        errors.append("order_size_detected is True.")
        report.risk_flags.append(PortfolioConstructionRiskFlag.ORDER_SIZE_RISK)
    if report.capital_allocation_detected:
        errors.append("capital_allocation_detected is True.")
        report.risk_flags.append(PortfolioConstructionRiskFlag.CAPITAL_DEPLOYMENT_RISK)
    if report.investment_advice:
        errors.append("investment_advice is True.")
        report.risk_flags.append(PortfolioConstructionRiskFlag.INVESTMENT_ADVICE_LANGUAGE_RISK)

    for r in report.allocation_results:
        if r.actual_target_weight is not None:
            errors.append(f"Result {r.symbol} has actual_target_weight.")
            report.risk_flags.append(PortfolioConstructionRiskFlag.ACTUAL_TARGET_WEIGHT_RISK)

    return errors

def allocation_sandbox_comparison_report_summary(report: AllocationSandboxComparisonReport) -> Dict[str, Any]:
    return {
        "report_id": report.report_id,
        "method_count": report.method_count,
        "symbol_count": report.symbol_count,
        "diagnostic_count": len(report.diagnostics),
        "hash": report.report_hash
    }

def allocation_sandbox_comparison_report_to_text(report: AllocationSandboxComparisonReport, limit: int = 300) -> str:
    summary = allocation_sandbox_comparison_report_summary(report)
    return (
        f"Allocation Sandbox Comparison Report: {summary['report_id']}\n"
        f"Methods: {summary['method_count']}, Symbols: {summary['symbol_count']}\n"
        f"Diagnostics: {summary['diagnostic_count']}\n"
        f"Hash: {summary['hash']}"
    )
