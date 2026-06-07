import sys
import os

with open("config/default.yaml", "r") as f:
    content = f.read()

append_str = """
backtest_closure:
  enabled: true
  current_phase: 152
  final_phase: 160
  require_phase151_stress_robustness: true
  stress_robustness_ingestion_enabled: true
  cross_phase_artifact_loader_enabled: true
  artifact_lineage_enabled: true
  artifact_availability_audit_enabled: true
  determinism_compliance_audit_enabled: true
  safety_compliance_audit_enabled: true
  research_boundary_audit_enabled: true
  metric_inventory_enabled: true
  risk_note_inventory_enabled: true
  robustness_evidence_enabled: true
  acceptance_summary_enabled: true
  closure_blocker_detector_enabled: true
  closure_warning_collector_enabled: true
  final_audit_report_enabled: true
  band_closure_certificate_enabled: true
  phase153_handoff_contract_enabled: true
  phase153_handoff_package_enabled: true
  handoff_safety_boundary_enabled: true
  phase153_readiness_gate_enabled: true
  write_backtest_closure_reports: true
  warn_not_investment_advice: true
  warn_closure_is_not_deployment: true
  warn_handoff_is_read_only: true
  warn_no_portfolio_construction_in_phase152: true

phase152_closure_policy:
  compute_values_local_only: true
  research_data_only: true
  offline_backtest_research_only: true
  local_fixture_only_default: true
  read_only_stress_artifacts: true
  read_only_cross_phase_artifacts: true
  allow_band_closure: true
  allow_phase153_handoff_package: true
  allow_portfolio_construction: false
  allow_position_sizing: false
  allow_portfolio_optimization: false
  allow_portfolio_allocation_output: false
  allow_target_weights: false
  allow_capital_deployment: false
  allow_network: false
  allow_paid_api: false
  allow_scraping: false
  allow_html_parsing: false
  allow_broker: false
  allow_real_order_creation: false
  allow_paper_mutation: false
  allow_telegram_real_send: false
  allow_dashboard: false
  allow_deployment: false
  allow_live_trading: false
  allow_paper_trading: false
  allow_strategy_activation: false
  allow_scheduler: false
  allow_background_daemon: false
  produce_live_signals: false
  produce_order_decisions: false
  produce_portfolio_weights: false
  produce_investment_advice: false

phase152_handoff_defaults:
  start_phase: 146
  end_phase: 152
  next_phase: 153
  final_phase: 160
  read_only_handoff: true
  include_metric_inventory: true
  include_risk_notes: true
  include_robustness_scorecard: true
  include_artifact_lineage: true
  include_safety_summary: true
  require_no_portfolio_fields: true
  require_deterministic_hashes: true

phase152_notifications:
  enabled: true
  dry_run: true
  preview_only: true
  telegram_real_send: false
"""

if "backtest_closure:" not in content:
    with open("config/default.yaml", "a") as f:
        f.write(append_str)
