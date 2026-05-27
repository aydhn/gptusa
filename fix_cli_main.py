import re

with open('usa_signal_bot/__main__.py', 'r') as f:
    content = f.read()

# Make sure setup_phase124_cli is called
if "setup_phase124_cli" not in content:
    content = content.replace("from .app.cli import ", "from .app.cli import setup_phase124_cli, ")
    content = content.replace("setup_phase118_cli(subparsers)", "setup_phase118_cli(subparsers)\n    setup_phase124_cli(subparsers)")

with open('usa_signal_bot/__main__.py', 'w') as f:
    f.write(content)
