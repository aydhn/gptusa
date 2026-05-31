import sys

file_path = "usa_signal_bot/__main__.py"
with open(file_path, "r") as f:
    content = f.read()

content = content.replace(
    "setup_phase124_cli",
    "setup_phase124_cli,\n    setup_phase135_cli"
)

content = content.replace(
    "    try:\n        setup_phase124_cli(subparsers)\n    except: pass\n",
    "    try:\n        setup_phase124_cli(subparsers)\n    except: pass\n    try:\n        setup_phase135_cli(subparsers)\n    except: pass\n"
)

with open(file_path, "w") as f:
    f.write(content)
