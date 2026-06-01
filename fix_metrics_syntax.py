import re
with open('usa_signal_bot/observability/metrics_collector.py', 'r') as f:
    content = f.read()

# Fix the specific syntax error where the new line was concatenated without a newline char.
content = content.replace('self.metrics["latest_phase125_deployment_violation_count"] = 0        self.phase141 = Phase141Metrics()',
                          'self.metrics["latest_phase125_deployment_violation_count"] = 0\n        self.phase141 = Phase141Metrics()')

with open('usa_signal_bot/observability/metrics_collector.py', 'w') as f:
    f.write(content)
