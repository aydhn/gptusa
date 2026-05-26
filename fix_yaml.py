import yaml

for file in ['config/default.yaml', 'config/local.example.yaml']:
    try:
        with open(file, 'r') as f:
            data = yaml.safe_load(f)

        data['feature_engine_foundation'] = {
            'enabled': True,
            'current_phase': 116,
            'final_phase': 160,
            'require_phase115_feature_factor_kickoff_gate': True,
            'indicator_registry_enabled': True,
            'feature_registry_enabled': True,
            'factor_registry_enabled': True,
            'feature_input_contract_enabled': True,
            'feature_output_schema_enabled': True,
            'feature_computation_planner_enabled': True,
            'feature_transform_pipeline_enabled': True,
            'write_feature_foundation_reports': True,
            'warn_not_investment_advice': True,
            'warn_phase116_is_not_activation': True,
            'warn_features_are_not_trade_signals': True
        }
        data['phase116_feature_policy'] = {
            'metadata_only': True,
            'research_data_only': True,
            'dry_run_only_default': True,
            'local_fixture_only_default': True,
            'allow_network': False,
            'allow_paid_api': False,
            'allow_scraping': False,
            'allow_html_parsing': False,
            'allow_broker': False,
            'allow_order': False,
            'allow_paper_mutation': False,
            'allow_telegram_real_send': False,
            'allow_dashboard': False,
            'produce_trade_signals': False,
            'produce_order_decisions': False,
            'strategy_activation_allowed': False
        }
        data['phase116_feature_scope'] = {
            'allow_indicator_input_contracts': True,
            'allow_feature_schema_definitions': True,
            'allow_factor_metadata_definitions': True,
            'allow_ohlcv_feature_fixtures': True,
            'allow_event_context_feature_metadata': True,
            'allow_calendar_aware_feature_metadata': True,
            'allow_quality_aware_feature_metadata': True,
            'allow_feature_validation_rules': True,
            'allow_feature_lineage_metadata': True,
            'block_signal_generation': True,
            'block_strategy_activation': True,
            'block_order_decision': True,
            'block_broker_execution': True,
            'block_paper_state_mutation': True
        }
        data['phase116_notifications'] = {
            'enabled': True,
            'dry_run': True,
            'preview_only': True,
            'telegram_real_send': False
        }
        with open(file, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
    except Exception as e:
        print(f"Failed on {file}: {e}")
