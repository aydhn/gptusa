"""Windows launcher for the research CLI. There is deliberately no background trading loop: gptusa is a
research / local-simulation tool (no broker, no orders, no live connection). This script re-runs the healthcheck,
prints the available research commands and exits 0, so ``start_windows.bat`` completes cleanly.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMMANDS = ("evidence-run", "decision-simulate", "ml-loop-train", "ml-loop-approve")


def main() -> int:
    rc = subprocess.call([sys.executable, str(ROOT / "scripts" / "windows_healthcheck.py")], cwd=ROOT)
    if rc != 0:
        print("[supervisor] healthcheck failed; not starting.")
        return rc
    print("[supervisor] research-only mode (local_paper_only). No orders, no broker, no live connection.")
    print("[supervisor] available commands: " + ", ".join(f"python -m usa_signal_bot {c}" for c in COMMANDS))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
