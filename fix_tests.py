import re
from pathlib import Path

for test_file in Path("tests").rglob("test_*.py"):
    with open(test_file, 'r') as f:
        content = f.read()

    # Many tests likely import missing things or use old enums
    if 'from usa_signal_bot.core.exceptions import USASignalBotError' not in content:
         # Try to find USASignalBotError and add import if not there
         if 'USASignalBotError' in content:
             content = 'from usa_signal_bot.core.exceptions import USASignalBotError\n' + content

    with open(test_file, 'w') as f:
        f.write(content)
