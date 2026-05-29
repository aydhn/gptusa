from usa_signal_bot.regime_classification.alignment.frozen_factor_artifact_loader import build_frozen_factor_alignment_references, load_frozen_factor_table_csv
from pathlib import Path
def test_frozen_factor_artifact_loader():
    df = load_frozen_factor_table_csv(Path("tests/fixtures/regime_alignment/sample_factor_table_aapl.csv"))
    refs = build_frozen_factor_alignment_references(None, {"AAPL": df})
    assert len(refs) == 1
    assert "factor_1" in refs[0].factor_columns
    assert "feature_1" in refs[0].feature_columns
