
from usa_signal_bot.ml_research.ensemble_evaluation.ensemble_prototype_report import build_ensemble_prototype_full_review, ensemble_prototype_full_review_to_text, ensemble_prototype_limitations_text
from usa_signal_bot.ml_research.ensemble_evaluation.ensemble_prototype_store import write_ensemble_prototype_full_review_json, ensemble_prototype_reviews_dir
from pathlib import Path

import argparse
import sys

def mock_cli():
    pass

# Read original
with open("usa_signal_bot/app/cli.py", "r") as f:
    content = f.read()

def main():
    parser = argparse.ArgumentParser(prog='python -m usa_signal_bot')
    subparsers = parser.add_subparsers(dest='command')

    parser_ensemble_info = subparsers.add_parser("ensemble-prototype-info", help="Print info about Phase 143")

    parser_ensemble_review = subparsers.add_parser("ensemble-prototype-review", help="Run full Phase 143 review")
    parser_ensemble_review.add_argument("--write", action="store_true")

    parser_ensemble_build_specs = subparsers.add_parser("build-ensemble-prototype-specs", help="Build specs")
    parser_ensemble_build_specs.add_argument("--write", action="store_true")

    parser_ensemble_pred = subparsers.add_parser("generate-offline-ensemble-predictions", help="Generate predictions")
    parser_ensemble_pred.add_argument("--write", action="store_true")

    parser_ensemble_diag = subparsers.add_parser("build-blend-diagnostics", help="Build diagnostics")
    parser_ensemble_diag.add_argument("--write", action="store_true")

    for cmd in ["ensemble-prototype-ingest-scaffolding", "ensemble-prototype-artifact-load",
                "resolve-ensemble-prototype-inputs", "build-candidate-agreement-diagnostics",
                "build-ensemble-candidate-comparison", "calculate-offline-ensemble-evaluation-metrics",
                "build-offline-ensemble-evaluation-reports", "build-non-activation-ensemble-registry",
                "update-model-cards-with-ensemble-evaluation", "validate-ensemble-prototype-boundary",
                "ensemble-prototype-readiness-gate", "ensemble-prototype-schema-check",
                "ensemble-prototype-safety-check", "ensemble-prototype-context",
                "ensemble-prototype-summary", "ensemble-prototype-validate"]:
        p = subparsers.add_parser(cmd, help=f"Phase 143 {cmd}")
        p.add_argument("--write", action="store_true")


    parser_ml_closure_info = subparsers.add_parser("ml-closure-info", help="Display information about Phase 145 ML Governance Closure.")

    parser_ingest = subparsers.add_parser("ml-closure-ingest-drift-monitoring", help="Ingest Drift Monitoring output (Simulated)")
    parser_ingest.add_argument("--write", action="store_true")

    parser_load = subparsers.add_parser("ml-closure-artifact-load", help="Load Artifacts (Simulated)")
    parser_load.add_argument("--write", action="store_true")

    parser_resolve = subparsers.add_parser("resolve-explainability-inputs", help="Resolve Explainability Inputs (Simulated)")
    parser_resolve.add_argument("--write", action="store_true")

    parser_feat_attr = subparsers.add_parser("build-feature-attribution-proxy", help="Build Feature Attribution Proxy (Simulated)")
    parser_feat_attr.add_argument("--write", action="store_true")

    parser_fact_cont = subparsers.add_parser("build-factor-contribution-summary", help="Build Factor Contribution Summary (Simulated)")
    parser_fact_cont.add_argument("--write", action="store_true")

    parser_mod_behav = subparsers.add_parser("build-model-behavior-explanation", help="Build Model Behavior Explanation (Simulated)")
    parser_mod_behav.add_argument("--write", action="store_true")

    parser_regime_exp = subparsers.add_parser("build-regime-aware-explanation", help="Build Regime Aware Explanation (Simulated)")
    parser_regime_exp.add_argument("--write", action="store_true")

    parser_cal_exp = subparsers.add_parser("build-calibration-aware-explanation", help="Build Calibration Aware Explanation (Simulated)")
    parser_cal_exp.add_argument("--write", action="store_true")

    parser_ens_exp = subparsers.add_parser("build-ensemble-explanation", help="Build Ensemble Explanation (Simulated)")
    parser_ens_exp.add_argument("--write", action="store_true")

    parser_exp_rep = subparsers.add_parser("build-explainability-report", help="Build Explainability Report (Simulated)")
    parser_exp_rep.add_argument("--write", action="store_true")

    parser_art_lin = subparsers.add_parser("build-advanced-ml-artifact-lineage", help="Build Advanced ML Artifact Lineage (Simulated)")
    parser_art_lin.add_argument("--write", action="store_true")

    parser_gov_clos = subparsers.add_parser("build-ml-governance-closure", help="Build ML Governance Closure (Simulated)")
    parser_gov_clos.add_argument("--write", action="store_true")

    parser_fin_aud = subparsers.add_parser("build-advanced-ml-final-audit", help="Build Advanced ML Final Audit (Simulated)")
    parser_fin_aud.add_argument("--write", action="store_true")

    parser_na_bound = subparsers.add_parser("validate-non-activation-ml-closure-boundary", help="Validate Non Activation ML Closure Boundary (Simulated)")
    parser_na_bound.add_argument("--write", action="store_true")

    parser_fin_mc = subparsers.add_parser("build-final-ml-model-card-closure", help="Build Final ML Model Card Closure (Simulated)")
    parser_fin_mc.add_argument("--write", action="store_true")

    parser_acc_gate = subparsers.add_parser("advanced-ml-acceptance-gate", help="Run Advanced ML Acceptance Gate (Simulated)")
    parser_acc_gate.add_argument("--write", action="store_true")

    parser_sch_chk = subparsers.add_parser("ml-closure-schema-check", help="Check ML Closure Schema (Simulated)")
    parser_saf_chk = subparsers.add_parser("ml-closure-safety-check", help="Check ML Closure Safety (Simulated)")

    parser_ctx = subparsers.add_parser("ml-closure-context", help="Build ML Closure Context (Simulated)")
    parser_ctx.add_argument("--write", action="store_true")

    parser_rev = subparsers.add_parser("ml-closure-review", help="Build ML Closure Review (Simulated)")
    parser_rev.add_argument("--write", action="store_true")

    parser_sum = subparsers.add_parser("ml-closure-summary", help="Show ML Closure Summary (Simulated)")
    parser_val = subparsers.add_parser("ml-closure-validate", help="Validate ML Closure (Simulated)")

    args = parser.parse_args()

    if args.command == "ensemble-prototype-info":
        print("Phase 143 is an offline ensemble prototype evaluation, blend diagnostics, and non-activation ensemble registry phase. It is NOT active paper trading, deployment, live inference, or live daemon.")
        print(ensemble_prototype_limitations_text())
        return

    if args.command == "ensemble-prototype-review":
        review = build_ensemble_prototype_full_review()
        if args.write:
            write_ensemble_prototype_full_review_json(ensemble_prototype_reviews_dir(Path("data")) / "latest_review.json", review)
            print("Wrote review to data/ml_research/ensemble_evaluation/reviews/latest_review.json")
        else:
            print(ensemble_prototype_full_review_to_text(review))
        return

    if args.command and args.command.startswith("ensemble-prototype") or args.command in [
        "build-ensemble-prototype-specs", "generate-offline-ensemble-predictions",
        "build-blend-diagnostics", "resolve-ensemble-prototype-inputs",
        "build-candidate-agreement-diagnostics", "build-ensemble-candidate-comparison",
        "calculate-offline-ensemble-evaluation-metrics", "build-offline-ensemble-evaluation-reports",
        "build-non-activation-ensemble-registry", "update-model-cards-with-ensemble-evaluation",
        "validate-ensemble-prototype-boundary"]:

        print(f"Executing {args.command} (Phase 143) [Mock]")
        if args.write:
            print("Write mode simulated.")
        return
















































































    if args.command == "ml-closure-info":
        print("Phase 145 - Advanced ML Band Final Audit and ML Governance Closure")
        print("This phase is for explainability metadata, final ML governance closure and Advanced ML band final audit.")
        print("It DOES NOT run active paper trading, deployment, live inference, live monitoring, live daemon, or backtests.")
        sys.exit(0)
    elif args.command == "ml-closure-ingest-drift-monitoring":
        print("Ingesting Drift Monitoring output...")
        if getattr(args, "write", False): print("Writing to store...")
        print("Done (Simulated)")
        sys.exit(0)
    elif args.command == "ml-closure-artifact-load":
        print("Loading artifacts...")
        if getattr(args, "write", False): print("Writing to store...")
        print("Done (Simulated)")
        sys.exit(0)
    elif args.command == "resolve-explainability-inputs":
        print("Resolving explainability inputs...")
        if getattr(args, "write", False): print("Writing to store...")
        print("Done (Simulated)")
        sys.exit(0)
    elif args.command == "build-feature-attribution-proxy":
        print("Building feature attribution proxies... Note: These are NOT trade signals.")
        if getattr(args, "write", False): print("Writing to store...")
        print("Done (Simulated)")
        sys.exit(0)
    elif args.command == "build-factor-contribution-summary":
        print("Building factor contribution summaries... Note: These are NOT portfolio weights or allocations.")
        if getattr(args, "write", False): print("Writing to store...")
        print("Done (Simulated)")
        sys.exit(0)
    elif args.command == "build-model-behavior-explanation":
        print("Building model behavior explanations...")
        if getattr(args, "write", False): print("Writing to store...")
        print("Done (Simulated)")
        sys.exit(0)
    elif args.command == "build-regime-aware-explanation":
        print("Building regime aware explanations...")
        if getattr(args, "write", False): print("Writing to store...")
        print("Done (Simulated)")
        sys.exit(0)
    elif args.command == "build-calibration-aware-explanation":
        print("Building calibration aware explanations...")
        if getattr(args, "write", False): print("Writing to store...")
        print("Done (Simulated)")
        sys.exit(0)
    elif args.command == "build-ensemble-explanation":
        print("Building ensemble explanations...")
        if getattr(args, "write", False): print("Writing to store...")
        print("Done (Simulated)")
        sys.exit(0)
    elif args.command == "build-explainability-report":
        print("Building explainability report...")
        if getattr(args, "write", False): print("Writing to store...")
        print("Done (Simulated)")
        sys.exit(0)
    elif args.command == "build-advanced-ml-artifact-lineage":
        print("Building advanced ML artifact lineage...")
        if getattr(args, "write", False): print("Writing to store...")
        print("Done (Simulated)")
        sys.exit(0)
    elif args.command == "build-ml-governance-closure":
        print("Building ML governance closure... Note: This does NOT produce strategy activation.")
        if getattr(args, "write", False): print("Writing to store...")
        print("Done (Simulated)")
        sys.exit(0)
    elif args.command == "build-advanced-ml-final-audit":
        print("Building advanced ML final audit...")
        if getattr(args, "write", False): print("Writing to store...")
        print("Done (Simulated)")
        sys.exit(0)
    elif args.command == "validate-non-activation-ml-closure-boundary":
        print("Validating non-activation ML closure boundary...")
        if getattr(args, "write", False): print("Writing to store...")
        print("Done (Simulated)")
        sys.exit(0)
    elif args.command == "build-final-ml-model-card-closure":
        print("Building final ML model card closure...")
        if getattr(args, "write", False): print("Writing to store...")
        print("Done (Simulated)")
        sys.exit(0)
    elif args.command == "advanced-ml-acceptance-gate":
        print("Running advanced ML acceptance gate... Note: This DOES NOT start live inference, live monitoring, backtest, or deployment.")
        if getattr(args, "write", False): print("Writing to store...")
        print("Done (Simulated)")
        sys.exit(0)
    elif args.command == "ml-closure-schema-check":
        print("Checking ML closure schema...")
        print("Done (Simulated)")
        sys.exit(0)
    elif args.command == "ml-closure-safety-check":
        print("Checking ML closure safety...")
        print("Done (Simulated)")
        sys.exit(0)
    elif args.command == "ml-closure-context":
        print("Building ML closure context...")
        if getattr(args, "write", False): print("Writing to store...")
        print("Done (Simulated)")
        sys.exit(0)
    elif args.command == "ml-closure-review":
        print("Building ML closure review...")
        if getattr(args, "write", False): print("Writing to store...")
        print("Done (Simulated)")
        sys.exit(0)
    elif args.command == "ml-closure-summary":
        print("Showing ML closure summary...")
        print("Done (Simulated)")
        sys.exit(0)
    elif args.command == "ml-closure-validate":
        print("Validating ML closure...")
        print("Done (Simulated)")
        sys.exit(0)
