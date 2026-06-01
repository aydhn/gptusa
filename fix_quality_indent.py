with open('usa_signal_bot/quality/data_quality_evaluator.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if "phase134_regime_monitoring_ingestion_score: int = 100" in line:
        if i > 0 and "class" not in lines[i-1] and "def" not in lines[i-1]:
            new_lines.append("class Phase135QualityDummy:\n")
    new_lines.append(line)

with open('usa_signal_bot/quality/data_quality_evaluator.py', 'w') as f:
    f.write("".join(new_lines))
