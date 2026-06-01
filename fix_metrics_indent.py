with open('usa_signal_bot/observability/metrics_collector.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    # Fix the indentation at line 315-320 ish (which seems to be missing its class or method definition)
    if "latest_research_freeze_context_count: int = 0" in line:
        if i > 0 and "class" not in lines[i-1] and "def" not in lines[i-1]:
            new_lines.append("class Phase135MetricsDummy:\n")
    new_lines.append(line)

with open('usa_signal_bot/observability/metrics_collector.py', 'w') as f:
    f.writelines(new_lines)
