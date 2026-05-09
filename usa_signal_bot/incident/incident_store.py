from pathlib import Path
import json
from typing import Any
from usa_signal_bot.incident.incident_models import IncidentSummaryReport, IncidentRecord, incident_summary_report_to_dict, incident_record_to_dict
from usa_signal_bot.incident.recovery_models import RecoveryPlan, RecoveryPlanResult, recovery_plan_to_dict, recovery_plan_result_to_dict
from usa_signal_bot.incident.rollback_models import RollbackPlan, RollbackExecutionResult, rollback_plan_to_dict, rollback_execution_result_to_dict
from usa_signal_bot.incident.rollback_precheck import RollbackPrecheckReport, rollback_precheck_report_to_dict

def incident_store_dir(data_root: Path) -> Path:
    return data_root / "incident"

def incident_reports_dir(data_root: Path) -> Path:
    return incident_store_dir(data_root) / "reports"

def incident_records_dir(data_root: Path) -> Path:
    return incident_store_dir(data_root) / "incidents"

def recovery_plans_dir(data_root: Path) -> Path:
    return incident_store_dir(data_root) / "recovery" / "plans"

def recovery_results_dir(data_root: Path) -> Path:
    return incident_store_dir(data_root) / "recovery" / "results"

def rollback_plans_dir(data_root: Path) -> Path:
    return incident_store_dir(data_root) / "rollback" / "plans"

def rollback_results_dir(data_root: Path) -> Path:
    return incident_store_dir(data_root) / "rollback" / "results"

def rollback_precheck_dir(data_root: Path) -> Path:
    return incident_store_dir(data_root) / "rollback" / "precheck"

def incident_audit_dir(data_root: Path) -> Path:
    return incident_store_dir(data_root) / "audit"

def write_incident_report_json(data_root: Path, report: IncidentSummaryReport) -> Path:
    d = incident_reports_dir(data_root)
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{report.report_id}.json"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(incident_summary_report_to_dict(report), f, indent=2)
    return p

def write_incidents_jsonl(data_root: Path, incidents: list[IncidentRecord]) -> Path:
    d = incident_records_dir(data_root)
    d.mkdir(parents=True, exist_ok=True)
    if not incidents:
        return d / "empty.jsonl"
    report_id = "incidents"
    p = d / f"{report_id}_{incidents[0].created_at_utc.replace(':', '').replace('-', '')[:14]}.jsonl"
    with open(p, "w", encoding="utf-8") as f:
        for i in incidents:
             f.write(json.dump(incident_record_to_dict(i), f) + "\n")
    return p

def write_recovery_plan_json(data_root: Path, plan: RecoveryPlan) -> Path:
    d = recovery_plans_dir(data_root)
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{plan.plan_id}.json"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(recovery_plan_to_dict(plan), f, indent=2)
    return p

def write_recovery_result_json(data_root: Path, result: RecoveryPlanResult) -> Path:
    d = recovery_results_dir(data_root)
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{result.result_id}.json"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(recovery_plan_result_to_dict(result), f, indent=2)
    return p

def write_rollback_plan_json(data_root: Path, plan: RollbackPlan) -> Path:
    d = rollback_plans_dir(data_root)
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{plan.plan_id}.json"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(rollback_plan_to_dict(plan), f, indent=2)
    return p

def write_rollback_result_json(data_root: Path, result: RollbackExecutionResult) -> Path:
    d = rollback_results_dir(data_root)
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{result.execution_id}.json"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(rollback_execution_result_to_dict(result), f, indent=2)
    return p

def write_rollback_precheck_report_json(data_root: Path, report: RollbackPrecheckReport) -> Path:
    d = rollback_precheck_dir(data_root)
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{report.report_id}.json"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(rollback_precheck_report_to_dict(report), f, indent=2)
    return p

def read_incident_report_json(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def read_recovery_plan_json(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def read_rollback_plan_json(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_incident_reports(data_root: Path) -> list[Path]:
    d = incident_reports_dir(data_root)
    if not d.exists(): return []
    return sorted(d.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)

def list_recovery_plans(data_root: Path) -> list[Path]:
    d = recovery_plans_dir(data_root)
    if not d.exists(): return []
    return sorted(d.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)

def list_rollback_plans(data_root: Path) -> list[Path]:
    d = rollback_plans_dir(data_root)
    if not d.exists(): return []
    return sorted(d.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)

def list_rollback_results(data_root: Path) -> list[Path]:
    d = rollback_results_dir(data_root)
    if not d.exists(): return []
    return sorted(d.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)

def get_latest_incident_report(data_root: Path) -> Path | None:
    lst = list_incident_reports(data_root)
    return lst[0] if lst else None

def get_latest_recovery_plan(data_root: Path) -> Path | None:
    lst = list_recovery_plans(data_root)
    return lst[0] if lst else None

def get_latest_rollback_plan(data_root: Path) -> Path | None:
    lst = list_rollback_plans(data_root)
    return lst[0] if lst else None

def incident_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "incident_reports_count": len(list_incident_reports(data_root)),
        "recovery_plans_count": len(list_recovery_plans(data_root)),
        "rollback_plans_count": len(list_rollback_plans(data_root))
    }
