from pathlib import Path
import re
p = Path("usa_signal_bot/app/cli.py")
content = p.read_text()
lines = content.split('\n')
for i in range(700, 720):
    if i < len(lines):
        print(f"{i}: {lines[i]}")
