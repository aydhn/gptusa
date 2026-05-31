import pytest
import tempfile
from pathlib import Path
from usa_signal_bot.ml_research.foundation.ml_foundation_store import (
    write_ml_foundation_context_json, ml_foundation_contexts_dir
)
from usa_signal_bot.ml_research.foundation.ml_foundation_report import build_ml_foundation_context

def test_ml_foundation_store_write_context():
    with tempfile.TemporaryDirectory() as td:
        data_root = Path(td)
        ctx = build_ml_foundation_context()
        p = ml_foundation_contexts_dir(data_root) / f"{ctx.context_id}.json"
        res = write_ml_foundation_context_json(p, ctx)
        assert res.exists()
