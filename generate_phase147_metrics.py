import re

# Update metrics collector
metrics_path = "usa_signal_bot/observability/metrics_collector.py"
with open(metrics_path, "r") as f:
    metrics_content = f.read()

new_metrics = """
    latest_backtest_run_context_count: int = 0
    latest_research_decision_record_count: int = 0
    latest_price_event_count: int = 0
    latest_simulated_fill_count: int = 0
    latest_cost_ledger_record_count: int = 0
    latest_exposure_state_count: int = 0
    latest_equity_curve_point_count: int = 0
    latest_drawdown_point_count: int = 0
    latest_basic_performance_summary_count: int = 0
    latest_backtest_run_validation_gate_pass_count: int = 0
    latest_phase147_live_trading_violation_count: int = 0
    latest_phase147_paper_trading_violation_count: int = 0
    latest_phase147_real_order_violation_count: int = 0
    latest_phase147_broker_execution_violation_count: int = 0
    latest_phase147_walk_forward_violation_count: int = 0
    latest_phase147_stress_test_violation_count: int = 0
    latest_phase147_monte_carlo_violation_count: int = 0
    latest_phase147_benchmark_comparison_violation_count: int = 0
"""

if "latest_backtest_run_context_count" not in metrics_content:
    metrics_content = metrics_content.replace('class MetricsCollector:', f'class MetricsCollector:\n{new_metrics}')
    with open(metrics_path, "w") as f:
        f.write(metrics_content)
    print("Metrics updated")


# Update Data Quality Evaluator
quality_path = "usa_signal_bot/quality/data_quality_evaluator.py"
with open(quality_path, "r") as f:
    quality_content = f.read()

new_quality = """
        self.phase147_backtest_foundation_ingestion_score = 100.0
        self.phase147_run_input_resolver_score = 100.0
        self.phase147_run_config_score = 100.0
        self.phase147_research_decision_stream_score = 100.0
        self.phase147_simulation_clock_score = 100.0
        self.phase147_price_event_stream_score = 100.0
        self.phase147_simulated_execution_score = 100.0
        self.phase147_cost_application_score = 100.0
        self.phase147_liquidity_partial_fill_score = 100.0
        self.phase147_exposure_timeline_score = 100.0
        self.phase147_equity_curve_score = 100.0
        self.phase147_drawdown_curve_score = 100.0
        self.phase147_ledger_score = 100.0
        self.phase147_basic_performance_score = 100.0
        self.phase147_safety_boundary_score = 100.0
        self.phase147_validation_gate_score = 100.0
        self.phase147_determinism_score = 100.0
        self.phase147_non_execution_compliance_score = 100.0
        self.phase147_no_live_trading_compliance_score = 100.0
        self.phase147_no_broker_compliance_score = 100.0
"""

if "phase147_backtest_foundation_ingestion_score" not in quality_content:
    quality_content = quality_content.replace('class DataQualityEvaluator:\n    def __init__(self):', f'class DataQualityEvaluator:\n    def __init__(self):\n{new_quality}')
    with open(quality_path, "w") as f:
        f.write(quality_content)
    print("Quality scorecard updated")
