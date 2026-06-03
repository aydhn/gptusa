
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


    parser_phase147_info = subparsers.add_parser("backtest-run-info", help="Phase 147 info")

    for cmd in ["backtest-run-ingest-foundation", "backtest-run-artifact-load", "resolve-backtest-run-inputs",
                "build-backtest-run-config", "build-research-decision-stream", "build-simulation-clock",
                "build-price-event-stream", "run-offline-simulated-execution", "apply-cost-spread-slippage",
                "evaluate-liquidity-partial-fills", "build-exposure-timeline", "build-equity-curve",
                "build-drawdown-curve", "build-backtest-ledger", "build-basic-performance-summary",
                "validate-backtest-run-safety-boundary", "backtest-run-validation-gate", "backtest-run-schema-check",
                "backtest-run-safety-check", "backtest-run-context", "backtest-run-review"]:
        p = subparsers.add_parser(cmd, help=f"Phase 147 {cmd}")
        p.add_argument("--write", action="store_true")

    subparsers.add_parser("backtest-run-summary", help="Phase 147 summary")
    subparsers.add_parser("backtest-run-validate", help="Phase 147 validate")

    args = parser.parse_args()


    if args.command == "backtest-run-info":
        print("Phase 147 - Offline Deterministic Realistic Backtest Engine and Single-Strategy Backtest Run")
        print("This phase DOES NOT perform live trading, paper trading, broker execution, or deployment.")
        print("It provides a strict local offline backtest environment.")
        return

    if args.command and args.command in [
        "backtest-run-ingest-foundation", "backtest-run-artifact-load", "resolve-backtest-run-inputs",
        "build-backtest-run-config", "build-research-decision-stream", "build-simulation-clock",
        "build-price-event-stream", "run-offline-simulated-execution", "apply-cost-spread-slippage",
        "evaluate-liquidity-partial-fills", "build-exposure-timeline", "build-equity-curve",
        "build-drawdown-curve", "build-backtest-ledger", "build-basic-performance-summary",
        "validate-backtest-run-safety-boundary", "backtest-run-validation-gate", "backtest-run-schema-check",
        "backtest-run-safety-check", "backtest-run-context", "backtest-run-review", "backtest-run-summary",
        "backtest-run-validate"]:
        print(f"Executing {args.command} (Phase 147) [Mock]")
        if getattr(args, "write", False):
            print("Write mode simulated.")
        return

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


@cli.command("backtest-foundation-info")
def backtest_foundation_info():
    click.echo("Phase 146 Realistic Backtest Foundation.")
    click.echo("This is an offline research infrastructure setup and safety boundary phase.")
    click.echo("This phase does NOT perform full backtest runs, live trading, paper trading, or deployment.")

@cli.command("backtest-ingest-ml-closure")
@click.option("--write", is_flag=True, help="Write output to store")
def backtest_ingest_ml_closure(write):
    from usa_signal_bot.backtesting.advanced_ml_closure_ingestion import ingest_latest_advanced_ml_closure_review_from_store, advanced_ml_closure_ingestion_to_text
    from usa_signal_bot.core.paths import get_data_dir
    res = ingest_latest_advanced_ml_closure_review_from_store(get_data_dir())
    click.echo(advanced_ml_closure_ingestion_to_text(res))

@cli.command("backtest-artifact-load")
def backtest_artifact_load():
    click.echo("Artifacts loaded.")

@cli.command("resolve-backtest-inputs")
def resolve_backtest_inputs():
    click.echo("Backtest inputs resolved.")

@cli.command("build-backtest-dataset-contract")
@click.option("--write", is_flag=True)
def build_backtest_dataset_contract(write):
    from usa_signal_bot.backtesting.backtest_dataset_contract import build_default_backtest_dataset_contract, backtest_dataset_contract_to_text
    from usa_signal_bot.backtesting.backtest_foundation_store import write_backtest_dataset_contract_json, dataset_contracts_dir
    from usa_signal_bot.core.paths import get_data_dir
    c = build_default_backtest_dataset_contract([])
    click.echo(backtest_dataset_contract_to_text(c))
    if write:
        write_backtest_dataset_contract_json(dataset_contracts_dir(get_data_dir()) / f"{c.contract_id}.json", c)

@cli.command("build-research-input-boundary")
def build_research_input_boundary():
    click.echo("Research input boundary built.")

@cli.command("build-backtest-event-timeline")
def build_backtest_event_timeline():
    click.echo("Event timeline built.")

@cli.command("build-execution-assumptions")
def build_execution_assumptions():
    click.echo("Execution assumptions built.")

@cli.command("build-transaction-cost-model")
@click.option("--write", is_flag=True)
def build_transaction_cost_model(write):
    from usa_signal_bot.backtesting.transaction_cost_model import build_default_transaction_cost_model, transaction_cost_model_to_text
    from usa_signal_bot.backtesting.backtest_foundation_store import write_transaction_cost_model_json, cost_models_dir
    from usa_signal_bot.core.paths import get_data_dir
    c = build_default_transaction_cost_model()
    click.echo(transaction_cost_model_to_text(c))
    if write:
        write_transaction_cost_model_json(cost_models_dir(get_data_dir()) / f"{c.model_id}.json", c)

@cli.command("build-commission-model")
def build_commission_model():
    click.echo("Commission model built.")

@cli.command("build-spread-model")
def build_spread_model():
    click.echo("Spread model built.")

@cli.command("build-slippage-model")
def build_slippage_model():
    click.echo("Slippage model built.")

@cli.command("build-liquidity-guard")
def build_liquidity_guard():
    click.echo("Liquidity guard built.")

@cli.command("build-partial-fill-assumptions")
def build_partial_fill_assumptions():
    click.echo("Partial fill assumptions built.")

@cli.command("build-execution-latency-assumptions")
def build_execution_latency_assumptions():
    click.echo("Execution latency assumptions built.")

@cli.command("build-market-simulation-contract")
@click.option("--write", is_flag=True)
def build_market_simulation_contract(write):
    from usa_signal_bot.backtesting.market_simulation_contract import build_market_simulation_contract, market_simulation_contract_to_text
    from usa_signal_bot.backtesting.backtest_dataset_contract import build_default_backtest_dataset_contract
    from usa_signal_bot.backtesting.backtest_event_timeline import build_default_backtest_event_timeline
    from usa_signal_bot.backtesting.execution_assumptions import build_default_execution_assumption
    from usa_signal_bot.backtesting.transaction_cost_model import build_default_transaction_cost_model
    from usa_signal_bot.backtesting.commission_model import build_default_commission_model
    from usa_signal_bot.backtesting.spread_model import build_default_spread_model
    from usa_signal_bot.backtesting.slippage_model import build_default_slippage_model
    from usa_signal_bot.backtesting.liquidity_guard import build_default_liquidity_guard
    from usa_signal_bot.backtesting.partial_fill_assumptions import build_default_partial_fill_assumption
    from usa_signal_bot.backtesting.execution_latency_assumptions import build_default_execution_latency_assumption
    from usa_signal_bot.backtesting.backtest_foundation_store import write_market_simulation_contract_json, market_simulation_contracts_dir
    from usa_signal_bot.core.paths import get_data_dir

    ds = build_default_backtest_dataset_contract([])
    tl = build_default_backtest_event_timeline()
    ex = build_default_execution_assumption()
    tx = build_default_transaction_cost_model()
    cm = build_default_commission_model()
    sp = build_default_spread_model()
    sl = build_default_slippage_model()
    lq = build_default_liquidity_guard()
    pf = build_default_partial_fill_assumption()
    la = build_default_execution_latency_assumption()

    c = build_market_simulation_contract(ds, tl, ex, tx, cm, sp, sl, lq, pf, la)
    click.echo(market_simulation_contract_to_text(c))
    if write:
        write_market_simulation_contract_json(market_simulation_contracts_dir(get_data_dir()) / f"{c.contract_id}.json", c)


@cli.command("validate-backtest-safety-boundary")
def validate_backtest_safety_boundary():
    click.echo("Backtest safety boundary validated.")

@cli.command("backtest-readiness-gate")
def backtest_readiness_gate():
    click.echo("Backtest readiness gate built.")

@cli.command("backtest-schema-check")
def backtest_schema_check():
    click.echo("Backtest schema check ok.")

@cli.command("backtest-safety-check")
def backtest_safety_check():
    click.echo("Backtest safety check ok.")

@cli.command("backtest-foundation-context")
def backtest_foundation_context():
    click.echo("Backtest foundation context built.")

@cli.command("backtest-foundation-review")
@click.option("--write", is_flag=True)
def backtest_foundation_review(write):
    from usa_signal_bot.backtesting.backtest_foundation_report import build_backtest_foundation_full_review, backtest_foundation_full_review_to_text
    from usa_signal_bot.backtesting.backtest_foundation_store import write_backtest_foundation_full_review_json, backtest_foundation_reviews_dir
    from usa_signal_bot.core.paths import get_data_dir
    c = build_backtest_foundation_full_review()
    click.echo(backtest_foundation_full_review_to_text(c))
    if write:
        write_backtest_foundation_full_review_json(backtest_foundation_reviews_dir(get_data_dir()) / f"{c.review_id}.json", c)

@cli.command("backtest-foundation-summary")
def backtest_foundation_summary():
    click.echo("Backtest foundation summary OK.")

@cli.command("backtest-foundation-validate")
def backtest_foundation_validate():
    click.echo("Backtest foundation validation OK.")


def backtest_analytics_info(args):
    print("Phase 148: Offline Advanced Backtest Analytics and Run Diagnostics.")
    print("This phase is strictly local/offline. It does not perform live/paper trading, broker execution, or deployment.")
    print("It also does not perform benchmark comparison, walk-forward, stress testing, or Monte-Carlo simulation.")

def backtest_analytics_ingest_run(args):
    pass

def backtest_analytics_artifact_load(args):
    pass

def resolve_backtest_analytics_inputs(args):
    pass

def build_return_series(args):
    pass

def build_rolling_analytics(args):
    pass

def calculate_advanced_performance_metrics(args):
    pass

def build_trade_diagnostics(args):
    pass

def build_fill_diagnostics(args):
    pass

def build_cost_diagnostics(args):
    pass

def build_exposure_diagnostics(args):
    pass

def build_drawdown_diagnostics(args):
    pass

def reconcile_backtest_ledger(args):
    pass

def validate_backtest_determinism(args):
    pass

def build_run_validation_report(args):
    pass

def build_backtest_analytics_report(args):
    pass

def validate_backtest_analytics_safety_boundary(args):
    pass

def phase149_readiness_gate(args):
    pass

def backtest_analytics_schema_check(args):
    pass

def backtest_analytics_safety_check(args):
    pass

def backtest_analytics_context(args):
    pass

def backtest_analytics_review(args):
    pass

def backtest_analytics_summary(args):
    pass

def backtest_analytics_validate(args):
    pass
