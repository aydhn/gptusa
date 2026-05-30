file_path = "usa_signal_bot/regime_classification/freeze_preparation/phase134_models.py"

with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if "class DriftReportQaRuleResult:" in line and "@dataclass" not in lines[i-1]:
        new_lines.append("@dataclass\n")
    new_lines.append(line)

with open(file_path, "w") as f:
    f.writelines(new_lines)
