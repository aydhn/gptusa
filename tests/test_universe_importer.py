import pytest
import csv
from pathlib import Path
from usa_signal_bot.universe.importer import (
    import_universe_csv,
    normalize_import_file,
    list_import_files
)
from usa_signal_bot.core.exceptions import UniverseImportError

@pytest.fixture
def test_csv(tmp_path):
    path = tmp_path / "test.csv"
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["symbol", "asset_type", "name"])
        writer.writeheader()
        writer.writerow({"symbol": "AAPL", "asset_type": "stock", "name": "Apple"})
    return path

def test_import_universe_csv(tmp_path, test_csv):
    dest_dir = tmp_path / "imports"
    out_path = import_universe_csv(test_csv, dest_dir, "my_import")

    assert out_path.exists()
    assert out_path.name == "my_import.csv"

    # Read output and check missing optional columns were added
    with open(out_path, "r") as f:
        reader = csv.DictReader(f)
        row = next(reader)
        assert row["symbol"] == "AAPL"
        assert "currency" in row
        assert row["currency"] == "USD" # default

def test_import_url_rejected(tmp_path):
    dest_dir = tmp_path / "imports"
    with pytest.raises(UniverseImportError) as e:
        import_universe_csv(Path("http://example.com/data.csv"), dest_dir, "test")
    assert "URL is not permitted" in str(e.value)

def test_import_path_traversal_rejected(tmp_path, test_csv):
    dest_dir = tmp_path / "imports"
    with pytest.raises(UniverseImportError) as e:
        import_universe_csv(test_csv, dest_dir, "../../sneaky")
    assert "Path traversal detected" in str(e.value)

def test_import_overwrite_protection(tmp_path, test_csv):
    dest_dir = tmp_path / "imports"
    dest_dir.mkdir()
    (dest_dir / "my_import.csv").touch()

    with pytest.raises(UniverseImportError) as e:
        import_universe_csv(test_csv, dest_dir, "my_import", overwrite=False)
    assert "already exists" in str(e.value)

def test_normalize_import_file_missing_required(tmp_path):
    path = tmp_path / "bad.csv"
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["symbol", "price"])
        writer.writeheader()
        writer.writerow({"symbol": "AAPL", "price": "100"})

    with pytest.raises(UniverseImportError) as e:
        normalize_import_file(path, tmp_path / "out.csv")
    assert "Missing required columns" in str(e.value)
