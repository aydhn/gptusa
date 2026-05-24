with open("config/default.yaml", "r") as f:
    content = f.read()

new_config = """
advanced_runtime:
  enabled: true
  current_phase: 102
  final_phase: 160
  require_phase101_transition_review: true
  normalize_runtime_registry: true
  normalize_config_surface: true
  provider_interfaces_ready: true
  allow_activation: false
  allow_active_paper: false
  allow_broker_execution: false
  allow_paper_state_mutation: false
  allow_telegram_real_send: false
  allow_scraping: false
  allow_dashboard: false
  allow_paid_api: false
  write_runtime_registry_reports: true
  warn_not_investment_advice: true
  warn_phase102_is_not_activation: true

phase102_runtime_modes:
  default_mode: "PROVIDER_READY_NO_FETCH"
  offline_metadata_enabled: true
  local_read_only_enabled: true
  local_compute_only_enabled: true
  provider_ready_no_fetch_enabled: true
  provider_network_fetch_default: false
  active_paper_enabled: false
  broker_execution_enabled: false

phase102_provider_contracts:
  enabled: true
  metadata_only_by_default: true
  network_disabled_by_default: true
  cache_allowed: true
  paid_api_blocked: true
  scraping_blocked: true
  broker_blocked: true
  order_blocked: true
  paper_mutation_blocked: true
  telegram_real_send_blocked: true

phase102_config_surface:
  enabled: true
  normalize_missing_safety_keys: true
  block_on_conflict: true
  block_on_unsafe_value: true
  generate_migration_hints: true

phase102_notifications:
  enabled: true
  dry_run: true
  preview_only: true
  telegram_real_send: false
"""

if "advanced_runtime:" not in content:
    content = content + "\n" + new_config + "\n"
    with open("config/default.yaml", "w") as f:
        f.write(content)
