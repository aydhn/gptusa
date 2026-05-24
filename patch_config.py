import re

with open("usa_signal_bot/core/config_schema.py", "r") as f:
    content = f.read()

new_classes = """
@dataclass
class AdvancedRuntimeConfig:
    enabled: bool = True
    current_phase: int = 102
    final_phase: int = 160
    require_phase101_transition_review: bool = True
    normalize_runtime_registry: bool = True
    normalize_config_surface: bool = True
    provider_interfaces_ready: bool = True
    allow_activation: bool = False
    allow_active_paper: bool = False
    allow_broker_execution: bool = False
    allow_paper_state_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_scraping: bool = False
    allow_dashboard: bool = False
    allow_paid_api: bool = False
    write_runtime_registry_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase102_is_not_activation: bool = True

@dataclass
class Phase102RuntimeModesConfig:
    default_mode: str = "PROVIDER_READY_NO_FETCH"
    offline_metadata_enabled: bool = True
    local_read_only_enabled: bool = True
    local_compute_only_enabled: bool = True
    provider_ready_no_fetch_enabled: bool = True
    provider_network_fetch_default: bool = False
    active_paper_enabled: bool = False
    broker_execution_enabled: bool = False

@dataclass
class Phase102ProviderContractsConfig:
    enabled: bool = True
    metadata_only_by_default: bool = True
    network_disabled_by_default: bool = True
    cache_allowed: bool = True
    paid_api_blocked: bool = True
    scraping_blocked: bool = True
    broker_blocked: bool = True
    order_blocked: bool = True
    paper_mutation_blocked: bool = True
    telegram_real_send_blocked: bool = True

@dataclass
class Phase102ConfigSurfaceConfig:
    enabled: bool = True
    normalize_missing_safety_keys: bool = True
    block_on_conflict: bool = True
    block_on_unsafe_value: bool = True
    generate_migration_hints: bool = True

@dataclass
class Phase102NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False
"""

if "class AdvancedRuntimeConfig" not in content:
    content = content + "\n" + new_classes + "\n"
    with open("usa_signal_bot/core/config_schema.py", "w") as f:
        f.write(content)
