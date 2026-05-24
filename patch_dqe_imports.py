import re

with open("usa_signal_bot/quality/data_quality_evaluator.py", "r") as f:
    content = f.read()

content = "from typing import Dict, List, Tuple\n" + content

with open("usa_signal_bot/quality/data_quality_evaluator.py", "w") as f:
    f.write(content)
