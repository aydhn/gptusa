from pathlib import Path
import tempfile
import pandas as pd
from usa_signal_bot.feature_engine.core_indicators.core_indicator_store import (
    write_core_indicator_full_review_json, read_core_indicator_full_review_json,
    write_feature_table_csv
)
from usa_signal_bot.feature_engine.core_indicators.core_indicator_report import build_core_indicator_full_review

def test_store_and_review():
    rev = build_core_indicator_full_review()
    assert len(rev.indicator_specs) >= 20

    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "rev.json"
        write_core_indicator_full_review_json(p, rev)
        data = read_core_indicator_full_review_json(p)
        assert data["review_id"] == rev.review_id
