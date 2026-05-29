with open("tests/test_cli.py", "r") as f:
    content = f.read()

cli_test_add = """
def test_phase130_market_behavior_info():
    import sys
    from io import StringIO
    from usa_signal_bot.app.cli import get_parser
    parser = get_parser()
    args = parser.parse_args(["market-behavior-info"])

    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    try:
        args.func(args)
    finally:
        sys.stdout = old_stdout

    output = mystdout.getvalue()
    assert "Phase 130" in output
    assert "NOT an active paper trading phase" in output
"""

if "test_phase130_market_behavior_info" not in content:
    with open("tests/test_cli.py", "a") as f:
        f.write("\n" + cli_test_add)

print("Updated test_cli.py")
