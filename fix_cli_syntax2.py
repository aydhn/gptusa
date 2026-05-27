import re

with open('usa_signal_bot/app/cli.py', 'r') as f:
    content = f.read()

# Make sure that syntax is fixed
content = content.replace("def setup_phase114_cli(subparsers)\n    def setup_phase114_cli(subparsers):", "def setup_phase114_cli(subparsers):")
content = content.replace("def setup_phase114_cli(subparsers)\n", "def setup_phase114_cli(subparsers):\n")

with open('usa_signal_bot/app/cli.py', 'w') as f:
    f.write(content)
