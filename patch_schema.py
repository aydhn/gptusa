import re
from pathlib import Path

path = Path("usa_signal_bot/core/config_schema.py")
content = path.read_text()

dataclasses_str = """
@dataclass
class FullSystemIntegrationConfig:
    enabled: bool = True
    current_phase: int = 158
    final_phase: int = 160
    require_phase157_portfolio_risk_handoff: bool = True
    phase158_handoff_ingestion_enabled: bool = True
    artifact_loader_enabled: bool = True
    integration_input_resolver_enabled: bool = True
    artifact_inventory_enabled: bool = True
    dependency_graph_enabled: bool = True
    boundary_contract_enabled: bool = True
    e2e_rehearsal_plan_enabled: bool = True
    dry_run_rehearsal_executor_enabled: bool = True
    acceptance_result_enabled: bool = True
    schema_compatibility_report_enabled: bool = True
    cli_integration_report_enabled: bool = True
    config_integration_report_enabled: bool = True
    storage_integration_report_enabled: bool = True
    health_integration_report_enabled: bool = True
    quality_observability_report_enabled: bool = True
    notification_dry_run_report_enabled: bool = True
    safety_boundary_enabled: bool = True
    final_delivery_preparation_checklist_enabled: bool = True
    phase159_readiness_gate_enabled: bool = True
    write_full_system_integration_reports: bool = True
    warn_integration_only: bool = True
    warn_dry_run_only: bool = True
    warn_not_deployment_approval: bool = True
    warn_not_trading_approval: bool = True
    warn_not_investment_advice: bool = True

@dataclass
class Phase158IntegrationPolicyConfig:
    compute_values_local_only: bool = True
    research_data_only: bool = True
    integration_only: bool = True
    dry_run_only: bool = True
    local_fixture_only_default: bool = True
    read_only_phase158_handoff: bool = True
    allow_full_system_integration: bool = True
    allow_e2e_rehearsal: bool = True
    allow_local_artifact_write: bool = True
    allow_live_trading: bool = False
    allow_paper_state_mutation: bool = False
    allow_broker_execution: bool = False
    allow_real_order_creation: bool = False
    allow_telegram_real_send: bool = False
    allow_strategy_activation: bool = False
    allow_deployment: bool = False
    allow_production_patch: bool = False
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_dashboard: bool = False
    allow_daemon: bool = False
    allow_scheduler: bool = False
    allow_actual_target_weights: bool = False
    allow_actual_allocation: bool = False
    allow_order_size: bool = False
    allow_capital_deployment: bool = False
    produce_live_signals: bool = False
    produce_order_decisions: bool = False
    produce_investment_advice: bool = False

@dataclass
class Phase158RehearsalDefaultsConfig:
    deterministic_seed: int = 158
    dry_run: bool = True
    preview_only: bool = True
    local_fixture_only: bool = True
    no_real_side_effects: bool = True
    no_network: bool = True
    no_paper_mutation: bool = True
    no_broker_execution: bool = True
    no_real_orders: bool = True
    no_telegram_real_send: bool = True
    no_deployment: bool = True
    require_deterministic_hashes: bool = True

@dataclass
class Phase158NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False
"""

if "FullSystemIntegrationConfig" not in content:
    # Safely insert before the AppConfig
    content = content.replace("@dataclass\nclass AppConfig:", dataclasses_str + "\n@dataclass\nclass AppConfig:")

    # Add fields inside AppConfig
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if "class AppConfig:" in line:
            # find first field
            for j in range(i+1, len(lines)):
                if ":" in lines[j] and not lines[j].strip().startswith("#"):
                    fields = [
                        "    full_system_integration: FullSystemIntegrationConfig = field(default_factory=FullSystemIntegrationConfig)",
                        "    phase158_integration_policy: Phase158IntegrationPolicyConfig = field(default_factory=Phase158IntegrationPolicyConfig)",
                        "    phase158_rehearsal_defaults: Phase158RehearsalDefaultsConfig = field(default_factory=Phase158RehearsalDefaultsConfig)",
                        "    phase158_notifications: Phase158NotificationsConfig = field(default_factory=Phase158NotificationsConfig)"
                    ]
                    for field_str in reversed(fields):
                        lines.insert(j, field_str)
                    break
            break

    content = "\n".join(lines)
    path.write_text(content)

