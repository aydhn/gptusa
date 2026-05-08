from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List
import yaml
import uuid
from usa_signal_bot.core.enums import ConfigProfileType, ReleaseValidationStatus

@dataclass
class ConfigProfile:
    profile_id: str
    name: str
    profile_type: ConfigProfileType
    description: str
    config_path: str
    safety_notes: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ConfigProfileValidationResult:
    profile_id: str
    name: str
    status: ReleaseValidationStatus
    checked_at_utc: str
    config_path: str
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def default_config_profiles(project_root: Path) -> List[ConfigProfile]:
    return [
        ConfigProfile(
            profile_id=f"prof_{uuid.uuid4().hex[:8]}",
            name="research",
            profile_type=ConfigProfileType.RESEARCH,
            description="Safe local research mode. Paper and notifications disabled.",
            config_path="config/profiles/research.yaml",
            safety_notes=["Broker flags must be false.", "Telegram real send must be false."]
        ),
        ConfigProfile(
            profile_id=f"prof_{uuid.uuid4().hex[:8]}",
            name="paper_dry_run",
            profile_type=ConfigProfileType.PAPER_DRY_RUN,
            description="Paper trading enabled in dry-run mode.",
            config_path="config/profiles/paper_dry_run.yaml",
            safety_notes=["Broker flags must be false."]
        ),
        ConfigProfile(
            profile_id=f"prof_{uuid.uuid4().hex[:8]}",
            name="regression_only",
            profile_type=ConfigProfileType.REGRESSION_ONLY,
            description="Strict regression mode. No external data fetch.",
            config_path="config/profiles/regression_only.yaml",
            safety_notes=["Network fetch disabled.", "Broker flags must be false."]
        ),
        ConfigProfile(
            profile_id=f"prof_{uuid.uuid4().hex[:8]}",
            name="notification_dry_run",
            profile_type=ConfigProfileType.NOTIFICATION_DRY_RUN,
            description="Notifications enabled but set to log-only dry-run.",
            config_path="config/profiles/notification_dry_run.yaml",
            safety_notes=["Telegram real send must be false."]
        )
    ]

def write_default_config_profiles(project_root: Path) -> List[Path]:
    profiles = default_config_profiles(project_root)
    paths = []

    # research.yaml
    p1 = project_root / profiles[0].config_path
    p1.parent.mkdir(parents=True, exist_ok=True)
    p1.write_text(yaml.dump({"paper": {"enabled": False}, "telegram": {"allow_real_send": False}, "runtime": {"default_mode": "manual_once"}}))
    paths.append(p1)

    # paper_dry_run.yaml
    p2 = project_root / profiles[1].config_path
    p2.write_text(yaml.dump({"paper": {"enabled": True, "execution_mode": "DRY_RUN"}, "telegram": {"allow_real_send": False}}))
    paths.append(p2)

    # regression_only.yaml
    p3 = project_root / profiles[2].config_path
    p3.write_text(yaml.dump({"market_scan": {"refresh_data_default": False}, "paper": {"enabled": False}, "telegram": {"allow_real_send": False}}))
    paths.append(p3)

    # notification_dry_run.yaml
    p4 = project_root / profiles[3].config_path
    p4.write_text(yaml.dump({"telegram": {"allow_real_send": False}, "notifications": {"enabled": True}, "market_scan": {"notification_channel_default": "dry_run"}}))
    paths.append(p4)

    return paths

def load_config_profile(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return yaml.safe_load(f) or {}

def validate_config_profile(profile: ConfigProfile) -> ConfigProfileValidationResult:
    warnings = []
    errors = []
    path = Path('.') / profile.config_path
    if not path.exists():
        errors.append("Profile config file missing.")
        return ConfigProfileValidationResult(profile.profile_id, profile.name, ReleaseValidationStatus.FAILED, datetime.now(timezone.utc).isoformat(), str(path), warnings, errors)

    try:
        data = load_config_profile(path)
        # Check safety flags
        tg = data.get("telegram", {})
        if tg.get("allow_real_send") is True:
            errors.append("telegram.allow_real_send must be false.")

        paper = data.get("paper", {})
        if paper.get("execution_mode") == "LIVE":
            errors.append("paper.execution_mode cannot be LIVE.")

        # Dashboard/Broker checks would go here if they existed in raw dict

    except Exception as e:
        errors.append(f"Failed to parse YAML: {e}")

    status = ReleaseValidationStatus.FAILED if errors else (ReleaseValidationStatus.WARNING if warnings else ReleaseValidationStatus.PASSED)

    return ConfigProfileValidationResult(
        profile.profile_id, profile.name, status, datetime.now(timezone.utc).isoformat(), str(path), warnings, errors
    )

def validate_all_config_profiles(project_root: Path) -> List[ConfigProfileValidationResult]:
    profiles = default_config_profiles(project_root)
    return [validate_config_profile(p) for p in profiles]

def config_profile_to_dict(profile: ConfigProfile) -> dict:
    return {"profile_id": profile.profile_id, "name": profile.name, "type": profile.profile_type.value, "config_path": profile.config_path}

def config_profile_validation_result_to_dict(result: ConfigProfileValidationResult) -> dict:
    return {"profile_id": result.profile_id, "name": result.name, "status": result.status.value, "errors": result.errors}

def config_profiles_to_text(profiles: List[ConfigProfile]) -> str:
    lines = ["--- Config Profiles ---"]
    for p in profiles:
        lines.append(f"{p.name} ({p.profile_type.value}): {p.config_path}")
    return "\n".join(lines)

def config_profile_validation_results_to_text(results: List[ConfigProfileValidationResult]) -> str:
    lines = ["--- Config Profile Validation ---"]
    for r in results:
        lines.append(f"{r.name}: {r.status.value} - Errors: {len(r.errors)}")
    return "\n".join(lines)
