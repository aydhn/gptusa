from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List
import uuid
from usa_signal_bot.release.release_models import OperatorRunbook, create_runbook_id

def generate_operator_runbook(project_root: Path = None) -> OperatorRunbook:
    sections = {
        "OVERVIEW": build_runbook_overview_section(),
        "INSTALLATION": build_installation_section(),
        "CONFIGURATION": build_configuration_section(),
        "DAILY_OPERATION": build_daily_operation_section(),
        "WEEKLY_MAINTENANCE": build_weekly_maintenance_section(),
        "BACKUP_RESTORE": build_backup_restore_section(),
        "REGRESSION": build_regression_section(),
        "QUALITY_GATE": build_quality_gate_section(),
        "PAPER_TRADING": build_paper_trading_section(),
        "NOTIFICATIONS": build_notifications_section(),
        "TROUBLESHOOTING": build_troubleshooting_section(),
        "SAFETY_LIMITATIONS": build_safety_limitations_section()
    }

    return OperatorRunbook(
        runbook_id=create_runbook_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        title="USA Signal Bot - Operator Runbook",
        sections=sections,
        command_reference=build_command_reference()
    )

def build_runbook_overview_section() -> str:
    return """This runbook provides operational instructions for running the USA Signal Bot locally.
It covers installation, configuration, daily operations, and maintenance workflows."""

def build_installation_section() -> str:
    return """1. Ensure Python 3.10+ is installed.
2. Create a virtual environment: `python -m venv .venv`
3. Activate the environment (e.g., `source .venv/bin/activate` or `.venv\\Scripts\\activate`).
4. Install dependencies: `pip install -r requirements.txt`"""

def build_configuration_section() -> str:
    return """Configuration is driven by YAML files in the `config/` directory.
- `default.yaml`: Base settings.
- `local.yaml`: User overrides (create from `local.example.yaml`).
- Profiles in `config/profiles/` can be used to set specific behavioral modes."""

def build_daily_operation_section() -> str:
    return """Recommended daily tasks:
1. Verify configuration: `python -m usa_signal_bot validate-config`
2. Check system health: `python -m usa_signal_bot health`
3. Run maintenance checks: `python -m usa_signal_bot maintenance-check --frequency daily`
4. Execute a local scan (dry-run): `python -m usa_signal_bot scan-dry-run`"""

def build_weekly_maintenance_section() -> str:
    return """Recommended weekly tasks:
1. Run smoke tests: `python -m usa_signal_bot regression-run-smoke`
2. Evaluate system quality: `python -m usa_signal_bot quality-scorecard`
3. Generate maintenance report: `python -m usa_signal_bot maintenance-check --frequency weekly`
4. Create a backup: `python -m usa_signal_bot backup-create --scope reports_only`"""

def build_backup_restore_section() -> str:
    return """Backups are created as zip archives containing system state (excluding secrets).
- Create backup: `python -m usa_signal_bot backup-create --scope config_only`
- Validate backup: `python -m usa_signal_bot backup-validate --backup <path_to_zip>`
- Restore dry-run: `python -m usa_signal_bot restore-dry-run --backup <path_to_zip> --target-dir <preview_dir>`"""

def build_regression_section() -> str:
    return """Regression testing ensures stability against local baselines.
- Run smoke tests: `python -m usa_signal_bot regression-info`
- Run release rehearsal: `python -m usa_signal_bot release-rehearsal`"""

def build_quality_gate_section() -> str:
    return """Quality gates ensure system readiness based on predefined metrics.
- Evaluate acceptance: `python -m usa_signal_bot acceptance-evaluate`"""

def build_paper_trading_section() -> str:
    return """Local simulated paper trading allows realistic execution gap analysis without broker risk.
- View status: `python -m usa_signal_bot paper-info`"""

def build_notifications_section() -> str:
    return """Notifications are sent via Telegram (if configured). Real sending is disabled by default.
- Test notification (dry-run): `python -m usa_signal_bot notification-dispatch-dry-run`"""

def build_troubleshooting_section() -> str:
    return """If the system fails or behaves unexpectedly:
1. Check the logs in `data/logs/` or console output.
2. Ensure data directories exist and are writable.
3. Validate config profile: `python -m usa_signal_bot config-profile-validate --all`"""

def build_safety_limitations_section() -> str:
    return """**CRITICAL SAFETY WARNINGS**
1. This system is for local research only. It is NOT a live trading bot.
2. It does NOT connect to any broker API (no Alpaca, IBKR, etc.).
3. It does NOT generate live or demo orders.
4. The outputs of this system do NOT constitute financial or investment advice.
5. Release packages and runbooks are strictly for local operations and are NOT live approvals."""

def build_command_reference() -> List[Dict[str, Any]]:
    return [
        {"command": "python -m usa_signal_bot smoke", "description": "Run basic smoke tests"},
        {"command": "python -m usa_signal_bot health", "description": "Check system health"},
        {"command": "python -m usa_signal_bot validate-config", "description": "Validate configuration"},
        {"command": "python -m usa_signal_bot release-info", "description": "Show release packaging info"},
        {"command": "python -m usa_signal_bot maintenance-info", "description": "Show maintenance plans"}
    ]

def runbook_to_markdown(runbook: OperatorRunbook) -> str:
    lines = [f"# {runbook.title}", f"*Generated: {runbook.created_at_utc}*\n"]
    for section, content in runbook.sections.items():
        lines.append(f"## {section.replace('_', ' ').title()}")
        lines.append(content)
        lines.append("")

    if runbook.command_reference:
        lines.append("## Command Reference")
        for cmd in runbook.command_reference:
            lines.append(f"- `{cmd['command']}`: {cmd['description']}")

    return "\n".join(lines)

def write_runbook_markdown(path: Path, runbook: OperatorRunbook) -> Path:
    md = runbook_to_markdown(runbook)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(md, encoding='utf-8')
    return path
