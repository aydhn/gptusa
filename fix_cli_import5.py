from pathlib import Path
p = Path("usa_signal_bot/app/cli.py")
content = p.read_text()
lines = content.split('\n')
# Remove all the garbage we added or that was left behind
filtered = []
for line in lines:
    if "Disclaimer: Boundary certificate is not an active paper approval" in line:
        continue
    filtered.append(line)

p.write_text('\n'.join(filtered))
