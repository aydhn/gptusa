import json
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional
from datetime import datetime, timezone

from usa_signal_bot.regression.regression_models import (
    GoldenDatasetSpec,
    GoldenDatasetStatus,
    golden_dataset_spec_to_dict,
    create_golden_dataset_id
)
from usa_signal_bot.regression.golden_fixtures import write_golden_fixture_files
from usa_signal_bot.core.exceptions import GoldenDatasetError

class GoldenDatasetManager:
    def __init__(self, data_root: Path):
        self.data_root = Path(data_root)
        self.golden_dir = self.data_root / "regression" / "golden"
        self.golden_dir.mkdir(parents=True, exist_ok=True)

    def default_spec(self) -> GoldenDatasetSpec:
        return GoldenDatasetSpec(
            dataset_id=create_golden_dataset_id(),
            name="golden_small_us",
            symbols=["SPY", "QQQ", "AAPL"],
            timeframe="1d",
            start_date="2024-01-02",
            end_date="2024-03-29",
            row_count_per_symbol=60,
            status=GoldenDatasetStatus.CREATED,
            created_at_utc=datetime.now(timezone.utc).isoformat()
        )

    def dataset_dir(self, dataset_name: str) -> Path:
        return self.golden_dir / dataset_name

    def latest_dataset_dir(self) -> Optional[Path]:
        dirs = [d for d in self.golden_dir.iterdir() if d.is_dir()]
        if not dirs:
            return None
        dirs.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        return dirs[0]

    def create_dataset(self, spec: Optional[GoldenDatasetSpec] = None, overwrite: bool = False) -> Dict[str, str]:
        if spec is None:
            spec = self.default_spec()

        ds_dir = self.dataset_dir(spec.name)

        if ds_dir.exists() and not overwrite:
            manifest = self.load_dataset_manifest(spec.name)
            if manifest:
                spec.status = GoldenDatasetStatus.VALID
                return {"manifest": str(ds_dir / "manifest.json")}

        paths = write_golden_fixture_files(ds_dir, spec)
        spec.status = GoldenDatasetStatus.VALID
        manifest_path = self.write_dataset_manifest(spec, paths)
        paths["manifest"] = str(manifest_path)
        return paths

    def validate_dataset(self, spec: Optional[GoldenDatasetSpec] = None) -> Tuple[bool, List[str], List[str]]:
        if spec is None:
            spec = self.default_spec()

        ds_dir = self.dataset_dir(spec.name)
        warnings = []
        errors = []

        if not ds_dir.exists():
            errors.append(f"Dataset directory missing: {ds_dir}")
            return False, warnings, errors

        manifest = self.load_dataset_manifest(spec.name)
        if not manifest:
            errors.append(f"Manifest missing or invalid for dataset: {spec.name}")
            return False, warnings, errors

        for sym in spec.symbols:
            p = ds_dir / f"ohlcv_{sym}_{spec.timeframe}.jsonl"
            if not p.exists():
                errors.append(f"Missing OHLCV file for symbol {sym}")

        for core_file in ["signals.jsonl", "candidates.jsonl", "risk_decisions.jsonl", "allocations.jsonl"]:
            if not (ds_dir / core_file).exists():
                 errors.append(f"Missing core file {core_file}")

        return len(errors) == 0, warnings, errors

    def load_dataset_manifest(self, dataset_name: str) -> Optional[Dict[str, Any]]:
        ds_dir = self.dataset_dir(dataset_name)
        man_path = ds_dir / "manifest.json"
        if not man_path.exists():
            return None
        try:
            with open(man_path, "r") as f:
                return json.load(f)
        except Exception:
            return None

    def write_dataset_manifest(self, spec: GoldenDatasetSpec, paths: Dict[str, str]) -> Path:
        ds_dir = self.dataset_dir(spec.name)
        man_path = ds_dir / "manifest.json"

        payload = {
            "spec": golden_dataset_spec_to_dict(spec),
            "paths": paths
        }
        with open(man_path, "w") as f:
             json.dump(payload, f, indent=2)

        return man_path

    def install_dataset_into_local_cache(self, dataset_name: str, target_data_root: Optional[Path] = None) -> Dict[str, str]:
        source_dir = self.dataset_dir(dataset_name)
        if not source_dir.exists():
            raise GoldenDatasetError(f"Cannot install missing dataset: {dataset_name}")

        target = target_data_root or self.data_root

        installed_paths = {}
        for f in source_dir.glob("*.jsonl"):
             installed_paths[f.name] = str(f)

        return installed_paths
