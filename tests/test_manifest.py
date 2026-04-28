import pytest
from usa_signal_bot.storage.manifest import create_manifest, add_manifest_record, write_manifest, read_manifest, ManifestRecord
from usa_signal_bot.storage.formats import StorageFormat

def test_manifest_lifecycle(tmp_path):
    file_path = tmp_path / "test_manifest.json"

    manifest = create_manifest("test_data")
    assert manifest.name == "test_data"
    assert len(manifest.records) == 0

    record = ManifestRecord(
        record_id="r1",
        artifact_type="features",
        path="features/data.csv",
        storage_format=StorageFormat.CSV,
        created_at_utc="2023-10-27T10:00:00Z",
        source="pipeline_v1",
        checksum_sha256="abcdef123"
    )

    add_manifest_record(manifest, record)
    assert len(manifest.records) == 1

    write_manifest(file_path, manifest)
    assert file_path.exists()

    loaded_dict = read_manifest(file_path)
    assert loaded_dict["name"] == "test_data"
    assert loaded_dict["records"][0]["record_id"] == "r1"
    assert loaded_dict["records"][0]["storage_format"] == "csv"
