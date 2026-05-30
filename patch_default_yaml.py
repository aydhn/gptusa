import yaml

file_path = "config/default.yaml"
with open(file_path, "r") as f:
    data = yaml.safe_load(f)

if "regime_research_freeze" not in data:
    data["regime_research_freeze"] = {
        "enabled": True,
        "current_phase": 134,
        "final_phase": 160,
        "require_phase133_regime_monitoring": True,
        "monitoring_artifact_loader_enabled": True,
        "monitoring_validation_enabled": True,
        "drift_report_enabled": True,
        "drift_report_qa_enabled": True,
        "freeze_package_enabled": True,
        "freeze_readiness_gate_enabled": True,
        "write_research_freeze_reports": True,
        "warn_not_investment_advice": True,
        "warn_phase134_is_not_activation": True,
        "warn_freeze_package_is_not_deployment": True,
    }

if "phase134_freeze_policy" not in data:
    data["phase134_freeze_policy"] = {
        "compute_values_local_only": True,
        "research_data_only": True,
        "local_fixture_only_default": True,
        "allow_network": False,
        "allow_paid_api": False,
        "allow_scraping": False,
        "allow_html_parsing": False,
        "allow_broker": False,
        "allow_order": False,
        "allow_paper_mutation": False,
        "allow_telegram_real_send": False,
        "allow_dashboard": False,
        "allow_deployment": False,
        "allow_model_training": False,
        "allow_model_prediction": False,
        "allow_heavy_ml_dependencies": False,
        "allow_background_daemon": False,
        "allow_scheduler": False,
        "produce_trade_signals": False,
        "produce_order_decisions": False,
        "produce_portfolio_weights": False,
        "produce_investment_advice": False,
        "strategy_activation_allowed": False,
    }

if "phase134_drift_report_qa" not in data:
    data["phase134_drift_report_qa"] = {
        "enabled": True,
        "require_qa_pass": True,
        "block_investment_advice_language": True,
        "block_trade_signal_language": True,
        "block_order_decision_language": True,
        "block_portfolio_allocation_language": True,
        "block_guarantee_language": True,
        "block_broker_execution_language": True,
        "block_deployment_language": True,
        "block_live_monitoring_language": True,
        "overwrite_reports_default": False,
    }

if "phase134_freeze_package" not in data:
    data["phase134_freeze_package"] = {
        "enabled": True,
        "package_version": "phase134.v1",
        "require_required_artifact_coverage": True,
        "require_package_hash": True,
        "require_manifest_hash": True,
        "ready_for_phase135_allowed": True,
    }

if "phase134_notifications" not in data:
    data["phase134_notifications"] = {
        "enabled": True,
        "dry_run": True,
        "preview_only": True,
        "telegram_real_send": False,
    }

with open(file_path, "w") as f:
    yaml.dump(data, f, default_flow_style=False, sort_keys=False)
