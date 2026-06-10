from usa_signal_bot.backtesting.closure.backtest_closure_report import build_backtest_closure_full_review
rev = build_backtest_closure_full_review()
print("Passed validation:", rev.context.phase153_readiness_gate_passed)
