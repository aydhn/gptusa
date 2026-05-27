import re

with open('usa_signal_bot/app/cli.py', 'r') as f:
    content = f.read()

# Replace any lingering @cli.command and @click decorators
content = re.sub(r'@cli\.command\([^\)]*\)\n', '', content)
content = re.sub(r'@click\.option\([^\)]*\)\n', '', content)

content = content.replace("import click", "")
content = content.replace("click.echo", "print")

with open('usa_signal_bot/app/cli.py', 'w') as f:
    f.write(content)
