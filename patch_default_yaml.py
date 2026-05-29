import yaml

with open("config/default.yaml", "r") as f:
    config = yaml.safe_load(f)

if "regime_labeling" not in config:
    config["regime_labeling"] = {
        "enabled": True,
        "current_phase": 128,
        "final_phase": 160,
        "require_phase127_regime_feature_engineering": True,
        "heuristic_labeling_enabled": True,
        "rolling_regime_windows_enabled": True,
        "candidate_validation_enabled": True,
        "label_stability_enabled": True,
        "readiness_gate_enabled": True,
        "write_regime_labeling_reports": True,
        "warn_not_investment_advice": True,
        "warn_phase128_is_not_activation": True,
        "warn_labels_are_not_trade_signals": True,
        "warn_labels_are_not_model_predictions": True,
        "policy": {
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
            "produce_trade_signals": False,
            "produce_order_decisions": False,
            "produce_portfolio_weights": False,
            "produce_investment_advice": False,
            "strategy_activation_allowed": False
        },
        "heuristic_labeling": {
            "enabled": True,
            "minimum_score_threshold": 40.0,
            "minimum_score_gap": 5.0,
            "fallback_label": "unknown_regime",
            "mixed_label": "mixed_regime",
            "unknown_label": "unknown_regime",
            "conflict_policy": "fallback_to_mixed_or_unknown",
            "write_labeled_tables": True,
            "overwrite_labeled_tables_default": False
        },
        "rolling_windows": {
            "enabled": True,
            "windows": [20, 60, 120],
            "min_periods_ratio": 0.5,
            "preserve_warmup_nulls": True,
            "build_stability_profiles": True
        },
        "candidate_validation": {
            "enabled": True,
            "require_candidate_definitions": True,
            "require_candidate_scores": True,
            "require_taxonomy_alignment": True,
            "require_no_model_training": True,
            "require_no_model_prediction": True,
            "ready_for_phase129_allowed": True
        },
        "notifications": {
            "enabled": True,
            "dry_run": True,
            "preview_only": True,
            "telegram_real_send": False
        }
    }

with open("config/default.yaml", "w") as f:
    yaml.dump(config, f, default_flow_style=False)

try:
    with open("config/local.example.yaml", "r") as f:
        local_config = yaml.safe_load(f)
    if "regime_labeling" not in local_config:
        local_config["regime_labeling"] = config["regime_labeling"]
    with open("config/local.example.yaml", "w") as f:
        yaml.dump(local_config, f, default_flow_style=False)
except FileNotFoundError:
    pass
