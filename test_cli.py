from usa_signal_bot.app.cli_phase152_patch import cmd_backtest_closure_info, cmd_backtest_closure_review
from collections import namedtuple

Args = namedtuple('Args', ['write'])

print("Running cmd_backtest_closure_info:")
cmd_backtest_closure_info(Args(write=False))

print("\nRunning cmd_backtest_closure_review:")
cmd_backtest_closure_review(Args(write=False))
