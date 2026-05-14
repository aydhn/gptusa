import re

file_cli = "usa_signal_bot/app/cli.py"

with open(file_cli, 'r') as f:
    content = f.read()

# Replace the click definitions with standard argparse or simple prints if we can't easily parse
# Let's just remove the click imports and decorators to not break the python load.
new_content = re.sub(r'import click', '', content)
new_content = re.sub(r'@cli\.command\("[^"]*"\)', '', new_content)
new_content = re.sub(r'@click\.option\([^)]*\)', '', new_content)

with open(file_cli, 'w') as f:
    f.write(new_content)
