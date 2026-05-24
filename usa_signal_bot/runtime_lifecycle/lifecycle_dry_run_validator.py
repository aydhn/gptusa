from typing import List, Dict, Any
from usa_signal_bot.runtime_lifecycle.phase104_models import RuntimeLifecycleContext

def validate_lifecycle_dry_run(context: RuntimeLifecycleContext) -> List[str]:
    errors = []
    if context.execution_performed:
        errors.append("Dry run violated: execution_performed is True")
    if context.network_used:
        errors.append("Dry run violated: network_used is True")
    if context.broker_used:
        errors.append("Dry run violated: broker_used is True")
    if context.order_created:
        errors.append("Dry run violated: order_created is True")
    if context.paper_state_mutated:
        errors.append("Dry run violated: paper_state_mutated is True")
    if context.telegram_real_sent:
        errors.append("Dry run violated: telegram_real_sent is True")
    if context.scraping_used:
        errors.append("Dry run violated: scraping_used is True")
    if context.dashboard_started:
        errors.append("Dry run violated: dashboard_started is True")

    return errors

def lifecycle_dry_run_passed(context: RuntimeLifecycleContext) -> bool:
    return len(validate_lifecycle_dry_run(context)) == 0

def lifecycle_dry_run_summary(context: RuntimeLifecycleContext) -> Dict[str, Any]:
    errors = validate_lifecycle_dry_run(context)
    return {"passed": len(errors) == 0, "errors": errors}

def lifecycle_dry_run_validator_to_text(errors: List[str]) -> str:
    if not errors:
        return "Lifecycle dry run passed without execution."
    return "Lifecycle dry run failed:\n" + "\n".join([f"- {e}" for e in errors])
