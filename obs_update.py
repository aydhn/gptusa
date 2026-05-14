import os

file_path = "usa_signal_bot/observability/metrics_collector.py"

content = """
# Operational metrics addition
def update_cost_robustness_metrics(status: str, score: float, failed_scenarios: int, fragile_windows: int, breakeven_bps: float, failed_cells: int, fragility_reasons: int):
    pass
"""

if not os.path.exists(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(content)
else:
    with open(file_path, "a") as f:
        f.write("\n" + content)
