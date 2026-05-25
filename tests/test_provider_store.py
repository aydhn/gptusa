
import tempfile
from pathlib import Path
from usa_signal_bot.data_providers.provider_store import write_provider_abstraction_full_review_json, read_provider_abstraction_full_review_json
from usa_signal_bot.data_providers.provider_report import build_provider_abstraction_full_review

def test_provider_store():
    rev = build_provider_abstraction_full_review()
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "rev.json"
        write_provider_abstraction_full_review_json(p, rev)
        loaded = read_provider_abstraction_full_review_json(p)
        assert "review_id" in loaded
