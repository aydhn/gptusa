file_path = "usa_signal_bot/regime_classification/freeze_preparation/phase134_models.py"

with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.strip() == "@dataclass":
        if len(new_lines) > 0 and new_lines[-1].strip() == "@dataclass":
            continue
    new_lines.append(line)

with open(file_path, "w") as f:
    f.writelines(new_lines)
