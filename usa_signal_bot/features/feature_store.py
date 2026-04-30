import json
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional

from usa_signal_bot.features.output_contract import FeatureRow, FeatureOutputMetadata
from usa_signal_bot.core.enums import FeatureStorageFormat
from usa_signal_bot.core.exceptions import FeatureStorageError, StoragePathError
from usa_signal_bot.utils.file_utils import atomic_write_text

def feature_store_dir(data_root: Path) -> Path:
    d = data_root / "features"
    d.mkdir(parents=True, exist_ok=True)
    return d

def build_feature_output_filename(provider_name: str, universe_name: Optional[str], timeframe: str, indicator_group: str, fmt: FeatureStorageFormat = FeatureStorageFormat.JSONL) -> str:
    uni = universe_name or "adhoc"
    ext = fmt.value.lower()
    return f"{provider_name}_{uni}_{timeframe}_{indicator_group}.{ext}"

def build_feature_output_path(data_root: Path, provider_name: str, universe_name: Optional[str], timeframe: str, indicator_group: str, fmt: FeatureStorageFormat = FeatureStorageFormat.JSONL) -> Path:
    d = feature_store_dir(data_root)
    fname = build_feature_output_filename(provider_name, universe_name, timeframe, indicator_group, fmt)

    path = (d / fname).resolve()
    if not str(path).startswith(str(d.resolve())):
        raise StoragePathError("Path traversal attempt in feature output path")

    return path

def write_feature_rows_jsonl(path: Path, rows: List[FeatureRow]) -> Path:
    try:
        lines = []
        for r in rows:
            d = {
                "timestamp_utc": r.timestamp_utc,
                "symbol": r.symbol,
                "timeframe": r.timeframe,
                "features": r.features
            }
            lines.append(json.dumps(d))

        atomic_write_text(path, "\n".join(lines) + "\n")
        return path
    except Exception as e:
        raise FeatureStorageError(f"Failed to write feature JSONL: {e}")

def read_feature_rows_jsonl(path: Path) -> List[dict]:
    if not path.exists():
        raise FeatureStorageError(f"Feature file not found: {path}")
    try:
        rows = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rows.append(json.loads(line))
        return rows
    except Exception as e:
        raise FeatureStorageError(f"Failed to read feature JSONL: {e}")

def write_feature_rows_csv(path: Path, rows: List[FeatureRow]) -> Path:
    if not rows:
        atomic_write_text(path, "")
        return path

    try:
        feature_cols = set()
        for r in rows:
            feature_cols.update(r.features.keys())
        feature_cols = sorted(list(feature_cols))

        fieldnames = ["timestamp_utc", "symbol", "timeframe"] + feature_cols

        import tempfile
        import shutil
        import os

        fd, temp_path = tempfile.mkstemp(dir=path.parent, prefix=".tmp_")
        with os.fdopen(fd, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in rows:
                d = {
                    "timestamp_utc": r.timestamp_utc,
                    "symbol": r.symbol,
                    "timeframe": r.timeframe
                }
                for fc in feature_cols:
                    d[fc] = r.features.get(fc, "")
                writer.writerow(d)

        shutil.move(temp_path, path)
        return path
    except Exception as e:
        if 'temp_path' in locals() and os.path.exists(temp_path):
             os.remove(temp_path)
        raise FeatureStorageError(f"Failed to write feature CSV: {e}")

def write_feature_metadata_json(path: Path, metadata: FeatureOutputMetadata) -> Path:
    try:
        import dataclasses
        d = dataclasses.asdict(metadata)
        atomic_write_text(path, json.dumps(d, indent=2))
        return path
    except Exception as e:
        raise FeatureStorageError(f"Failed to write feature metadata: {e}")

def list_feature_outputs(data_root: Path) -> List[Path]:
    d = feature_store_dir(data_root)
    return sorted(list(d.glob("*.jsonl")) + list(d.glob("*.csv")))

def feature_store_summary(data_root: Path) -> Dict[str, Any]:
    d = feature_store_dir(data_root)
    files = list(d.glob("*.*"))

    total_size = sum(f.stat().st_size for f in files if f.is_file())
    jsonl_count = len([f for f in files if f.suffix == ".jsonl"])
    csv_count = len([f for f in files if f.suffix == ".csv"])
    meta_count = len([f for f in files if f.name.endswith("_meta.json")])

    return {
        "total_files": len(files),
        "total_size_bytes": total_size,
        "jsonl_files": jsonl_count,
        "csv_files": csv_count,
        "metadata_files": meta_count
    }
