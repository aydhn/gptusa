file_path = "usa_signal_bot/regime_classification/freeze_preparation/research_freeze_safety_validator.py"

with open(file_path, "r") as f:
    text = f.read()

text = text.replace("import pandas as pd", """
try:
    import pandas as pd
except ImportError:
    pd = None
""")

text = text.replace("def validate_research_freeze_dataframe_output_safety(df: pd.DataFrame)", "def validate_research_freeze_dataframe_output_safety(df: Any)")

with open(file_path, "w") as f:
    f.write(text)
