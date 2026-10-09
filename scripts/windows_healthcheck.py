"""Windows pre-flight healthcheck (read-only): interpreter, package import, safety flags. Exit 0 = healthy."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def run_checks() -> List[Tuple[str, bool, str]]:
    out: List[Tuple[str, bool, str]] = []
    out.append(("python>=3.10", sys.version_info >= (3, 10), sys.version.split()[0]))
    try:
        import usa_signal_bot  # noqa: F401

        out.append(("package import", True, "usa_signal_bot"))
    except Exception as exc:  # report, do not hide
        out.append(("package import", False, repr(exc)[:120]))
        return out
    try:
        from typing import get_args

        from usa_signal_bot.core.types import ExecutionMode

        out.append(("ExecutionMode local_paper_only", get_args(ExecutionMode) == ("local_paper_only",), str(get_args(ExecutionMode))))
    except Exception as exc:
        out.append(("ExecutionMode local_paper_only", False, repr(exc)[:120]))
    try:
        from usa_signal_bot.ml_loop.registry import ModelRecord

        flag = ModelRecord("h", "t", {}, {}, "f", True).activation_allowed
        out.append(("registry activation_allowed default False", flag is False, str(flag)))
    except Exception as exc:
        out.append(("registry activation_allowed default False", False, repr(exc)[:120]))
    logs = ROOT / "logs"
    try:
        logs.mkdir(exist_ok=True)
        probe = logs / ".healthcheck"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        out.append(("logs writable", True, str(logs)))
    except OSError as exc:
        out.append(("logs writable", False, repr(exc)[:120]))
    return out


def main() -> int:
    results = run_checks()
    for name, ok, detail in results:
        print(f"[{'OK' if ok else 'FAIL'}] {name}: {detail}")
    return 0 if all(ok for _n, ok, _d in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
