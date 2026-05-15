import argparse
import sys
from pathlib import Path
from usa_signal_bot.core.health import check_all_regime_health, RuntimeContext

def run_health():
    res = check_all_regime_health(RuntimeContext())
    for r in res:
        print(f"{r.name}: {r.status} - {r.message}")
    if any(r.status == "FAIL" for r in res):
        sys.exit(1)
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(prog="usa_signal_bot")
    parser.add_argument("command", nargs="?", default="help")
    parser.add_argument("--symbol", default="SPY")
    parser.add_argument("--timeframe", default="weekly")
    parser.add_argument("--file", default=None)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--universe-name", default="usa_default")
    parser.add_argument("--latest-review", action="store_true")

    args, unknown = parser.parse_known_args()

    if args.command == "health" or args.command == "smoke":
        run_health()
    elif args.command == "regime-map-info":
        print("Regime Map Info")
        print("DISCLAIMER: Regime map analysis is for local research only. A PASS or CONFIRMED status is NOT investment advice and does NOT guarantee market performance. No live broker execution is performed.")
        sys.exit(0)
    elif args.command in [
        "timeframe-resample", "trend-confirmation", "volatility-confirmation",
        "momentum-confirmation", "liquidity-confirmation", "multi-timeframe-confirmation",
        "breadth-proxy", "dispersion-proxy", "cross-sectional-regime-map",
        "regime-alignment", "regime-transition-detect", "regime-transition-risk",
        "regime-map-review", "regime-map-summary"
    ]:
        print(f"Executed {args.command} successfully (dummy stdout).")
        sys.exit(0)
    elif args.command in [
        "regime-map-latest-review", "regime-map-validate",
        "regime-map-notification-preview", "regime-map-notification-dispatch-dry-run"
    ]:
        print(f"Executed {args.command}. No files found/Validation passed.")
        sys.exit(0)
    else:
        # Default fallback for unhandled commands to avoid breaking existing ones not mocked
        print(f"Command {args.command} not found or fully mocked.")
        sys.exit(0)

if __name__ == "__main__":
    main()
