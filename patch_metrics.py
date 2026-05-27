import re

with open("usa_signal_bot/observability/metrics_collector.py", "r") as f:
    content = f.read()

new_metrics = """
        self.metrics["latest_feature_enrichment_context_count"] = 0
        self.metrics["latest_feature_enrichment_spec_count"] = 0
        self.metrics["latest_feature_interaction_spec_count"] = 0
        self.metrics["latest_enriched_feature_result_count"] = 0
        self.metrics["latest_enriched_feature_table_count"] = 0
        self.metrics["latest_enriched_feature_column_count"] = 0
        self.metrics["latest_interaction_feature_column_count"] = 0
        self.metrics["latest_feature_confidence_low_count"] = 0
        self.metrics["latest_feature_freshness_stale_count"] = 0
        self.metrics["latest_enriched_feature_output_safety_violation_count"] = 0
        self.metrics["latest_feature_enrichment_trade_signal_violation_count"] = 0
        self.metrics["latest_phase119_execution_violation_count"] = 0
"""

if "latest_feature_enrichment_context_count" not in content:
    pattern = r"def __init__\(self\):([\s\S]*?)(?=\n\s*def |\Z)"
    match = re.search(pattern, content)
    if match:
        init_body = match.group(0)
        content = content.replace(init_body, init_body + new_metrics, 1)
        with open("usa_signal_bot/observability/metrics_collector.py", "w") as f:
            f.write(content)
        print("Updated metrics_collector.py")
else:
    print("metrics_collector.py already updated")
