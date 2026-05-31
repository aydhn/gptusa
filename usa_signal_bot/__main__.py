import argparse
import sys
from .app.cli import (
    append_phase129_to_parser,
    setup_phase114_cli,
    setup_phase124_cli,
    setup_phase135_cli,
    setup_phase136_cli
)

def main():
    parser = argparse.ArgumentParser(prog='python -m usa_signal_bot')
    subparsers = parser.add_subparsers(dest='command')

    try:
        setup_phase114_cli(subparsers)
    except: pass
    try:
        setup_phase124_cli(subparsers)
    except: pass
    try:
        append_phase129_to_parser(subparsers)
    except: pass
    try:
        setup_phase135_cli(subparsers)
    except: pass
    try:
        setup_phase136_cli(subparsers)
    except: pass

    args = parser.parse_args()
    if args.command:
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
