file_path = "usa_signal_bot/regime_classification/freeze_preparation/drift_report_qa_validator.py"

with open(file_path, "r") as f:
    text = f.read()

text = text.replace("field=None", "field_name=None")

with open(file_path, "w") as f:
    f.write(text)
