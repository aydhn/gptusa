from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import datetime
import uuid
from usa_signal_bot.core.enums import SafetyMonitorStatus
from usa_signal_bot.core.config import config_to_dict

@dataclass
class SafetyFlagCheck:
    name: str
    status: SafetyMonitorStatus
    expected: Any
    observed: Any
    message: str

@dataclass
class SafetyMonitorReport:
    report_id: str
    created_at_utc: str
    status: SafetyMonitorStatus
    checks: List[SafetyFlagCheck]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def check_broker_flags_disabled(config_dict: Dict[str, Any]) -> SafetyFlagCheck:
    obs = config_dict.get("project", {}).get("broker_integration_enabled", False)
    st = SafetyMonitorStatus.SAFE if not obs else SafetyMonitorStatus.BLOCKED
    return SafetyFlagCheck(
        name="broker_flags_disabled",
        status=st,
        expected=False,
        observed=obs,
        message="Broker integration must be disabled." if st == SafetyMonitorStatus.BLOCKED else "OK"
    )

def check_live_demo_flags_disabled(config_dict: Dict[str, Any]) -> SafetyFlagCheck:
    obs1 = config_dict.get("project", {}).get("live_order_enabled", False)
    obs2 = config_dict.get("project", {}).get("demo_order_enabled", False)
    obs = obs1 or obs2
    st = SafetyMonitorStatus.SAFE if not obs else SafetyMonitorStatus.BLOCKED
    return SafetyFlagCheck(
        name="live_demo_flags_disabled",
        status=st,
        expected=False,
        observed=obs,
        message="Live and demo orders must be disabled." if st == SafetyMonitorStatus.BLOCKED else "OK"
    )

def check_telegram_real_send_disabled(config_dict: Dict[str, Any]) -> SafetyFlagCheck:
    obs = config_dict.get("telegram", {}).get("allow_real_send", False)
    st = SafetyMonitorStatus.SAFE if not obs else SafetyMonitorStatus.WARNING
    return SafetyFlagCheck(
        name="telegram_real_send_disabled",
        status=st,
        expected=False,
        observed=obs,
        message="Telegram real send is enabled. Proceed with caution." if st == SafetyMonitorStatus.WARNING else "OK"
    )

def check_dashboard_disabled(config_dict: Dict[str, Any]) -> SafetyFlagCheck:
    obs = config_dict.get("observability", {}).get("dashboard_enabled", False)
    st = SafetyMonitorStatus.SAFE if not obs else SafetyMonitorStatus.WARNING
    return SafetyFlagCheck(
        name="dashboard_disabled",
        status=st,
        expected=False,
        observed=obs,
        message="Dashboard should be disabled for local mode." if st == SafetyMonitorStatus.WARNING else "OK"
    )

def check_scraping_disabled(config_dict: Dict[str, Any]) -> SafetyFlagCheck:
    obs = config_dict.get("providers", {}).get("allow_web_scraping", False)
    st = SafetyMonitorStatus.SAFE if not obs else SafetyMonitorStatus.BLOCKED
    return SafetyFlagCheck(
        name="scraping_disabled",
        status=st,
        expected=False,
        observed=obs,
        message="Web scraping must be disabled." if st == SafetyMonitorStatus.BLOCKED else "OK"
    )

def build_safety_monitor_report(config: Any = None, config_dict: Optional[Dict[str, Any]] = None) -> SafetyMonitorReport:
    d = config_dict
    if d is None and config is not None:
        try:
            d = config_to_dict(config)
        except Exception:
            d = {}
    if d is None: d = {}

    c1 = check_broker_flags_disabled(d)
    c2 = check_live_demo_flags_disabled(d)
    c3 = check_telegram_real_send_disabled(d)
    c4 = check_dashboard_disabled(d)
    c5 = check_scraping_disabled(d)

    checks = [c1, c2, c3, c4, c5]

    st = SafetyMonitorStatus.SAFE
    for c in checks:
        if c.status == SafetyMonitorStatus.BLOCKED:
            st = SafetyMonitorStatus.BLOCKED
            break
        elif c.status == SafetyMonitorStatus.WARNING:
            if st != SafetyMonitorStatus.BLOCKED:
                st = SafetyMonitorStatus.WARNING

    return SafetyMonitorReport(
        report_id=f"safe_{uuid.uuid4().hex[:8]}",
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        status=st,
        checks=checks
    )

def safety_flag_check_to_dict(check: SafetyFlagCheck) -> dict:
    from dataclasses import asdict
    return asdict(check)

def safety_monitor_report_to_dict(report: SafetyMonitorReport) -> dict:
    from dataclasses import asdict
    d = asdict(report)
    d["checks"] = [safety_flag_check_to_dict(c) for c in report.checks]
    return d

def safety_monitor_report_to_text(report: SafetyMonitorReport) -> str:
    lines = [
        f"--- Safety Monitor Report ---",
        f"Status: {report.status.value}",
        "Checks:"
    ]
    for c in report.checks:
        lines.append(f"  - {c.name}: {c.status.value} ({c.message})")
    return "\n".join(lines)
