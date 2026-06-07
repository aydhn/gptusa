import re

with open("usa_signal_bot/core/config_schema.py", "r") as f:
    content = f.read()

append_str = """

@dataclass
class BacktestClosureConfig:
    enabled: bool = True
    current_phase: int = 152
    final_phase: int = 160
    require_phase151_stress_robustness: bool = True
    stress_robustness_ingestion_enabled: bool = True
    cross_phase_artifact_loader_enabled: bool = True
    artifact_lineage_enabled: bool = True
    artifact_availability_audit_enabled: bool = True
    determinism_compliance_audit_enabled: bool = True
    safety_compliance_audit_enabled: bool = True
    research_boundary_audit_enabled: bool = True
    metric_inventory_enabled: bool = True
    risk_note_inventory_enabled: bool = True
    robustness_evidence_enabled: bool = True
    acceptance_summary_enabled: bool = True
    closure_blocker_detector_enabled: bool = True
    closure_warning_collector_enabled: bool = True
    final_audit_report_enabled: bool = True
    band_closure_certificate_enabled: bool = True
    phase153_handoff_contract_enabled: bool = True
    phase153_handoff_package_enabled: bool = True
    handoff_safety_boundary_enabled: bool = True
    phase153_readiness_gate_enabled: bool = True
    write_backtest_closure_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_closure_is_not_deployment: bool = True
    warn_handoff_is_read_only: bool = True
    warn_no_portfolio_construction_in_phase152: bool = True


@dataclass
class Phase152ClosurePolicyConfig:
    compute_values_local_only: bool = True
    research_data_only: bool = True
    offline_backtest_research_only: bool = True
    local_fixture_only_default: bool = True
    read_only_stress_artifacts: bool = True
    read_only_cross_phase_artifacts: bool = True
    allow_band_closure: bool = True
    allow_phase153_handoff_package: bool = True
    allow_portfolio_construction: bool = False
    allow_position_sizing: bool = False
    allow_portfolio_optimization: bool = False
    allow_portfolio_allocation_output: bool = False
    allow_target_weights: bool = False
    allow_capital_deployment: bool = False
    allow_network: bool = False
    allow_paid_api: bool = False
    allow_scraping: bool = False
    allow_html_parsing: bool = False
    allow_broker: bool = False
    allow_real_order_creation: bool = False
    allow_paper_mutation: bool = False
    allow_telegram_real_send: bool = False
    allow_dashboard: bool = False
    allow_deployment: bool = False
    allow_live_trading: bool = False
    allow_paper_trading: bool = False
    allow_strategy_activation: bool = False
    allow_scheduler: bool = False
    allow_background_daemon: bool = False
    produce_live_signals: bool = False
    produce_order_decisions: bool = False
    produce_portfolio_weights: bool = False
    produce_investment_advice: bool = False


@dataclass
class Phase152HandoffDefaultsConfig:
    start_phase: int = 146
    end_phase: int = 152
    next_phase: int = 153
    final_phase: int = 160
    read_only_handoff: bool = True
    include_metric_inventory: bool = True
    include_risk_notes: bool = True
    include_robustness_scorecard: bool = True
    include_artifact_lineage: bool = True
    include_safety_summary: bool = True
    require_no_portfolio_fields: bool = True
    require_deterministic_hashes: bool = True


@dataclass
class Phase152NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False
"""

if "BacktestClosureConfig" not in content:
    content += append_str

    with open("usa_signal_bot/core/config_schema.py", "w") as f:
        f.write(content)
