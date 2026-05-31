file_path = "usa_signal_bot/app/cli.py"
with open(file_path, "r") as f:
    content = f.read()

content = content.replace("def append_phase132_to_parser(subparsers)\n", "def append_phase132_to_parser(subparsers):\n")

with open(file_path, "w") as f:
    f.write(content)
