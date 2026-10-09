import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "usa_signal_bot"


def test_every_source_file_parses():
    bad = []
    for path in ROOT.rglob("*.py"):
        try:
            ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError as exc:
            bad.append(f"{path.relative_to(ROOT)}:{exc.lineno}")
    assert not bad, bad
