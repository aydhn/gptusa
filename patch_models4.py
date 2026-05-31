import sys
file_path = "usa_signal_bot/regime_classification/freeze_preparation/phase134_models.py"

with open(file_path, "r") as f:
    text = f.read()

text = text.replace("    field: Optional[str] = None", "    field_name: Optional[str] = None")

with open(file_path, "w") as f:
    f.write(text)
