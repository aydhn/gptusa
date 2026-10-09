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
    q = subparsers.add_parser("ml-loop-approve", help="Human approval of an ELIGIBLE model (research use only)")
    q.add_argument("--model-id", required=True)
    q.add_argument("--approver", required=True)
    q.add_argument("--note", required=True)
    q.add_argument("--registry-dir", default="data/model_registry")
    q.set_defaults(func=cmd_ml_loop_approve)
