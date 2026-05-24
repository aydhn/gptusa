from pathlib import Path
p = Path("usa_signal_bot/app/cli.py")
content = p.read_text()
lines = content.split('\n')
for i, line in enumerate(lines):
    if line.startswith('    print("Disclaimer: Boundary certificate is not an active paper approval")'):
        print(f"Found issue at line {i}: {line}")
        # Need to put it in a function
        break
