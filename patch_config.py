import yaml
from pathlib import Path

config_path = Path("config/default.yaml")

with open(config_path, "r") as f:
    config = yaml.safe_load(f)

if "regime_feature_engineering" not in config:
    config["regime_feature_engineering"] = {
        "enabled": True,
        "current_phase": 127,
        "final_phase": 160,
        "require_phase126_regime_foundation": True,
        "market_state_metrics_enabled": True,
        "rolling_market_state_metrics_enabled": True,
        "cross_sectional_market_state_metrics_enabled": True,
        "regime_feature_table_enabled": True,
        "unsupervised_candidate_preparation_enabled": True,
        "candidate_readiness_gate_enabled": True,
        "write_regime_feature_engineering_reports": True,
        "warn_not_investment_advice": True,
        "warn_phase127_is_not_activation": True,
        "warn_candidates_are_not_predictions": True,
        "warn_candidates_are_not_trade_signals": True,
    }

if "phase127_regime_policy" not in config:
    config["phase127_regime_policy"] = {
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
        "allow_heavy_ml_dependencies": False,
        "produce_trade_signals": False,
        "produce_order_decisions": False,
        "produce_portfolio_weights": False,
        "produce_investment_advice": False,
        "strategy_activation_allowed": False,
    }

if "phase127_market_state_metrics" not in config:
    config["phase127_market_state_metrics"] = {
        "enabled": True,
        "default_windows": [20, 60, 120],
        "build_cross_sectional_metrics": True,
        "preserve_warmup_nulls": True,
        "write_feature_tables": True,
        "overwrite_feature_tables_default": False,
    }

if "phase127_candidate_preparation" not in config:
    config["phase127_candidate_preparation"] = {
        "enabled": True,
        "method": "DETERMINISTIC_RULE_TEMPLATE",
        "produce_model_predictions": False,
        "train_models": False,
        "fit_clustering_models": False,
        "candidate_scores_are_metadata_only": True,
        "ready_for_phase128_allowed": True,
    }

if "phase127_notifications" not in config:
    config["phase127_notifications"] = {
        "enabled": True,
        "dry_run": True,
        "preview_only": True,
        "telegram_real_send": False,
    }


with open(config_path, "w") as f:
    yaml.dump(config, f, sort_keys=False)
