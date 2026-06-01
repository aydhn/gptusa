
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
