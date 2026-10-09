"""CLI: ``python -m usa_signal_bot evidence-run`` (research only, writes a markdown report)."""

from __future__ import annotations

from pathlib import Path

from usa_signal_bot.evidence.costs import CostModel
from usa_signal_bot.evidence.data import load_csv_market, synthetic_market
from usa_signal_bot.evidence.report import run_evidence


def _cash_rate(args):
    if getattr(args, "cash_rate_csv", None):
        from usa_signal_bot.evidence.rates import load_rate_csv

        return load_rate_csv(args.cash_rate_csv)
    return args.cash_rate


def _hlog(args):
    if not getattr(args, "hypothesis_log", None):
        return None
    from usa_signal_bot.evidence.hypothesis_log import HypothesisLog
    from datetime import datetime, timezone

    return HypothesisLog(Path(args.hypothesis_log), clock=lambda: datetime.now(timezone.utc).isoformat())


def cmd_evidence_run(args) -> None:
    if args.source == "csv":
        if not args.csv_dir:
            raise SystemExit("--csv-dir is required with --source csv")
        data = load_csv_market(args.csv_dir, args.memberships)
    else:
        data = synthetic_market(seed=args.seed)
    report = run_evidence(data, CostModel(args.commission_bps, args.slippage_bps), seed=args.seed,
                          families=args.families.split(",") if args.families else None,
                          hypothesis_log=_hlog(args), run_id=f"run-seed{args.seed}",
                          cash_rate=_cash_rate(args), inflation=args.inflation)
    text = report.to_markdown()
    print(text)
    if args.write:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"Written to {out}")


def setup_evidence_cli(subparsers) -> None:
    p = subparsers.add_parser("evidence-run", help="Walk-forward strategy evidence report (research only)")
    p.add_argument("--source", choices=["synthetic", "csv"], default="synthetic")
    p.add_argument("--csv-dir", default=None, help="Directory with <SYMBOL>.csv price files")
    p.add_argument("--memberships", default=None, help="CSV with symbol,start,end (point-in-time universe)")
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--commission-bps", type=float, default=1.0)
    p.add_argument("--slippage-bps", type=float, default=5.0)
    p.add_argument("--families", default=None, help="Comma-separated strategy family names (default: all)")
    p.add_argument("--hypothesis-log", default=None, help="JSONL file recording every evaluated candidate (cumulative trial count for DSR)")
    p.add_argument("--cash-rate", type=float, default=0.02, help="Annual interest on idle cash (ASSUMPTION; default 2%%)")
    p.add_argument("--cash-rate-csv", default=None, help="FRED-style CSV (e.g. DTB3) for a historical cash rate; overrides --cash-rate")
    p.add_argument("--inflation", type=float, default=0.025, help="Annual inflation assumption for real CAGR (default 2.5%%)")
    p.add_argument("--write", action="store_true")
    p.add_argument("--out", default="data/evidence/evidence_report.md")
    p.set_defaults(func=cmd_evidence_run)
