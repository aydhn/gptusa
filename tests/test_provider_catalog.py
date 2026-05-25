
from usa_signal_bot.data_providers.provider_catalog import build_free_provider_candidate_catalog, validate_provider_catalog_safety

def test_provider_catalog():
    cat = build_free_provider_candidate_catalog()
    assert len(cat) >= 6
    errs = validate_provider_catalog_safety(cat)
    assert len(errs) == 0
