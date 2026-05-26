from typing import Any, Dict, List
from usa_signal_bot.provider_freeze.phase114_models import DataLayerRehearsalReport
from usa_signal_bot.core.enums import ProviderFreezeRiskFlag

def validate_data_layer_rehearsal_report(report: DataLayerRehearsalReport) -> List[str]:
    errors = []
    if not report.metadata_only:
        errors.append("Report missing metadata_only.")
    if not report.dry_run_only:
        errors.append("Report missing dry_run_only.")
    if not report.research_data_only:
        errors.append("Report missing research_data_only.")

    for flag in [
        "network_used", "paid_api_used", "scraping_used", "html_parsing_used",
        "broker_used", "order_created", "paper_state_mutated", "telegram_real_sent",
        "dashboard_started", "produces_trade_signal", "produces_order_decision"
    ]:
        if getattr(report, flag):
            errors.append(f"Rehearsal violated {flag}.")

    if report.failed_scenarios > 0 or report.blocked_scenarios > 0:
        errors.append(f"Rehearsal has {report.failed_scenarios} failed and {report.blocked_scenarios} blocked scenarios.")

    return errors

def data_layer_rehearsal_passed(report: DataLayerRehearsalReport) -> bool:
    return report.rehearsal_passed and len(validate_data_layer_rehearsal_report(report)) == 0

def data_layer_rehearsal_blocks_phase115(report: DataLayerRehearsalReport) -> bool:
    return not data_layer_rehearsal_passed(report)

def rehearsal_validator_summary(errors: List[str]) -> Dict[str, Any]:
    return {
        "valid": len(errors) == 0,
        "error_count": len(errors),
        "errors": errors
    }

def rehearsal_validator_to_text(errors: List[str]) -> str:
    if not errors:
        return "Rehearsal validation passed safely."
    return "Rehearsal Validation Errors:\n" + "\n".join(f" - {e}" for e in errors)
