"""CLI: ``python -m usa_signal_bot evidence-run`` (research only, writes a markdown report)."""

from __future__ import annotations

from pathlib import Path

from usa_signal_bot.evidence.costs import CostModel
from usa_signal_bot.evidence.data import load_csv_market, synthetic_market
from usa_signal_bot.evidence.report import run_evidence


def cmd_evidence_run(args) -> None:
    if args.source == "csv":
        if not args.csv_dir:
            raise SystemExit("--csv-dir is required with --source csv")
        data = load_csv_market(args.csv_dir, args.memberships)
    else:
        data = synthetic_market(seed=args.seed)
    report = run_evidence(data, CostModel(args.commission_bps, args.slippage_bps), seed=args.seed)
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
    p.add_argument("--write", action="store_true")
    p.add_argument("--out", default="data/evidence/evidence_report.md")
    p.set_defaults(func=cmd_evidence_run)
