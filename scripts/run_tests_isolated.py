"""Run every test file in its own pytest subprocess (parallel, per-file timeout) and print a before/after-friendly summary.

A single full ``pytest`` run hangs in tests/test_final_closure_store.py and tests/test_paper_safe_dossier_store.py
(cross-test mock leakage: dataclasses.asdict deep-copies a leaked MagicMock). Per-file isolation avoids it.

Usage: python scripts/run_tests_isolated.py OUT.json [--workers 8] [--timeout 90] [--only FILELIST.json]
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run_one(f: str, timeout: int):
    try:
        r = subprocess.run(
            [sys.executable, "-m", "pytest", f, "-q", "-p", "no:cacheprovider", "--no-header", "-rfE"],
            cwd=ROOT, capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="replace",
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
    except subprocess.TimeoutExpired:
        return f, [0, 0, 0, "TIMEOUT"]
    t = r.stdout

    def g(k: str) -> int:
        m = re.search(r"(\d+) " + k, t)
        return int(m.group(1)) if m else 0

    passed, failed, errors = g("passed"), g("failed"), g("error")
    if r.returncode == 0:
        status = "OK"
    elif passed == 0 and failed == 0:
        status = "COLLECT_ERR"
    else:
        status = "FAIL"
    return f, [passed, failed, errors, status]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--timeout", type=int, default=90)
    ap.add_argument("--only", default=None)
    a = ap.parse_args()
    files = sorted(
        str(p.relative_to(ROOT)).replace("\\", "/")
        for d in ("tests", "usa_signal_bot/tests") for p in (ROOT / d).rglob("test_*.py")
    )
    if a.only:
        keep = set(json.loads(Path(a.only).read_text(encoding="utf-8")))
        files = [f for f in files if f in keep]
    with ThreadPoolExecutor(a.workers) as ex:
        res = dict(ex.map(lambda f: run_one(f, a.timeout), files))
    Path(a.out).write_text(json.dumps(res, indent=1), encoding="utf-8")
    c = collections.Counter(v[3] for v in res.values())
    print("files", len(res), dict(c), "passed", sum(v[0] for v in res.values()), "failed", sum(v[1] for v in res.values()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
