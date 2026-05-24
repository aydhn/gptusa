import re

with open("usa_signal_bot/__main__.py", "r") as f:
    content = f.read()

new_content = """
import sys
from usa_signal_bot.app.cli import cli

def main():
    cli()

if __name__ == "__main__":
    main()
"""

with open("usa_signal_bot/__main__.py", "w") as f:
    f.write(new_content)
