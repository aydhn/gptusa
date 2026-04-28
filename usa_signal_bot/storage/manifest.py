"""Metadata manifest system for storage layer."""

from dataclasses import dataclass, field
from typing import Any, List, Optional, Union
from datetime import datetime, timezone
from pathlib import Path
import uuid

from usa_signal_bot.storage.formats import StorageFormat
from usa_signal_bot.storage.json_store import write_model_json, read_json_dict
from usa_signal_bot.core.serialization import serialize_value

@dataclass
class ManifestRecord:
    """A record representing a single artifact in the storage system."""
    record_id: str
    artifact_type: str
    path: str
    storage_format: StorageFormat
    created_at_utc: str
    source: str
    row_count: Optional[int] = None
    checksum_sha256: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class Manifest:
    """A collection of manifest records."""
    manifest_id: str
    name: str
    created_at_utc: str
    records: List[ManifestRecord] = field(default_factory=list)

def create_manifest(name: str) -> Manifest:
    """Creates a new empty manifest."""
    return Manifest(
        manifest_id=str(uuid.uuid4()),
        name=name,
        created_at_utc=datetime.now(timezone.utc).isoformat()
    )

def add_manifest_record(manifest: Manifest, record: ManifestRecord) -> Manifest:
    """Adds a record to a manifest."""
    manifest.records.append(record)
    return manifest

def write_manifest(path: Path, manifest: Manifest) -> Path:
    """Writes a manifest to disk."""
    return write_model_json(path, manifest, atomic=True)

def read_manifest(path: Path) -> Union[Manifest, dict]:
    """Reads a manifest from disk."""
    # Since we don't have full deserialization yet, returning the dict is acceptable for now.
    # The instructions say "Manifest veya dict".
    return read_json_dict(path)

def manifest_to_dict(manifest: Manifest) -> dict:
    """Converts a manifest to a dictionary."""
    return serialize_value(manifest)
