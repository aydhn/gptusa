from typing import Any

def detect_config_conflicts(config: dict[str, Any]) -> list[str]:
    conflicts = []
    conflicts.extend(detect_execution_config_conflicts(config))
    conflicts.extend(detect_provider_config_conflicts(config))
    conflicts.extend(detect_notification_config_conflicts(config))
    conflicts.extend(detect_dashboard_scraping_conflicts(config))
    return conflicts

def detect_execution_config_conflicts(config: dict[str, Any]) -> list[str]:
    conflicts = []
    safety = config.get("safety", {})
    if safety.get("allow_broker_execution"):
        conflicts.append("allow_broker_execution cannot be true in Phase 102")
    if safety.get("allow_paper_state_mutation"):
        conflicts.append("allow_paper_state_mutation cannot be true in Phase 102")
    return conflicts

def detect_provider_config_conflicts(config: dict[str, Any]) -> list[str]:
    conflicts = []
    provider = config.get("provider", {})
    if provider.get("allow_paid_api"):
        conflicts.append("allow_paid_api cannot be true in Phase 102")
    return conflicts

def detect_notification_config_conflicts(config: dict[str, Any]) -> list[str]:
    conflicts = []
    safety = config.get("safety", {})
    if safety.get("allow_telegram_real_send"):
        conflicts.append("allow_telegram_real_send cannot be true in Phase 102")
    return conflicts

def detect_dashboard_scraping_conflicts(config: dict[str, Any]) -> list[str]:
    conflicts = []
    safety = config.get("safety", {})
    if safety.get("allow_scraping"):
        conflicts.append("allow_scraping cannot be true in Phase 102")
    if safety.get("allow_dashboard"):
        conflicts.append("allow_dashboard cannot be true in Phase 102")
    return conflicts

def config_conflict_summary(config: dict[str, Any]) -> dict[str, Any]:
    conflicts = detect_config_conflicts(config)
    return {
        "conflict_count": len(conflicts),
        "conflicts": conflicts
    }

def config_conflict_detector_to_text(conflicts: list[str]) -> str:
    lines = ["--- Config Conflicts ---"]
    if not conflicts:
        lines.append("No conflicts detected.")
    else:
        for c in conflicts:
            lines.append(f" - {c}")
    return "\n".join(lines)
