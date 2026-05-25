print("Adding config...")
with open("usa_signal_bot/core/config_schema.py", "r") as f:
    content = f.read()

import re

ADDITION = """
@dataclass
class Phase107FetchPolicyConfig:
    dry_run_only: bool = True
    metadata_only_default: bool = True
    cache_lookup_dry_run_allowed: bool = True
    local_fixture_read_allowed: bool = True
    network_enabled_by_default: bool = False
    paid_api_enabled: bool = False
    scraping_enabled: bool = False
    html_parse_enabled: bool = False
    broker_execution_enabled: bool = False
    order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    telegram_real_send_enabled: bool = False
    dashboard_enabled: bool = False
    credential_required_now: bool = False

@dataclass
class Phase107ProviderAdaptersConfig:
    yfinance_adapter_enabled: bool = True
    stooq_adapter_enabled: bool = True
    local_csv_adapter_enabled: bool = True
    yfinance_network_default: bool = False
    stooq_network_default: bool = False
    local_csv_network_default: bool = False

@dataclass
class Phase107NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False

@dataclass
class DataProviderRuntimeConfig:
    enabled: bool = True
    current_phase: int = 107
    final_phase: int = 160
    require_phase106_provider_abstraction: bool = True
    provider_runtime_ready: bool = True
    adapter_contract_tests_enabled: bool = True
    cache_aware_dry_run_enabled: bool = True
    write_provider_runtime_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase107_is_not_activation: bool = True
    warn_no_real_network_in_tests: bool = True
"""

if "DataProviderRuntimeConfig" not in content:
    content = content.replace(
        "class AppConfig:",
        ADDITION + "\n@dataclass\nclass AppConfig:\n    data_provider_runtime: DataProviderRuntimeConfig = field(default_factory=DataProviderRuntimeConfig)\n    phase107_fetch_policy: Phase107FetchPolicyConfig = field(default_factory=Phase107FetchPolicyConfig)\n    phase107_provider_adapters: Phase107ProviderAdaptersConfig = field(default_factory=Phase107ProviderAdaptersConfig)\n    phase107_notifications: Phase107NotificationsConfig = field(default_factory=Phase107NotificationsConfig)"
    )
    with open("usa_signal_bot/core/config_schema.py", "w") as f:
        f.write(content)
