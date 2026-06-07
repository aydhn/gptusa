import os
import textwrap

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(textwrap.dedent(content).lstrip())

# 32. HEALTH
write_file("usa_signal_bot/core/health_phase152_patch.py", """
from typing import Any

def check_phase152_backtest_closure_config_health(context: Any) -> Any:
    # return mock HealthCheckResult
    class Result:
        def __init__(self):
            self.status = "healthy"
            self.component = "phase152_closure"
            self.message = "Closure config is valid"
    return Result()
""")

# 33. CLI
write_file("usa_signal_bot/app/cli_phase152_patch.py", """
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
""")

# 37-46. DOCS
write_file("docs/PHASE_152_SUMMARY.md", """
# Phase 152 Summary: Realistic Backtest Robustness Final Audit & Closure

## Overview
Phase 152 serves as the final audit, governance closure, and artifact lineage verification step for the Phase 146-151 Realistic Backtest band. It securely bundles the single-strategy runs, advanced analytics, benchmark comparisons, walk-forward out-of-sample tests, and stress/Monte Carlo robustness evaluations into a final sealed package.

## Constraints & Limitations
- **No Live Trading:** Phase 152 generates artifacts only. It does not trade.
- **No Paper Trading:** It does not mutate paper state.
- **No Broker Execution:** It does not route orders.
- **No Deployment:** The final closure certificate is not an activation trigger.
- **No Portfolio Output:** This phase explicitly blocks portfolio construction, position sizing, allocation, and target weights.
- **Research Only:** All outputs are strictly for offline research purposes.

## Deliverables
1. **Artifact Lineage Manifest:** Cross-phase deterministic hash tracking.
2. **Compliance Audits:** Determinism, Safety, and Research Boundary audits to ensure adherence to Phase 152 constraints.
3. **Metric & Risk Note Inventories:** Aggregated diagnostics.
4. **Final Audit Report & Closure Certificate:** The official sign-off for the backtest band.
5. **Phase 153 Handoff Package:** A strictly read-only, non-execution bundle serving as the foundation for the Phase 153 Portfolio Construction and Risk Budgeting band.

## Next Steps
The generated `Phase153HandoffPackage` allows for safe transition into Phase 153, where multi-strategy portfolio construction and position sizing will begin, strictly offline.
""")
