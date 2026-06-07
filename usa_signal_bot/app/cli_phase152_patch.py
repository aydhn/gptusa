import argparse

def register_phase152_commands(subparsers):
    parser = subparsers.add_parser('backtest-closure-info', help='Show info about Phase 152 backtest closure')
    parser.set_defaults(func=cmd_backtest_closure_info)

    parser = subparsers.add_parser('backtest-closure-review', help='Run full backtest closure review')
    parser.add_argument('--write', action='store_true', help='Write artifacts to disk')
    parser.set_defaults(func=cmd_backtest_closure_review)

def cmd_backtest_closure_info(args):
    print("Phase 152: Realistic Backtest Robustness Final Audit & Closure")
    print("This phase acts strictly as a read-only final audit and closure phase.")
    print("It explicitly prohibits:")
    print(" - Live/paper trading")
    print(" - Broker execution")
    print(" - Paper state mutation")
    print(" - Deployment")
    print(" - Portfolio construction / Position sizing / Allocation")
    print("Produces a read-only research handoff package for Phase 153.")

def cmd_backtest_closure_review(args):
    from usa_signal_bot.backtesting.closure.backtest_closure_report import build_backtest_closure_full_review
    review = build_backtest_closure_full_review()
    print(f"Backtest closure review generated. Ready for Phase 153: {review.context.ready_for_phase153}")
    if args.write:
        from pathlib import Path
        from usa_signal_bot.backtesting.closure.backtest_closure_store import write_backtest_closure_full_review_json, backtest_closure_reviews_dir
        path = backtest_closure_reviews_dir(Path("data")) / f"backtest_closure_full_review_{review.review_id}.json"
        write_backtest_closure_full_review_json(path, review)
        print(f"Written to {path}")
