import re

with open("usa_signal_bot/app/cli.py", "r") as f:
    content = f.read()

patch_code = """
def setup_phase152_cli(subparsers):
    try:
        from usa_signal_bot.app.cli_phase152_patch import register_phase152_commands
        register_phase152_commands(subparsers)
    except ImportError:
        pass
"""

if "setup_phase152_cli" not in content:
    # insert before the end of the file or setup_parser
    content += patch_code

    # We also need to add setup_phase152_cli to setup_parser
    if "def setup_parser():" in content:
        content = content.replace("    # Phase 151 dummy cli stubs", "    setup_phase152_cli(subparsers)\n    # Phase 151 dummy cli stubs")

    with open("usa_signal_bot/app/cli.py", "w") as f:
        f.write(content)
