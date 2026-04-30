import pytest
from usa_signal_bot.universe.catalog import build_universe_catalog, write_universe_catalog, read_universe_catalog

def test_build_write_read_catalog(tmp_path):
    cat = build_universe_catalog(tmp_path)

    assert cat is not None
    assert cat.catalog_id.startswith("cat_")

    path = write_universe_catalog(tmp_path, cat)
    assert path.exists()

    read_cat = read_universe_catalog(tmp_path)
    assert read_cat is not None
    assert read_cat.catalog_id == cat.catalog_id
