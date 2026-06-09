import pytest
from usa_signal_bot.release.acceptance_scenario_matrix import build_acceptance_scenario_matrix
from usa_signal_bot.release.advanced_dry_run_rehearsal_executor import execute_advanced_dry_run_scenario_matrix
from usa_signal_bot.release.acceptance_evidence_bundle import build_acceptance_evidence_bundle
from usa_signal_bot.release.data_pipeline_acceptance_report import build_data_pipeline_acceptance_report
from usa_signal_bot.release.feature_engine_acceptance_report import build_feature_engine_acceptance_report
from usa_signal_bot.release.model_governance_acceptance_report import build_model_governance_acceptance_report
from usa_signal_bot.release.backtest_acceptance_report import build_backtest_acceptance_report
from usa_signal_bot.release.portfolio_acceptance_report import build_portfolio_acceptance_report
from usa_signal_bot.release.cli_acceptance_report import build_cli_acceptance_report
from usa_signal_bot.release.config_acceptance_report import build_config_acceptance_report
from usa_signal_bot.release.storage_acceptance_report import build_storage_acceptance_report
from usa_signal_bot.release.health_acceptance_report import build_health_acceptance_report
from usa_signal_bot.release.quality_observability_acceptance_report import build_quality_observability_acceptance_report
from usa_signal_bot.release.notification_acceptance_report import build_notification_acceptance_report

def test_system_area_acceptance_reports():
    matrix = build_acceptance_scenario_matrix()
    steps = execute_advanced_dry_run_scenario_matrix(matrix)
    bundle = build_acceptance_evidence_bundle(matrix, steps)

    reports = [
        build_data_pipeline_acceptance_report(bundle, steps),
        build_feature_engine_acceptance_report(bundle, steps),
        build_model_governance_acceptance_report(bundle, steps),
        build_backtest_acceptance_report(bundle, steps),
        build_portfolio_acceptance_report(bundle, steps),
        build_cli_acceptance_report(bundle, steps),
        build_config_acceptance_report(bundle, steps),
        build_storage_acceptance_report(bundle, steps),
        build_health_acceptance_report(bundle, steps),
        build_quality_observability_acceptance_report(bundle, steps),
        build_notification_acceptance_report(bundle, steps)
    ]

    for report in reports:
        assert report.passed == True
        assert report.dry_run_only == True
        assert report.no_real_side_effects == True
