from pathlib import Path
import datetime
from usa_signal_bot.core.enums import IncidentReportType, IncidentStatus, IncidentSeverity
from usa_signal_bot.incident.incident_models import IncidentRecord, IncidentSummaryReport, create_incident_report_id, validate_incident_summary_report
from usa_signal_bot.incident.incident_timeline import build_incident_timeline
from usa_signal_bot.incident.incident_adapters import collect_incidents_from_latest_artifacts
from usa_signal_bot.incident.incident_classifier import severity_rank

class IncidentReportBuilder:
    def __init__(self, data_root: Path):
        self.data_root = data_root

    def build_from_incidents(self, incidents: list[IncidentRecord]) -> IncidentSummaryReport:
        timeline = build_incident_timeline(incidents)
        open_count = sum(1 for i in incidents if i.status in [IncidentStatus.OPEN, IncidentStatus.BLOCKED, IncidentStatus.INVESTIGATING])
        critical_count = sum(1 for i in incidents if i.severity in [IncidentSeverity.CRITICAL, IncidentSeverity.BLOCKER])
        highest_sev = self.highest_severity(incidents)
        status = self.decide_report_status(incidents)
        actions = self.recommend_actions(incidents)

        report = IncidentSummaryReport(
            report_id=create_incident_report_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            report_type=IncidentReportType.INCIDENT_SUMMARY,
            status=status,
            highest_severity=highest_sev,
            incident_count=len(incidents),
            open_count=open_count,
            critical_count=critical_count,
            incidents=incidents,
            timeline=timeline,
            recommended_actions=actions,
            output_paths={},
            warnings=[],
            errors=[]
        )
        if not incidents:
            report.status = IncidentStatus.CLOSED # No incidents = ok

        validate_incident_summary_report(report)
        return report

    def build_from_latest_artifacts(self) -> IncidentSummaryReport:
        incidents = collect_incidents_from_latest_artifacts(self.data_root)
        return self.build_from_incidents(incidents)

    def recommend_actions(self, incidents: list[IncidentRecord]) -> list[str]:
        actions = set()
        for inc in incidents:
            if inc.severity in [IncidentSeverity.BLOCKER]:
                actions.add("Manual review required immediately. Automated recovery blocked.")
            if "disk" in str(inc.category).lower():
                actions.add("Check disk quota and run cleanup-dry-run.")
            if "config" in str(inc.category).lower():
                actions.add("Validate configuration with `validate-config`.")

        rec = list(actions)
        if not rec and incidents:
             rec.append("Review incident logs and generate recovery plan.")
        return rec

    def decide_report_status(self, incidents: list[IncidentRecord]) -> IncidentStatus:
        if not incidents:
            return IncidentStatus.CLOSED
        if any(i.status == IncidentStatus.BLOCKED or i.severity == IncidentSeverity.BLOCKER for i in incidents):
            return IncidentStatus.BLOCKED
        if any(i.status == IncidentStatus.OPEN for i in incidents):
            return IncidentStatus.OPEN
        return IncidentStatus.MITIGATED

    def highest_severity(self, incidents: list[IncidentRecord]) -> IncidentSeverity:
        if not incidents:
            return IncidentSeverity.INFO
        highest = IncidentSeverity.INFO
        for i in incidents:
            if severity_rank(i.severity) > severity_rank(highest):
                highest = i.severity
        return highest

    def write_report(self, report: IncidentSummaryReport) -> list[Path]:
        from usa_signal_bot.incident.incident_store import write_incident_report_json, write_incidents_jsonl
        report_path = write_incident_report_json(self.data_root, report)
        jsonl_path = write_incidents_jsonl(self.data_root, report.incidents)
        report.output_paths["report_json"] = str(report_path)
        report.output_paths["incidents_jsonl"] = str(jsonl_path)
        return [report_path, jsonl_path]
