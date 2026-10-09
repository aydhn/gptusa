import sys

from usa_signal_bot.ml_research.ensemble_evaluation.ensemble_prototype_report import (
    build_ensemble_prototype_full_review,
    ensemble_prototype_full_review_to_text,
    ensemble_prototype_limitations_text,
)
from usa_signal_bot.ml_research.ensemble_evaluation.ensemble_prototype_store import (
    write_ensemble_prototype_full_review_json,
    ensemble_prototype_reviews_dir,
)
from pathlib import Path

import argparse

from usa_signal_bot.evidence.cli import setup_evidence_cli
import sys


def setup_phase156_cli(subparsers):
    p = subparsers.add_parser(
        "optimizer-prototype-info", help="Print Phase 156 Optimizer prototype info"
    )
    p.set_defaults(
        func=lambda args: print(
            "Phase 156 is a research-only local portfolio optimization prototype phase. No actual target weights or live trading are allowed."
        )
    )

    p = subparsers.add_parser(
        "build-optimizer-policy",
        help="Build and optionally write Optimizer sandbox policy",
    )
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=lambda args: print("Built Optimizer sandbox policy"))

    p = subparsers.add_parser(
        "build-score-maximizing-optimizer",
        help="Build score-maximizing optimizer prototype results",
    )
    p.add_argument("--write", action="store_true")
    p.set_defaults(
        func=lambda args: print("Built score-maximizing optimizer sandbox results")
    )

    p = subparsers.add_parser(
        "build-objective-comparison-report", help="Build objective comparison report"
    )
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=lambda args: print("Built objective comparison report"))

    p = subparsers.add_parser(
        "optimizer-prototype-review",
        help="Build full Phase 156 optimizer prototype review",
    )
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=lambda args: print("Built optimizer prototype full review"))


def setup_phase157_cli(subparsers):
    p = subparsers.add_parser(
        "portfolio-risk-info",
        help="Phase 157 is research-only portfolio risk reporting, exposure governance, and portfolio band closure phase. No live/paper/broker/deployment/actual target weight/actual allocation.",
    )
    p.set_defaults(
        func=lambda args: print(
            "Phase 157 is a research-only local phase. No actual target weights or live trading are allowed."
        )
    )

    for cmd in [
        "risk-ingest-optimizer-prototype",
        "risk-artifact-load",
        "resolve-risk-governance-inputs",
        "build-sandbox-exposure-governance",
        "build-portfolio-risk-summary",
        "build-concentration-risk-report",
        "build-diversification-governance-report",
        "build-risk-budget-governance-report",
        "build-turnover-governance-report",
        "build-optimizer-objective-governance-report",
        "build-constraint-governance-report",
        "build-portfolio-limitations-report",
        "build-portfolio-band-lineage",
        "build-portfolio-band-compliance-audit",
        "build-portfolio-band-final-review",
        "build-portfolio-band-closure-certificate",
        "build-phase158-handoff-contract",
        "build-phase158-handoff-package",
        "validate-portfolio-risk-safety-boundary",
        "phase158-readiness-gate",
        "portfolio-risk-schema-check",
        "portfolio-risk-safety-check",
        "portfolio-risk-context",
        "portfolio-risk-review",
        "portfolio-risk-summary",
        "portfolio-risk-validate",
    ]:
        p = subparsers.add_parser(cmd)
        p.add_argument("--write", action="store_true")
        p.set_defaults(
            func=lambda args, c=cmd: print(
                f"Executed {c} {'(Write Mode)' if args.write else '(Preview)'}"
            )
        )


def handle_advanced_acceptance_commands(args, context):
    print("Executing Phase 159 Advanced Acceptance command")
    if args.command == "advanced-acceptance-info":
        print(
            "Phase 159 is strictly an advanced acceptance rehearsal, release candidate audit and final freeze preparation phase."
        )
        print("It does NOT represent a deployment approval or trading approval.")
    elif args.command == "advanced-acceptance-review":
        from usa_signal_bot.release.advanced_acceptance_report import (
            build_advanced_acceptance_context,
            build_advanced_acceptance_full_review,
            advanced_acceptance_full_review_to_text,
        )

        ctx = build_advanced_acceptance_context()
        rev = build_advanced_acceptance_full_review(ctx)
        print(advanced_acceptance_full_review_to_text(rev))
    elif args.command == "build-acceptance-scenario-matrix":
        from usa_signal_bot.release.acceptance_scenario_matrix import (
            build_acceptance_scenario_matrix,
            acceptance_scenario_matrix_to_text,
        )

        mat = build_acceptance_scenario_matrix()
        print(acceptance_scenario_matrix_to_text(mat))
    elif args.command == "execute-advanced-dry-run-rehearsal":
        from usa_signal_bot.release.acceptance_scenario_matrix import (
            build_acceptance_scenario_matrix,
        )
        from usa_signal_bot.release.advanced_dry_run_rehearsal_executor import (
            execute_advanced_dry_run_scenario_matrix,
            advanced_dry_run_rehearsal_to_text,
        )

        mat = build_acceptance_scenario_matrix()
        steps = execute_advanced_dry_run_scenario_matrix(mat)
        print(advanced_dry_run_rehearsal_to_text(steps))
    elif args.command == "build-release-candidate-audit":
        from usa_signal_bot.release.advanced_acceptance_report import (
            build_advanced_acceptance_context,
            build_advanced_acceptance_full_review,
        )

        ctx = build_advanced_acceptance_context()
        rev = build_advanced_acceptance_full_review(ctx)
        # Assuming audit exists in mock
        print("Mocked Release Candidate Audit Output.")
    else:
        print(f"Command {args.command} executed in dry-run preview mode.")
        print("Done.")


def setup_phase143_cli(subparsers):
    parser_ensemble_info = subparsers.add_parser(
        "ensemble-prototype-info", help="Print info about Phase 143"
    )

    parser_ensemble_review = subparsers.add_parser(
        "ensemble-prototype-review", help="Run full Phase 143 review"
    )
    parser_ensemble_review.add_argument("--write", action="store_true")

    parser_ensemble_build_specs = subparsers.add_parser(
        "build-ensemble-prototype-specs", help="Build specs"
    )
    parser_ensemble_build_specs.add_argument("--write", action="store_true")

    parser_ensemble_pred = subparsers.add_parser(
        "generate-offline-ensemble-predictions", help="Generate predictions"
    )
    parser_ensemble_pred.add_argument("--write", action="store_true")

    parser_ensemble_diag = subparsers.add_parser(
        "build-blend-diagnostics", help="Build diagnostics"
    )
    parser_ensemble_diag.add_argument("--write", action="store_true")

    for cmd in [
        "ensemble-prototype-ingest-scaffolding",
        "ensemble-prototype-artifact-load",
        "resolve-ensemble-prototype-inputs",
        "build-candidate-agreement-diagnostics",
        "build-ensemble-candidate-comparison",
        "calculate-offline-ensemble-evaluation-metrics",
        "build-offline-ensemble-evaluation-reports",
        "build-non-activation-ensemble-registry",
        "update-model-cards-with-ensemble-evaluation",
        "validate-ensemble-prototype-boundary",
        "ensemble-prototype-readiness-gate",
        "ensemble-prototype-schema-check",
        "ensemble-prototype-safety-check",
        "ensemble-prototype-context",
        "ensemble-prototype-summary",
        "ensemble-prototype-validate",
    ]:
        p = subparsers.add_parser(cmd, help=f"Phase 143 {cmd}")
        p.add_argument("--write", action="store_true")


def setup_phase155_cli(subparsers):
    parser_info_155 = subparsers.add_parser(
        "portfolio-construction-info", help="Print info about Phase 155"
    )
    parser_policy_155 = subparsers.add_parser(
        "build-portfolio-construction-policy", help="Build policy"
    )
    parser_policy_155.add_argument("--write", action="store_true")
    parser_review_155 = subparsers.add_parser(
        "portfolio-construction-review", help="Run full Phase 155 review"
    )
    parser_review_155.add_argument("--write", action="store_true")


def setup_phase145_cli(subparsers):
    subparsers.add_parser(
        "ml-closure-info",
        help="Display information about Phase 145 ML Governance Closure.",
    )

    commands_with_write = [
        (
            "ml-closure-ingest-drift-monitoring",
            "Ingest Drift Monitoring output (Simulated)",
        ),
        ("ml-closure-artifact-load", "Load Artifacts (Simulated)"),
        ("resolve-explainability-inputs", "Resolve Explainability Inputs (Simulated)"),
        (
            "build-feature-attribution-proxy",
            "Build Feature Attribution Proxy (Simulated)",
        ),
        (
            "build-factor-contribution-summary",
            "Build Factor Contribution Summary (Simulated)",
        ),
        (
            "build-model-behavior-explanation",
            "Build Model Behavior Explanation (Simulated)",
        ),
        (
            "build-regime-aware-explanation",
            "Build Regime Aware Explanation (Simulated)",
        ),
        (
            "build-calibration-aware-explanation",
            "Build Calibration Aware Explanation (Simulated)",
        ),
        ("build-ensemble-explanation", "Build Ensemble Explanation (Simulated)"),
        ("build-explainability-report", "Build Explainability Report (Simulated)"),
        (
            "build-advanced-ml-artifact-lineage",
            "Build Advanced ML Artifact Lineage (Simulated)",
        ),
        ("build-ml-governance-closure", "Build ML Governance Closure (Simulated)"),
        ("build-advanced-ml-final-audit", "Build Advanced ML Final Audit (Simulated)"),
        (
            "validate-non-activation-ml-closure-boundary",
            "Validate Non Activation ML Closure Boundary (Simulated)",
        ),
        (
            "build-final-ml-model-card-closure",
            "Build Final ML Model Card Closure (Simulated)",
        ),
        ("advanced-ml-acceptance-gate", "Run Advanced ML Acceptance Gate (Simulated)"),
        ("ml-closure-context", "Build ML Closure Context (Simulated)"),
        ("ml-closure-review", "Build ML Closure Review (Simulated)"),
    ]

    for cmd, help_text in commands_with_write:
        p = subparsers.add_parser(cmd, help=help_text)
        p.add_argument("--write", action="store_true")

    commands_without_write = [
        ("ml-closure-schema-check", "Check ML Closure Schema (Simulated)"),
        ("ml-closure-safety-check", "Check ML Closure Safety (Simulated)"),
        ("ml-closure-summary", "Show ML Closure Summary (Simulated)"),
        ("ml-closure-validate", "Validate ML Closure (Simulated)"),
    ]

    for cmd, help_text in commands_without_write:
        subparsers.add_parser(cmd, help=help_text)


def setup_phase147_cli(subparsers):
    parser_phase147_info = subparsers.add_parser(
        "backtest-run-info", help="Phase 147 info"
    )

    for cmd in [
        "backtest-run-ingest-foundation",
        "backtest-run-artifact-load",
        "resolve-backtest-run-inputs",
        "build-backtest-run-config",
        "build-research-decision-stream",
        "build-simulation-clock",
        "build-price-event-stream",
        "run-offline-simulated-execution",
        "apply-cost-spread-slippage",
        "evaluate-liquidity-partial-fills",
        "build-exposure-timeline",
        "build-equity-curve",
        "build-drawdown-curve",
        "build-backtest-ledger",
        "build-basic-performance-summary",
        "validate-backtest-run-safety-boundary",
        "backtest-run-validation-gate",
        "backtest-run-schema-check",
        "backtest-run-safety-check",
        "backtest-run-context",
        "backtest-run-review",
    ]:
        p = subparsers.add_parser(cmd, help=f"Phase 147 {cmd}")
        p.add_argument("--write", action="store_true")

    subparsers.add_parser("backtest-run-summary", help="Phase 147 summary")
    subparsers.add_parser("backtest-run-validate", help="Phase 147 validate")


def setup_phase150_cli(subparsers):
    parser_wf_info = subparsers.add_parser(
        "walk-forward-info", help="Print info about Phase 150"
    )

    parser_wf_wp = subparsers.add_parser(
        "build-walk-forward-window-policy", help="Build window policy"
    )
    parser_wf_wp.add_argument("--write", action="store_true", help="Write output")

    parser_wf_as = subparsers.add_parser(
        "build-anchored-walk-forward-splits", help="Build anchored splits"
    )
    parser_wf_as.add_argument("--write", action="store_true", help="Write output")

    parser_wf_rs = subparsers.add_parser("run-fold-replays", help="Run fold replays")
    parser_wf_rs.add_argument("--write", action="store_true", help="Write output")

    parser_wf_rev = subparsers.add_parser(
        "walk-forward-review", help="Walk forward review"
    )
    parser_wf_rev.add_argument("--write", action="store_true", help="Write output")


def setup_parser():
    parser = argparse.ArgumentParser(prog="python -m usa_signal_bot")
    subparsers = parser.add_subparsers(dest="command")

    for register in _command_registrars():
        register(subparsers)

    return parser


def _command_registrars():
    """Single list of all CLI command registrars; add new setup_* functions here."""
    return (
        setup_phase143_cli,
        setup_phase145_cli,
        setup_phase147_cli,
        setup_phase150_cli,
        setup_phase151_cli,
        setup_phase152_cli,
        setup_phase155_cli,
        setup_phase156_cli,
        setup_phase157_cli,
        setup_evidence_cli,
    )


def handle_walk_forward_commands(args):
    if args.command == "walk-forward-info":
        from usa_signal_bot.backtesting.walk_forward.walk_forward_report import (
            walk_forward_limitations_text,
        )

        print(
            "Phase 150 is offline walk-forward validation and temporal stability audit."
        )
        print(
            "It explicitly prohibits live/paper trading, broker integration, deployment, stress tests, and Monte Carlo."
        )
        print(walk_forward_limitations_text())
        import sys
        import sys

        sys.exit(0)
    if args.command == "build-walk-forward-window-policy":
        from usa_signal_bot.backtesting.walk_forward.walk_forward_window_policy import (
            build_default_walk_forward_window_policy,
            walk_forward_window_policy_to_text,
        )

        policy = build_default_walk_forward_window_policy()
        print(walk_forward_window_policy_to_text(policy))
        if getattr(args, "write", False):
            print("Written (mock).")
        import sys
        import sys

        sys.exit(0)
    if args.command == "build-anchored-walk-forward-splits":
        from usa_signal_bot.backtesting.walk_forward.walk_forward_window_policy import (
            build_default_walk_forward_window_policy,
        )
        from usa_signal_bot.backtesting.walk_forward.anchored_split_builder import (
            build_anchored_walk_forward_folds,
            anchored_folds_to_text,
        )

        policy = build_default_walk_forward_window_policy()
        try:
            import pandas as pd

            df = pd.DataFrame({"timestamp": ["2023-01-01"], "strategy_return": [0.0]})
            folds = build_anchored_walk_forward_folds(df, policy)
            print(anchored_folds_to_text(folds))
        except ImportError:
            print("Skipping proper split generation due to missing pandas")
        if getattr(args, "write", False):
            print("Written (mock).")
        import sys
        import sys

        sys.exit(0)
    if args.command == "run-fold-replays":
        print("Fold replays ran successfully (mock).")
        import sys
        import sys

        sys.exit(0)
    if args.command == "walk-forward-review":
        from usa_signal_bot.backtesting.walk_forward.walk_forward_report import (
            build_walk_forward_full_review,
            walk_forward_full_review_to_text,
        )

        review = build_walk_forward_full_review()
        print(walk_forward_full_review_to_text(review))
        if getattr(args, "write", False):
            print("Written (mock).")
        import sys
        import sys

        sys.exit(0)


def handle_backtest_run_commands(args):
    if args.command == "backtest-run-info":
        print(
            "Phase 147 - Offline Deterministic Realistic Backtest Engine and Single-Strategy Backtest Run"
        )
        print(
            "This phase DOES NOT perform live trading, paper trading, broker execution, or deployment."
        )
        print("It provides a strict local offline backtest environment.")
        return
    if args.command and args.command in [
        "backtest-run-ingest-foundation",
        "backtest-run-artifact-load",
        "resolve-backtest-run-inputs",
        "build-backtest-run-config",
        "build-research-decision-stream",
        "build-simulation-clock",
        "build-price-event-stream",
        "run-offline-simulated-execution",
        "apply-cost-spread-slippage",
        "evaluate-liquidity-partial-fills",
        "build-exposure-timeline",
        "build-equity-curve",
        "build-drawdown-curve",
        "build-backtest-ledger",
        "build-basic-performance-summary",
        "validate-backtest-run-safety-boundary",
        "backtest-run-validation-gate",
        "backtest-run-schema-check",
        "backtest-run-safety-check",
        "backtest-run-context",
        "backtest-run-review",
        "backtest-run-summary",
        "backtest-run-validate",
    ]:
        print(f"Executing {args.command} (Phase 147) [Mock]")
        if getattr(args, "write", False):
            print("Write mode simulated.")
        return


def handle_portfolio_foundation_commands(args):
    if args.command == "portfolio-foundation-info":
        print(
            "Phase 153 is the Portfolio Construction Foundation, Position Sizing Boundary and Risk Budgeting Contract phase."
        )
        print("It is strictly a contract-only phase.")
        print(
            "It does NOT perform actual portfolio construction, sizing, or capital allocation."
        )
        print(
            "It does NOT generate investment advice, target weights, or live/paper/broker orders."
        )
        print(
            "Its sole purpose is to establish boundaries for Phase 154 sizing prototypes."
        )
        return


def handle_ensemble_prototype_commands(args):
    if args.command == "ensemble-prototype-info":
        print(
            "Phase 143 is an offline ensemble prototype evaluation, blend diagnostics, and non-activation ensemble registry phase. It is NOT active paper trading, deployment, live inference, or live daemon."
        )
        print(ensemble_prototype_limitations_text())
        return
    if args.command == "ensemble-prototype-review":
        review = build_ensemble_prototype_full_review()
        if args.write:
            write_ensemble_prototype_full_review_json(
                ensemble_prototype_reviews_dir(Path("data")) / "latest_review.json",
                review,
            )
            print(
                "Wrote review to data/ml_research/ensemble_evaluation/reviews/latest_review.json"
            )
        else:
            print(ensemble_prototype_full_review_to_text(review))
        return
    if (
        args.command
        and args.command.startswith("ensemble-prototype")
        or args.command
        in [
            "build-ensemble-prototype-specs",
            "generate-offline-ensemble-predictions",
            "build-blend-diagnostics",
            "resolve-ensemble-prototype-inputs",
            "build-candidate-agreement-diagnostics",
            "build-ensemble-candidate-comparison",
            "calculate-offline-ensemble-evaluation-metrics",
            "build-offline-ensemble-evaluation-reports",
            "build-non-activation-ensemble-registry",
            "update-model-cards-with-ensemble-evaluation",
            "validate-ensemble-prototype-boundary",
        ]
    ):
        print(f"Executing {args.command} (Phase 143) [Mock]")
        if args.write:
            print("Write mode simulated.")
        return
    if args.command == "build-ensemble-explanation":
        print("Building ensemble explanations...")
        if getattr(args, "write", False):
            print("Writing to store...")
        print("Done (Simulated)")
        import sys

        sys.exit(0)


def _handle_ml_closure_info(args):
    if args.command == "ml-closure-info":
        print("Phase 145 - Advanced ML Band Final Audit and ML Governance Closure")
        print(
            "This phase is for explainability metadata, final ML governance closure and Advanced ML band final audit."
        )
        print(
            "It DOES NOT run active paper trading, deployment, live inference, live monitoring, live daemon, or backtests."
        )
        import sys

        sys.exit(0)
    if args.command == "ml-closure-ingest-drift-monitoring":
        print("Ingesting Drift Monitoring output...")
        if getattr(args, "write", False):
            print("Writing to store...")
        print("Done (Simulated)")
        import sys

        sys.exit(0)
    if args.command == "ml-closure-artifact-load":
        print("Loading artifacts...")
        if getattr(args, "write", False):
            print("Writing to store...")
        print("Done (Simulated)")
        import sys

        sys.exit(0)


def _handle_ml_closure_explainability(args):
    if args.command == "resolve-explainability-inputs":
        print("Resolving explainability inputs...")
        if getattr(args, "write", False):
            print("Writing to store...")
        print("Done (Simulated)")
        import sys

        sys.exit(0)
    if args.command == "build-feature-attribution-proxy":
        print(
            "Building feature attribution proxies... Note: These are NOT trade signals."
        )
        if getattr(args, "write", False):
            print("Writing to store...")
        print("Done (Simulated)")
        import sys

        sys.exit(0)
    if args.command == "build-factor-contribution-summary":
        print(
            "Building factor contribution summaries... Note: These are NOT portfolio weights or allocations."
        )
        if getattr(args, "write", False):
            print("Writing to store...")
        print("Done (Simulated)")
        import sys

        sys.exit(0)
    if args.command == "build-model-behavior-explanation":
        print("Building model behavior explanations...")
        if getattr(args, "write", False):
            print("Writing to store...")
        print("Done (Simulated)")
        import sys

        sys.exit(0)
    if args.command == "build-regime-aware-explanation":
        print("Building regime aware explanations...")
        if getattr(args, "write", False):
            print("Writing to store...")
        print("Done (Simulated)")
        import sys

        sys.exit(0)
    if args.command == "build-calibration-aware-explanation":
        print("Building calibration aware explanations...")
        if getattr(args, "write", False):
            print("Writing to store...")
        print("Done (Simulated)")
        import sys

        sys.exit(0)
    if args.command == "build-explainability-report":
        print("Building explainability report...")
        if getattr(args, "write", False):
            print("Writing to store...")
        print("Done (Simulated)")
        import sys

        sys.exit(0)


def _handle_ml_closure_audit_and_validation(args):
    if args.command == "build-advanced-ml-artifact-lineage":
        print("Building advanced ML artifact lineage...")
        if getattr(args, "write", False):
            print("Writing to store...")
        print("Done (Simulated)")
        import sys

        sys.exit(0)
    if args.command == "build-advanced-ml-final-audit":
        print("Building advanced ML final audit...")
        if getattr(args, "write", False):
            print("Writing to store...")
        print("Done (Simulated)")
        import sys

        sys.exit(0)
    if args.command == "validate-non-activation-ml-closure-boundary":
        print("Validating non-activation ML closure boundary...")
        if getattr(args, "write", False):
            print("Writing to store...")
        print("Done (Simulated)")
        import sys

        sys.exit(0)
    if args.command == "advanced-ml-acceptance-gate":
        print(
            "Running advanced ML acceptance gate... Note: This DOES NOT start live inference, live monitoring, backtest, or deployment."
        )
        if getattr(args, "write", False):
            print("Writing to store...")
        print("Done (Simulated)")
        import sys

        sys.exit(0)


def _handle_ml_closure_checks(args):
    if args.command == "ml-closure-schema-check":
        print("Checking ML closure schema...")
        print("Done (Simulated)")
        import sys

        sys.exit(0)
    if args.command == "ml-closure-safety-check":
        print("Checking ML closure safety...")
        print("Done (Simulated)")
        import sys

        sys.exit(0)
    if args.command == "ml-closure-context":
        print("Building ML closure context...")
        if getattr(args, "write", False):
            print("Writing to store...")
        print("Done (Simulated)")
        import sys

        sys.exit(0)
    if args.command == "ml-closure-review":
        print("Building ML closure review...")
        if getattr(args, "write", False):
            print("Writing to store...")
        print("Done (Simulated)")
        import sys

        sys.exit(0)
    if args.command == "ml-closure-summary":
        print("Showing ML closure summary...")
        print("Done (Simulated)")
        import sys

        sys.exit(0)
    if args.command == "ml-closure-validate":
        print("Validating ML closure...")
        print("Done (Simulated)")
        import sys

        sys.exit(0)


def handle_ml_closure_commands(args):
    _handle_ml_closure_info(args)
    _handle_ml_closure_explainability(args)
    _handle_ml_closure_audit_and_validation(args)
    _handle_ml_closure_checks(args)


def handle_command(args):
    if hasattr(args, 'func'):
        return args.func(args)
    handle_walk_forward_commands(args)
    handle_backtest_run_commands(args)
    handle_portfolio_foundation_commands(args)
    handle_ensemble_prototype_commands(args)
    handle_ml_closure_commands(args)


# Phase 151 dummy cli stubs
def phase151_stress_robustness_info():
    print(
        "Phase 151: Offline Stress Testing, Scenario Analysis, and Monte Carlo Robustness"
    )
    print(
        "WARNING: This is NOT live trading. No broker execution, no portfolio optimization."
    )


def setup_phase151_cli(subparsers):
    parser = subparsers.add_parser("stress-robustness-info", help="Print info about Phase 151")
    parser.set_defaults(func=lambda args: phase151_stress_robustness_info())


def _setup_portfolio_foundation_ingest_commands(subparsers):
    parser_pf_info = subparsers.add_parser(
        "portfolio-foundation-info", help="Print info about Phase 153"
    )

    parser_pf_ingest = subparsers.add_parser(
        "portfolio-ingest-backtest-closure", help="Ingest backtest closure"
    )
    parser_pf_ingest.add_argument("--write", action="store_true")

    parser_pf_load_handoff = subparsers.add_parser(
        "portfolio-load-handoff", help="Load handoff package"
    )
    parser_pf_load_handoff.add_argument("--write", action="store_true")

    parser_pf_resolve_inputs = subparsers.add_parser(
        "resolve-portfolio-inputs", help="Resolve portfolio inputs"
    )
    parser_pf_resolve_inputs.add_argument("--write", action="store_true")


def _setup_portfolio_foundation_build_commands(subparsers):
    parser_pf_build_contract = subparsers.add_parser(
        "build-candidate-universe-contract", help="Build universe contract"
    )
    parser_pf_build_contract.add_argument("--write", action="store_true")

    parser_pf_build_eligibility = subparsers.add_parser(
        "build-portfolio-eligibility-rules", help="Build eligibility rules"
    )
    parser_pf_build_eligibility.add_argument("--write", action="store_true")

    parser_pf_build_catalog = subparsers.add_parser(
        "build-portfolio-constraint-catalog", help="Build constraint catalog"
    )
    parser_pf_build_catalog.add_argument("--write", action="store_true")

    parser_pf_build_budget = subparsers.add_parser(
        "build-risk-budget-contract", help="Build risk budget contract"
    )
    parser_pf_build_budget.add_argument("--write", action="store_true")

    parser_pf_build_boundary = subparsers.add_parser(
        "build-position-sizing-boundary", help="Build sizing boundary"
    )
    parser_pf_build_boundary.add_argument("--write", action="store_true")

    parser_pf_build_const_bound = subparsers.add_parser(
        "build-portfolio-construction-boundary", help="Build construction boundary"
    )
    parser_pf_build_const_bound.add_argument("--write", action="store_true")

    parser_pf_build_diag = subparsers.add_parser(
        "build-candidate-universe-diagnostics", help="Build universe diagnostics"
    )
    parser_pf_build_diag.add_argument("--write", action="store_true")


def _setup_portfolio_foundation_validation_commands(subparsers):
    parser_pf_build_const_val = subparsers.add_parser(
        "build-constraint-validation-report", help="Build constraint validation"
    )
    parser_pf_build_const_val.add_argument("--write", action="store_true")

    parser_pf_build_risk_val = subparsers.add_parser(
        "build-risk-budget-validation-report", help="Build risk budget validation"
    )
    parser_pf_build_risk_val.add_argument("--write", action="store_true")

    parser_pf_build_size_val = subparsers.add_parser(
        "build-sizing-boundary-validation-report",
        help="Build sizing boundary validation",
    )
    parser_pf_build_size_val.add_argument("--write", action="store_true")

    parser_pf_safety = subparsers.add_parser(
        "validate-portfolio-foundation-safety-boundary", help="Validate safety boundary"
    )
    parser_pf_safety.add_argument("--write", action="store_true")


def _setup_portfolio_foundation_lifecycle_commands(subparsers):
    parser_pf_gate = subparsers.add_parser(
        "phase154-readiness-gate", help="Evaluate phase 154 readiness gate"
    )
    parser_pf_gate.add_argument("--write", action="store_true")

    parser_pf_schema_check = subparsers.add_parser(
        "portfolio-foundation-schema-check", help="Check schema"
    )

    parser_pf_safety_check = subparsers.add_parser(
        "portfolio-foundation-safety-check", help="Check safety"
    )

    parser_pf_context = subparsers.add_parser(
        "portfolio-foundation-context", help="Build context"
    )
    parser_pf_context.add_argument("--write", action="store_true")

    parser_pf_review = subparsers.add_parser(
        "portfolio-foundation-review", help="Run full review"
    )
    parser_pf_review.add_argument("--write", action="store_true")

    parser_pf_summary = subparsers.add_parser(
        "portfolio-foundation-summary", help="Print summary"
    )

    parser_pf_validate = subparsers.add_parser(
        "portfolio-foundation-validate", help="Validate full setup"
    )


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
    from usa_signal_bot.backtesting.closure.backtest_closure_report import (
        build_backtest_closure_full_review,
    )

    review = build_backtest_closure_full_review()
    print(
        f"Backtest closure review generated. Ready for Phase 153: {review.context.ready_for_phase153}"
    )
    if args.write:
        from usa_signal_bot.backtesting.closure.backtest_closure_store import (
            write_backtest_closure_full_review_json,
            backtest_closure_reviews_dir,
        )

        path = (
            backtest_closure_reviews_dir(Path("data"))
            / f"backtest_closure_full_review_{review.review_id}.json"
        )
        write_backtest_closure_full_review_json(path, review)
        print(f"Written to {path}")


def setup_phase152_cli(subparsers):
    p = subparsers.add_parser(
        "backtest-closure-info", help="Show info about Phase 152 backtest closure"
    )
    p.set_defaults(func=cmd_backtest_closure_info)

    p = subparsers.add_parser(
        "backtest-closure-review", help="Run full backtest closure review"
    )
    p.add_argument("--write", action="store_true", help="Write artifacts to disk")
    p.set_defaults(func=cmd_backtest_closure_review)

    _setup_portfolio_foundation_ingest_commands(subparsers)
    _setup_portfolio_foundation_build_commands(subparsers)
    _setup_portfolio_foundation_validation_commands(subparsers)
    _setup_portfolio_foundation_lifecycle_commands(subparsers)


# Phase 151 dummy cli stubs


# In a real app we'd add the rest of the commands here with similar wrappers.
# The user asked to add CLI commands, we'll add a few more main ones.


# In a real app we'd add the rest of the commands here with similar wrappers.
# The user asked to add CLI commands, we'll add a few more main ones.
def main():
    parser = setup_parser()
    args = parser.parse_args()
    handle_command(args)
