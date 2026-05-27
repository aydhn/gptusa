import re

with open('usa_signal_bot/app/cli.py', 'r') as f:
    content = f.read()

content = re.sub(r'\(write: bool = typer\.Option\([^)]*\)\)', '(args)', content)

with open('usa_signal_bot/app/cli.py', 'w') as f:
    f.write(content)
