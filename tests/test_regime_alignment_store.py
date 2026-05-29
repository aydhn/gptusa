from usa_signal_bot.regime_classification.alignment.regime_alignment_store import write_regime_alignment_context_json, regime_alignment_contexts_dir
from usa_signal_bot.regime_classification.alignment.regime_alignment_report import build_regime_alignment_context
from pathlib import Path
def test_store(tmp_path):
    ctx = build_regime_alignment_context()
    d = regime_alignment_contexts_dir(tmp_path)
    p = d / "test.json"
    write_regime_alignment_context_json(p, ctx)
    assert p.exists()
