
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

@cli.command(name="drift-monitoring-info")
@click.option("--write", is_flag=True, help="Write output to data directory")
def drift_monitoring_info(write: bool):
    """Phase 144 placeholder."""
    click.echo("Phase 144 placeholder.")
    if "drift-monitoring-info" == "drift-monitoring-info":
        click.echo("Phase 144 is an offline drift baseline, monitoring metadata, and post-ensemble governance phase. No active paper trading, deployment, live inference, live monitoring, live daemon, or alert sender.")


@cli.command(name="drift-ingest-ensemble-prototype")
@click.option("--write", is_flag=True, help="Write output to data directory")
def drift_ingest_ensemble_prototype(write: bool):
    """Phase 144 placeholder."""
    click.echo("Phase 144 placeholder.")
    if "drift-ingest-ensemble-prototype" == "drift-monitoring-info":
        click.echo("Phase 144 is an offline drift baseline, monitoring metadata, and post-ensemble governance phase. No active paper trading, deployment, live inference, live monitoring, live daemon, or alert sender.")


@cli.command(name="drift-artifact-load")
@click.option("--write", is_flag=True, help="Write output to data directory")
def drift_artifact_load(write: bool):
    """Phase 144 placeholder."""
    click.echo("Phase 144 placeholder.")
    if "drift-artifact-load" == "drift-monitoring-info":
        click.echo("Phase 144 is an offline drift baseline, monitoring metadata, and post-ensemble governance phase. No active paper trading, deployment, live inference, live monitoring, live daemon, or alert sender.")


@cli.command(name="resolve-drift-inputs")
@click.option("--write", is_flag=True, help="Write output to data directory")
def resolve_drift_inputs(write: bool):
    """Phase 144 placeholder."""
    click.echo("Phase 144 placeholder.")
    if "resolve-drift-inputs" == "drift-monitoring-info":
        click.echo("Phase 144 is an offline drift baseline, monitoring metadata, and post-ensemble governance phase. No active paper trading, deployment, live inference, live monitoring, live daemon, or alert sender.")


@cli.command(name="build-monitoring-window-policy")
@click.option("--write", is_flag=True, help="Write output to data directory")
def build_monitoring_window_policy(write: bool):
    """Phase 144 placeholder."""
    click.echo("Phase 144 placeholder.")
    if "build-monitoring-window-policy" == "drift-monitoring-info":
        click.echo("Phase 144 is an offline drift baseline, monitoring metadata, and post-ensemble governance phase. No active paper trading, deployment, live inference, live monitoring, live daemon, or alert sender.")


@cli.command(name="build-drift-baseline-specs")
@click.option("--write", is_flag=True, help="Write output to data directory")
def build_drift_baseline_specs(write: bool):
    """Phase 144 placeholder."""
    click.echo("Phase 144 placeholder.")
    if "build-drift-baseline-specs" == "drift-monitoring-info":
        click.echo("Phase 144 is an offline drift baseline, monitoring metadata, and post-ensemble governance phase. No active paper trading, deployment, live inference, live monitoring, live daemon, or alert sender.")


@cli.command(name="build-feature-drift-baseline")
@click.option("--write", is_flag=True, help="Write output to data directory")
def build_feature_drift_baseline(write: bool):
    """Phase 144 placeholder."""
    click.echo("Phase 144 placeholder.")
    if "build-feature-drift-baseline" == "drift-monitoring-info":
        click.echo("Phase 144 is an offline drift baseline, monitoring metadata, and post-ensemble governance phase. No active paper trading, deployment, live inference, live monitoring, live daemon, or alert sender.")


@cli.command(name="build-prediction-drift-baseline")
@click.option("--write", is_flag=True, help="Write output to data directory")
def build_prediction_drift_baseline(write: bool):
    """Phase 144 placeholder."""
    click.echo("Phase 144 placeholder.")
    if "build-prediction-drift-baseline" == "drift-monitoring-info":
        click.echo("Phase 144 is an offline drift baseline, monitoring metadata, and post-ensemble governance phase. No active paper trading, deployment, live inference, live monitoring, live daemon, or alert sender.")


@cli.command(name="build-score-distribution-drift")
@click.option("--write", is_flag=True, help="Write output to data directory")
def build_score_distribution_drift(write: bool):
    """Phase 144 placeholder."""
    click.echo("Phase 144 placeholder.")
    if "build-score-distribution-drift" == "drift-monitoring-info":
        click.echo("Phase 144 is an offline drift baseline, monitoring metadata, and post-ensemble governance phase. No active paper trading, deployment, live inference, live monitoring, live daemon, or alert sender.")


@cli.command(name="build-calibration-drift-baseline")
@click.option("--write", is_flag=True, help="Write output to data directory")
def build_calibration_drift_baseline(write: bool):
    """Phase 144 placeholder."""
    click.echo("Phase 144 placeholder.")
    if "build-calibration-drift-baseline" == "drift-monitoring-info":
        click.echo("Phase 144 is an offline drift baseline, monitoring metadata, and post-ensemble governance phase. No active paper trading, deployment, live inference, live monitoring, live daemon, or alert sender.")


@cli.command(name="build-residual-drift-baseline")
@click.option("--write", is_flag=True, help="Write output to data directory")
def build_residual_drift_baseline(write: bool):
    """Phase 144 placeholder."""
    click.echo("Phase 144 placeholder.")
    if "build-residual-drift-baseline" == "drift-monitoring-info":
        click.echo("Phase 144 is an offline drift baseline, monitoring metadata, and post-ensemble governance phase. No active paper trading, deployment, live inference, live monitoring, live daemon, or alert sender.")


@cli.command(name="build-label-distribution-drift")
@click.option("--write", is_flag=True, help="Write output to data directory")
def build_label_distribution_drift(write: bool):
    """Phase 144 placeholder."""
    click.echo("Phase 144 placeholder.")
    if "build-label-distribution-drift" == "drift-monitoring-info":
        click.echo("Phase 144 is an offline drift baseline, monitoring metadata, and post-ensemble governance phase. No active paper trading, deployment, live inference, live monitoring, live daemon, or alert sender.")


@cli.command(name="build-regime-drift-baseline")
@click.option("--write", is_flag=True, help="Write output to data directory")
def build_regime_drift_baseline(write: bool):
    """Phase 144 placeholder."""
    click.echo("Phase 144 placeholder.")
    if "build-regime-drift-baseline" == "drift-monitoring-info":
        click.echo("Phase 144 is an offline drift baseline, monitoring metadata, and post-ensemble governance phase. No active paper trading, deployment, live inference, live monitoring, live daemon, or alert sender.")


@cli.command(name="calculate-drift-metrics")
@click.option("--write", is_flag=True, help="Write output to data directory")
def calculate_drift_metrics(write: bool):
    """Phase 144 placeholder."""
    click.echo("Phase 144 placeholder.")
    if "calculate-drift-metrics" == "drift-monitoring-info":
        click.echo("Phase 144 is an offline drift baseline, monitoring metadata, and post-ensemble governance phase. No active paper trading, deployment, live inference, live monitoring, live daemon, or alert sender.")


@cli.command(name="build-monitoring-snapshot")
@click.option("--write", is_flag=True, help="Write output to data directory")
def build_monitoring_snapshot(write: bool):
    """Phase 144 placeholder."""
    click.echo("Phase 144 placeholder.")
    if "build-monitoring-snapshot" == "drift-monitoring-info":
        click.echo("Phase 144 is an offline drift baseline, monitoring metadata, and post-ensemble governance phase. No active paper trading, deployment, live inference, live monitoring, live daemon, or alert sender.")


@cli.command(name="build-alert-rule-metadata")
@click.option("--write", is_flag=True, help="Write output to data directory")
def build_alert_rule_metadata(write: bool):
    """Phase 144 placeholder."""
    click.echo("Phase 144 placeholder.")
    if "build-alert-rule-metadata" == "drift-monitoring-info":
        click.echo("Phase 144 is an offline drift baseline, monitoring metadata, and post-ensemble governance phase. No active paper trading, deployment, live inference, live monitoring, live daemon, or alert sender.")


@cli.command(name="build-monitoring-metadata-package")
@click.option("--write", is_flag=True, help="Write output to data directory")
def build_monitoring_metadata_package(write: bool):
    """Phase 144 placeholder."""
    click.echo("Phase 144 placeholder.")
    if "build-monitoring-metadata-package" == "drift-monitoring-info":
        click.echo("Phase 144 is an offline drift baseline, monitoring metadata, and post-ensemble governance phase. No active paper trading, deployment, live inference, live monitoring, live daemon, or alert sender.")


@cli.command(name="build-post-ensemble-governance")
@click.option("--write", is_flag=True, help="Write output to data directory")
def build_post_ensemble_governance(write: bool):
    """Phase 144 placeholder."""
    click.echo("Phase 144 placeholder.")
    if "build-post-ensemble-governance" == "drift-monitoring-info":
        click.echo("Phase 144 is an offline drift baseline, monitoring metadata, and post-ensemble governance phase. No active paper trading, deployment, live inference, live monitoring, live daemon, or alert sender.")


@cli.command(name="validate-non-activation-drift-boundary")
@click.option("--write", is_flag=True, help="Write output to data directory")
def validate_non_activation_drift_boundary(write: bool):
    """Phase 144 placeholder."""
    click.echo("Phase 144 placeholder.")
    if "validate-non-activation-drift-boundary" == "drift-monitoring-info":
        click.echo("Phase 144 is an offline drift baseline, monitoring metadata, and post-ensemble governance phase. No active paper trading, deployment, live inference, live monitoring, live daemon, or alert sender.")


@cli.command(name="update-model-cards-with-drift")
@click.option("--write", is_flag=True, help="Write output to data directory")
def update_model_cards_with_drift(write: bool):
    """Phase 144 placeholder."""
    click.echo("Phase 144 placeholder.")
    if "update-model-cards-with-drift" == "drift-monitoring-info":
        click.echo("Phase 144 is an offline drift baseline, monitoring metadata, and post-ensemble governance phase. No active paper trading, deployment, live inference, live monitoring, live daemon, or alert sender.")


@cli.command(name="drift-readiness-gate")
@click.option("--write", is_flag=True, help="Write output to data directory")
def drift_readiness_gate(write: bool):
    """Phase 144 placeholder."""
    click.echo("Phase 144 placeholder.")
    if "drift-readiness-gate" == "drift-monitoring-info":
        click.echo("Phase 144 is an offline drift baseline, monitoring metadata, and post-ensemble governance phase. No active paper trading, deployment, live inference, live monitoring, live daemon, or alert sender.")


@cli.command(name="drift-schema-check")
@click.option("--write", is_flag=True, help="Write output to data directory")
def drift_schema_check(write: bool):
    """Phase 144 placeholder."""
    click.echo("Phase 144 placeholder.")
    if "drift-schema-check" == "drift-monitoring-info":
        click.echo("Phase 144 is an offline drift baseline, monitoring metadata, and post-ensemble governance phase. No active paper trading, deployment, live inference, live monitoring, live daemon, or alert sender.")


@cli.command(name="drift-safety-check")
@click.option("--write", is_flag=True, help="Write output to data directory")
def drift_safety_check(write: bool):
    """Phase 144 placeholder."""
    click.echo("Phase 144 placeholder.")
    if "drift-safety-check" == "drift-monitoring-info":
        click.echo("Phase 144 is an offline drift baseline, monitoring metadata, and post-ensemble governance phase. No active paper trading, deployment, live inference, live monitoring, live daemon, or alert sender.")


@cli.command(name="drift-monitoring-context")
@click.option("--write", is_flag=True, help="Write output to data directory")
def drift_monitoring_context(write: bool):
    """Phase 144 placeholder."""
    click.echo("Phase 144 placeholder.")
    if "drift-monitoring-context" == "drift-monitoring-info":
        click.echo("Phase 144 is an offline drift baseline, monitoring metadata, and post-ensemble governance phase. No active paper trading, deployment, live inference, live monitoring, live daemon, or alert sender.")


@cli.command(name="drift-monitoring-review")
@click.option("--write", is_flag=True, help="Write output to data directory")
def drift_monitoring_review(write: bool):
    """Phase 144 placeholder."""
    click.echo("Phase 144 placeholder.")
    if "drift-monitoring-review" == "drift-monitoring-info":
        click.echo("Phase 144 is an offline drift baseline, monitoring metadata, and post-ensemble governance phase. No active paper trading, deployment, live inference, live monitoring, live daemon, or alert sender.")


@cli.command(name="drift-monitoring-summary")
@click.option("--write", is_flag=True, help="Write output to data directory")
def drift_monitoring_summary(write: bool):
    """Phase 144 placeholder."""
    click.echo("Phase 144 placeholder.")
    if "drift-monitoring-summary" == "drift-monitoring-info":
        click.echo("Phase 144 is an offline drift baseline, monitoring metadata, and post-ensemble governance phase. No active paper trading, deployment, live inference, live monitoring, live daemon, or alert sender.")


@cli.command(name="drift-monitoring-validate")
@click.option("--write", is_flag=True, help="Write output to data directory")
def drift_monitoring_validate(write: bool):
    """Phase 144 placeholder."""
    click.echo("Phase 144 placeholder.")
    if "drift-monitoring-validate" == "drift-monitoring-info":
        click.echo("Phase 144 is an offline drift baseline, monitoring metadata, and post-ensemble governance phase. No active paper trading, deployment, live inference, live monitoring, live daemon, or alert sender.")
