from typing import Any, Dict, List

def build_phase107_provider_runtime_policy() -> Dict[str, Any]:
    return {
        "metadata_only": True,
        "dry_run_only": True,
        "cache_lookup_allowed": True,
        "local_fixture_read_allowed": True,
        "network_enabled_by_default": False,
        "paid_api": False,
        "scraping": False,
        "html_parse": False,
        "broker": False,
        "order": False,
        "paper_mutation": False,
        "telegram_real": False,
        "dashboard": False
    }

def validate_provider_runtime_policy(policy: Dict[str, Any]) -> List[str]:
    errors = []
    if not policy.get("metadata_only", False):
        errors.append("metadata_only must be True")
    if not policy.get("dry_run_only", False):
        errors.append("dry_run_only must be True")
    if not policy.get("cache_lookup_allowed", False):
        errors.append("cache_lookup_allowed must be True")
    if not policy.get("local_fixture_read_allowed", False):
        errors.append("local_fixture_read_allowed must be True")

    if policy.get("network_enabled_by_default", True):
        errors.append("network_enabled_by_default must be False")
    if policy.get("paid_api", True):
        errors.append("paid_api must be False")
    if policy.get("scraping", True):
        errors.append("scraping must be False")
    if policy.get("html_parse", True):
        errors.append("html_parse must be False")
    if policy.get("broker", True):
        errors.append("broker must be False")
    if policy.get("order", True):
        errors.append("order must be False")
    if policy.get("paper_mutation", True):
        errors.append("paper_mutation must be False")
    if policy.get("telegram_real", True):
        errors.append("telegram_real must be False")
    if policy.get("dashboard", True):
        errors.append("dashboard must be False")

    return errors

def provider_runtime_policy_allows_network(policy: Dict[str, Any]) -> bool:
    return policy.get("network_enabled_by_default", False)

def provider_runtime_policy_allows_paid_api(policy: Dict[str, Any]) -> bool:
    return policy.get("paid_api", False)

def provider_runtime_policy_to_text(policy: Dict[str, Any]) -> str:
    lines = [
        "=== Provider Runtime Policy ==="
    ]
    for k, v in policy.items():
        lines.append(f"{k}: {v}")
    return "\n".join(lines)
