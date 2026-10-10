"""CLI: ``ml-loop-train`` (offline, registers a CANDIDATE and runs the gate) and ``ml-loop-approve``."""

from __future__ import annotations

from datetime import datetime, timezone

from usa_signal_bot.evidence.data import load_csv_market, synthetic_market
from usa_signal_bot.evidence.universe import PointInTimeUniverse
from usa_signal_bot.ml_loop.registry import ModelRegistry, PromotionThresholds
from usa_signal_bot.ml_loop.training import run_training


def _clock() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def cmd_ml_loop_train(args) -> None:
    data = load_csv_market(args.csv_dir, args.memberships) if args.source == "csv" else synthetic_market(seed=args.seed)
    members = PointInTimeUniverse.from_frame(data.memberships).membership_matrix(data.prices.index, data.prices.columns)
    res = run_training(data.prices, members, ridge_alpha=args.ridge_alpha)
    reg = ModelRegistry(args.registry_dir, _clock)
    rec = reg.register(args.model_id, res.params, res.metrics, res.fingerprint, res.leakage.clean)
    rec = reg.evaluate_promotion(rec.model_id, PromotionThresholds())
    print(f"Data: {data.label} | model={rec.model_id} | status={rec.status}")
    print(f"OOS rank IC {res.metrics['oos_ic_mean']:.4f} vs baseline {res.metrics['baseline_ic_mean']:.4f}; "
          f"positive folds {res.metrics['positive_fold_fraction']:.0%}; leakage clean={res.leakage.clean}")
    for r in rec.gate_reasons:
        print(f"  gate: {r}")
    print("activation_allowed=False; ELIGIBLE models still need `ml-loop-approve` by a named human. Research only.")


def cmd_ml_loop_cpcv(args) -> None:
    """Tree models (+ optional meta-labeling) on CPCV paths; registers a CANDIDATE and runs the CPCV+DSR+SPA gate."""
    from pathlib import Path

    from usa_signal_bot.evidence.cli import _cash_rate, _hlog
    from usa_signal_bot.evidence.costs import CostModel
    from usa_signal_bot.ml_loop.drift import feature_drift
    from usa_signal_bot.ml_loop.registry import CpcvThresholds
    from usa_signal_bot.ml_loop.retrain_trigger import evaluate_retrain
    from usa_signal_bot.ml_loop.tree_cpcv import build_features, run_tree_cpcv

    data = load_csv_market(args.csv_dir, args.memberships) if args.source == "csv" else synthetic_market(seed=args.seed)
    members = PointInTimeUniverse.from_frame(data.memberships).membership_matrix(data.prices.index, data.prices.columns)
    hlog = _hlog(args)
    n_trials = (hlog.n_trials(data.label) + 1) if hlog else args.trials
    var_sr = hlog.sharpe_variance(data.label) if hlog and hlog.n_trials(data.label) > 1 else None
    res = run_tree_cpcv(data.prices, members, CostModel(args.commission_bps, args.slippage_bps), _cash_rate(args),
                        kind=args.model, meta_labeling=args.meta, n_trials=n_trials, var_sr_trials=var_sr, seed=args.seed)
    if hlog:
        med = float(sorted(res.path_sharpe)[len(res.path_sharpe) // 2]) / (252 ** 0.5)
        hlog.append(f"ml-cpcv-seed{args.seed}", f"ML {args.model}{' +meta' if args.meta else ''}", {"top_frac": 0.3}, len(data.prices), med, data.label)
    model_id = args.model_id or f"cpcv_{args.model}{'_meta' if args.meta else ''}_{_clock()}".replace(":", "")
    reg = ModelRegistry(args.registry_dir, _clock)
    reg.register(model_id, {"model": float(args.model == "rf"), "meta": float(args.meta)}, res.metrics(), res.fingerprint, res.leakage_clean)
    rec = reg.evaluate_cpcv_promotion(model_id, CpcvThresholds())
    x, _ = build_features(data.prices, members, 5)
    half = len(x) // 2
    drift = evaluate_retrain(feature_drift(x.iloc[:half], x.iloc[half:]))
    lines = [f"Data: {data.label} | model={model_id} | status={rec.status} | trials(N)={n_trials}",
             f"CPCV paths={res.n_paths}: median path CAGR {rec.metrics['median_path_cagr']:.1%} vs benchmark {res.bench_cagr:.1%}; "
             f"median excess Sharpe {rec.metrics['median_path_excess_sharpe']:.2f}; positive paths {rec.metrics['positive_path_fraction']:.0%}",
             f"DSR(excess)={res.dsr_excess:.2f}, SPA p={res.spa_p:.3f}, leakage clean={res.leakage_clean}",
             f"Drift (first vs second half features): triggered={drift.triggered} {drift.reasons[:3]}"]
    lines += [f"  gate: {r}" for r in rec.gate_reasons]
    lines.append("activation_allowed=False; ELIGIBLE models still need `ml-loop-approve` by a named human. Research only; not investment advice.")
    text = "\n".join(lines)
    print(text)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text + "\n", encoding="utf-8")


def cmd_ml_loop_approve(args) -> None:
    reg = ModelRegistry(args.registry_dir, _clock)
    rec = reg.approve(args.model_id, args.approver, args.note)
    print(f"{rec.model_id}: {rec.status} by {rec.approved_by}; activation_allowed={rec.activation_allowed}")


def setup_ml_loop_cli(subparsers) -> None:
    p = subparsers.add_parser("ml-loop-train", help="Offline purged-CV training, registry and promotion gate")
    p.add_argument("--model-id", required=True)
    p.add_argument("--source", choices=["synthetic", "csv"], default="synthetic")
    p.add_argument("--csv-dir", default=None)
    p.add_argument("--memberships", default=None)
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--ridge-alpha", type=float, default=10.0)
    p.add_argument("--registry-dir", default="data/model_registry")
    p.set_defaults(func=cmd_ml_loop_train)
    c = subparsers.add_parser("ml-loop-cpcv", help="Tree models / meta-labeling on CPCV paths with DSR+SPA gate (research only)")
    c.add_argument("--model", choices=["hgb", "rf"], default="hgb")
    c.add_argument("--meta", action="store_true", help="meta-labeling over the factor-mix primary signal")
    c.add_argument("--model-id", default=None)
    c.add_argument("--source", choices=["synthetic", "csv"], default="synthetic")
    c.add_argument("--csv-dir", default=None)
    c.add_argument("--memberships", default=None)
    c.add_argument("--seed", type=int, default=7)
    c.add_argument("--trials", type=int, default=1, help="trial count for DSR when no --hypothesis-log is given")
    c.add_argument("--hypothesis-log", default=None)
    c.add_argument("--commission-bps", type=float, default=1.0)
    c.add_argument("--slippage-bps", type=float, default=5.0)
    c.add_argument("--cash-rate", type=float, default=0.02)
    c.add_argument("--cash-rate-csv", default=None)
    c.add_argument("--registry-dir", default="data/model_registry")
    c.add_argument("--out", default=None)
    c.set_defaults(func=cmd_ml_loop_cpcv)
    q = subparsers.add_parser("ml-loop-approve", help="Human approval of an ELIGIBLE model (research use only)")
    q.add_argument("--model-id", required=True)
    q.add_argument("--approver", required=True)
    q.add_argument("--note", required=True)
    q.add_argument("--registry-dir", default="data/model_registry")
    q.set_defaults(func=cmd_ml_loop_approve)
