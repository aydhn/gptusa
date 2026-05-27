from typing import Any

def build_default_factor_retention_policy() -> dict[str, Any]:
    return {
        "keep_latest_versions": 20,
        "keep_latest_snapshots": 20,
        "allow_manual_cleanup_only": True,
        "never_delete_without_manifest": True,
        "preserve_rollback_candidate": True,
        "local_filesystem_only": True,
        "no_cloud_sync_required": True,
        "no_auto_deployment": True
    }

def validate_factor_retention_policy(policy: dict[str, Any]) -> list[str]:
    return []

def factor_retention_policy_summary(policy: dict[str, Any]) -> dict[str, Any]:
    return {"keep_latest_versions": policy.get("keep_latest_versions")}

def factor_retention_policy_to_text(policy: dict[str, Any]) -> str:
    return "Retention Policy configured."
