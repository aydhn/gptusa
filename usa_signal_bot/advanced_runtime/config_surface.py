from typing import Any
from usa_signal_bot.advanced_runtime.phase102_models import ConfigSurfaceRecord
from usa_signal_bot.core.enums import ConfigSurfaceDomain, ConfigSurfaceStatus

def required_config_surface_domains() -> list[ConfigSurfaceDomain]:
    return [
        ConfigSurfaceDomain.SAFETY,
        ConfigSurfaceDomain.RUNTIME_MODE,
        ConfigSurfaceDomain.PROVIDER,
        ConfigSurfaceDomain.DATA_CACHE,
        ConfigSurfaceDomain.OBSERVABILITY,
        ConfigSurfaceDomain.NOTIFICATION,
        ConfigSurfaceDomain.STORAGE,
        ConfigSurfaceDomain.CLI,
        ConfigSurfaceDomain.HEALTH
    ]

def required_keys_for_domain(domain: ConfigSurfaceDomain) -> list[str]:
    keys = {
        ConfigSurfaceDomain.SAFETY: [
            "allow_broker_execution", "allow_paper_state_mutation",
            "allow_telegram_real_send", "allow_scraping", "allow_dashboard"
        ],
        ConfigSurfaceDomain.RUNTIME_MODE: ["default_mode", "allowed_modes", "blocked_modes"],
        ConfigSurfaceDomain.PROVIDER: ["provider_ready", "allow_paid_api", "allow_scraping", "allow_network_fetch_default"],
        ConfigSurfaceDomain.DATA_CACHE: ["enabled", "data_root", "cache_read_only_default"],
        ConfigSurfaceDomain.OBSERVABILITY: ["enabled", "local_only"],
        ConfigSurfaceDomain.NOTIFICATION: ["dry_run", "telegram_real_send"],
        ConfigSurfaceDomain.STORAGE: ["data_root"],
        ConfigSurfaceDomain.CLI: ["enabled"],
        ConfigSurfaceDomain.HEALTH: ["enabled"]
    }
    return keys.get(domain, [])

def build_config_surface_records(config: dict[str, Any]) -> list[ConfigSurfaceRecord]:
    records = []

    # Minimal stub implementation for building records from an arbitrary config structure.
    # In a full implementation, you'd map sections of the config to the domains.
    for domain in required_config_surface_domains():
        req_keys = required_keys_for_domain(domain)
        records.append(
            ConfigSurfaceRecord(
                domain=domain,
                status=ConfigSurfaceStatus.CLEAN,
                required_keys=req_keys,
                present_keys=[],
                missing_keys=req_keys,
                unsafe_keys=[],
                conflict_keys=[],
                normalized_values={},
                warnings=[],
                errors=[],
                metadata={}
            )
        )
    return records

def config_surface_summary(records: list[ConfigSurfaceRecord]) -> dict[str, Any]:
    return {
        "total_domains": len(records),
        "clean_domains": [r.domain.value for r in records if r.status == ConfigSurfaceStatus.CLEAN],
        "needs_normalization": [r.domain.value for r in records if r.status == ConfigSurfaceStatus.NEEDS_NORMALIZATION]
    }

def config_surface_to_text(records: list[ConfigSurfaceRecord]) -> str:
    lines = ["--- Config Surface ---"]
    for r in records:
        lines.append(f"Domain: {r.domain.value} | Status: {r.status.value}")
    return "\n".join(lines)
