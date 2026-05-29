with open("usa_signal_bot/regime_classification/behavior_reporting/markdown_behavior_report_renderer.py", "r") as f:
    c = f.read()
c = "from typing import Any\n" + c
with open("usa_signal_bot/regime_classification/behavior_reporting/markdown_behavior_report_renderer.py", "w") as f:
    f.write(c)
