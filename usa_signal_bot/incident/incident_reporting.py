from pathlib import Path
from usa_signal_bot.incident.incident_models import IncidentRecord, IncidentSummaryReport
from usa_signal_bot.incident.recovery_models import RecoveryPlan, RecoveryPlanResult
from usa_signal_bot.incident.rollback_models import RollbackSource, RollbackPlan, RollbackExecutionResult
from usa_signal_bot.incident.rollback_precheck import RollbackPrecheckReport
from usa_signal_bot.incident.incident_validation import IncidentValidationReport

def incident_record_to_text(record: IncidentRecord) -> str:
    return f"[{record.severity.name}] {record.title} ({record.status.name})\n  Source: {record.source.name}, Category: {record.category.name}\n  Summary: {record.summary}"

def incident_summary_report_to_text(report: IncidentSummaryReport, limit: int = 50) -> str:
    lines = [f"=== INCIDENT SUMMARY REPORT ({report.status.name}) ==="]
    lines.append(f"Highest Severity: {report.highest_severity.name}")
    lines.append(f"Total Incidents: {report.incident_count} (Open: {report.open_count}, Critical: {report.critical_count})")
    lines.append("\nIncidents:")
    for i in report.incidents[:limit]:
        lines.append("  " + incident_record_to_text(i).replace("\n", "\n  "))
    lines.append("\nRecommended Actions:")
    for a in report.recommended_actions:
        lines.append(f"  - {a}")
    lines.append("\n" + incident_limitations_text())
    return "\n".join(lines)

def recovery_plan_to_text(plan: RecoveryPlan, limit: int = 50) -> str:
    lines = [f"=== RECOVERY PLAN ({plan.status.name}) ==="]
    lines.append(f"Dry Run: {plan.dry_run}")
    lines.append("Actions:")
    for a in plan.actions[:limit]:
        req = "[REQUIRED]" if a.required else "[OPTIONAL]"
        lines.append(f"  {req} {a.name} ({a.status.name})")
        if a.command:
            lines.append(f"    Cmd: {a.command}")
    lines.append("\n" + incident_limitations_text())
    return "\n".join(lines)

def recovery_plan_result_to_text(result: RecoveryPlanResult, limit: int = 50) -> str:
    lines = [f"=== RECOVERY PLAN RESULT ({result.status.name}) ==="]
    lines.append("Action Results:")
    for r in result.action_results[:limit]:
        lines.append(f"  {r.action_type.name}: {r.status.name} - {r.summary}")
    return "\n".join(lines)

def rollback_source_to_text(source: RollbackSource) -> str:
    return f"{source.source_type.name} - {source.path} (Valid: {source.valid})"

def rollback_precheck_report_to_text(report: RollbackPrecheckReport) -> str:
    lines = [f"=== ROLLBACK PRECHECK ({report.status.name}) ==="]
    for i in report.items:
        lines.append(f"  {i.name}: {i.status.name} - {i.message}")
    return "\n".join(lines)

def rollback_plan_to_text(plan: RollbackPlan, limit: int = 50) -> str:
    lines = [f"=== ROLLBACK PLAN ({plan.status.name}) ==="]
    lines.append(f"Safety: {plan.safety_status.name}")
    lines.append(f"Dry Run: {plan.dry_run}")
    lines.append("Steps:")
    for s in plan.steps[:limit]:
        prot = "[PROTECTED]" if s.protected else ""
        lines.append(f"  {s.action} {s.source_path} -> {s.target_path} {prot}")
    lines.append("\n" + incident_limitations_text())
    return "\n".join(lines)

def rollback_execution_result_to_text(result: RollbackExecutionResult, limit: int = 50) -> str:
    lines = [f"=== ROLLBACK RESULT ({result.status.name}) ==="]
    lines.append(f"Dry Run: {result.dry_run}")
    lines.append(f"Executed: {len(result.executed_steps)}, Skipped: {len(result.skipped_steps)}, Failed: {len(result.failed_steps)}")
    if result.errors:
         lines.append("Errors:")
         for e in result.errors:
             lines.append(f"  - {e}")
    return "\n".join(lines)

def incident_store_summary_to_text(summary: dict[str, int]) -> str:
    lines = ["=== INCIDENT STORE SUMMARY ==="]
    for k, v in summary.items():
        lines.append(f"  {k}: {v}")
    return "\n".join(lines)

def incident_limitations_text() -> str:
    return (
        "*** LOCAL OPERATIONAL REVIEW ONLY ***\n"
        "1. No broker API execution or live trading.\n"
        "2. Rollback 'PASS' is NOT an investment approval.\n"
        "3. System is default dry-run and read-only.\n"
    )

def write_full_incident_review_json(
    path: Path,
    incident_report: IncidentSummaryReport,
    recovery_plan: RecoveryPlan | None = None,
    rollback_plan: RollbackPlan | None = None,
    validation_report: IncidentValidationReport | None = None
) -> Path:
    from usa_signal_bot.incident.incident_models import incident_summary_report_to_dict
    from usa_signal_bot.incident.recovery_models import recovery_plan_to_dict
    from usa_signal_bot.incident.rollback_models import rollback_plan_to_dict
    import json

    data = {
        "incident_report": incident_summary_report_to_dict(incident_report)
    }
    if recovery_plan:
        data["recovery_plan"] = recovery_plan_to_dict(recovery_plan)
    if rollback_plan:
         data["rollback_plan"] = rollback_plan_to_dict(rollback_plan)
    if validation_report:
         data["validation_report"] = {
             "valid": validation_report.valid,
             "issues": [{"field": i.field, "message": i.message} for i in validation_report.issues]
         }

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return path
