from pathlib import Path
p = Path("usa_signal_bot/app/cli.py")
content = p.read_text()
lines = content.split('\n')
for i in range(890, 910):
    if i < len(lines):
        print(f"{i}: {lines[i]}")
