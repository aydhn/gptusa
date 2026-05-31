import sys

file_path = "usa_signal_bot/app/cli.py"
with open(file_path, "r") as f:
    content = f.read()

# We used argparse before, not click. Let's see how phase 134 was added.
if "@click" in content:
    content = content.replace("@click.command", "# @click.command")
    content = content.replace("@click.pass_context", "# @click.pass_context")
    content = content.replace("@click.option", "# @click.option")

with open(file_path, "w") as f:
    f.write(content)
