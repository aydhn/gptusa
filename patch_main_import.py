import re

with open('usa_signal_bot/__main__.py', 'r') as f:
    content = f.read()

# Make sure all the CLI setup functions are called
content = content.replace("from .app.cli import ", "from .app.cli import setup_phase114_cli, setup_phase120_cli, setup_phase124_cli, ")

if "setup_phase124_cli(subparsers)" not in content:
    content = content.replace("def main():", "def main():\n    pass")
    content = re.sub(r'(setup_phase\d+_cli\(subparsers\))', r'\1\n    setup_phase124_cli(subparsers)', content, count=1)

with open('usa_signal_bot/__main__.py', 'w') as f:
    f.write(content)
