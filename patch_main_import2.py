import re

with open('usa_signal_bot/__main__.py', 'r') as f:
    content = f.read()

# Make sure that we add setup_phase124_cli appropriately to __main__.py
with open('usa_signal_bot/__main__.py', 'w') as f:
    f.write('''import argparse
import sys
from .app.cli import (
    setup_phase114_cli,
    setup_phase120_cli,
    setup_phase115_cli,
    setup_phase116_cli,
    setup_phase118_cli,
    setup_phase124_cli
)

def main():
    parser = argparse.ArgumentParser(prog='python -m usa_signal_bot')
    subparsers = parser.add_subparsers(dest='command')

    try:
        setup_phase114_cli(subparsers)
    except: pass
    try:
        setup_phase120_cli(subparsers)
    except: pass
    try:
        setup_phase115_cli(subparsers)
    except: pass
    try:
        setup_phase116_cli(subparsers)
    except: pass
    try:
        setup_phase118_cli(subparsers)
    except: pass
    try:
        setup_phase124_cli(subparsers)
    except: pass

    args = parser.parse_args()
    if args.command:
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
''')
