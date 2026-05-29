from typing import Any
import json
from pathlib import Path
from usa_signal_bot.regime_classification.alignment.phase131_models import (
    RegimeAlignmentContext, RegimeAlignmentFullReview, FrozenFactorAlignmentReference,
    RegimeAwareAlignmentSpec, MarketBehaviorOverlayResult, RegimeContextCompatibilityResult,
    AlignmentDiagnosticsProfile, RegimeAlignmentReadinessGate
)
import dataclasses

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        from enum import Enum
        if isinstance(o, Enum):
            return o.value
        return super().default(o)

def regime_alignment_store_dir(data_root: Path) -> Path:
    p = data_root / "regime_classification" / "alignment"
    p.mkdir(parents=True, exist_ok=True)
    return p

def regime_alignment_contexts_dir(data_root: Path) -> Path:
    p = regime_alignment_store_dir(data_root) / "contexts"
    p.mkdir(parents=True, exist_ok=True)
    return p

def regime_alignment_reviews_dir(data_root: Path) -> Path:
    p = regime_alignment_store_dir(data_root) / "reviews"
    p.mkdir(parents=True, exist_ok=True)
    return p

def frozen_factor_refs_dir(data_root: Path) -> Path:
    p = regime_alignment_store_dir(data_root) / "frozen_factor_refs"
    p.mkdir(parents=True, exist_ok=True)
    return p

def alignment_specs_dir(data_root: Path) -> Path:
    p = regime_alignment_store_dir(data_root) / "specs"
    p.mkdir(parents=True, exist_ok=True)
    return p

def overlay_results_dir(data_root: Path) -> Path:
    p = regime_alignment_store_dir(data_root) / "overlays"
    p.mkdir(parents=True, exist_ok=True)
    return p

def compatibility_results_dir(data_root: Path) -> Path:
    p = regime_alignment_store_dir(data_root) / "compatibility"
    p.mkdir(parents=True, exist_ok=True)
    return p

def alignment_diagnostics_dir(data_root: Path) -> Path:
    p = regime_alignment_store_dir(data_root) / "diagnostics"
    p.mkdir(parents=True, exist_ok=True)
    return p

def alignment_gates_dir(data_root: Path) -> Path:
    p = regime_alignment_store_dir(data_root) / "gates"
    p.mkdir(parents=True, exist_ok=True)
    return p

def write_regime_alignment_context_json(path: Path, item: RegimeAlignmentContext) -> Path:
    with open(path, "w") as f:
        json.dump(item, f, cls=EnhancedJSONEncoder, indent=2)
    return path

def write_regime_alignment_full_review_json(path: Path, item: RegimeAlignmentFullReview) -> Path:
    with open(path, "w") as f:
        json.dump(item, f, cls=EnhancedJSONEncoder, indent=2)
    return path

def write_frozen_factor_refs_jsonl(path: Path, items: list[FrozenFactorAlignmentReference]) -> Path:
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(i, cls=EnhancedJSONEncoder) + "\n")
    return path

def write_alignment_specs_jsonl(path: Path, items: list[RegimeAwareAlignmentSpec]) -> Path:
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(i, cls=EnhancedJSONEncoder) + "\n")
    return path

def write_overlay_results_jsonl(path: Path, items: list[MarketBehaviorOverlayResult]) -> Path:
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(i, cls=EnhancedJSONEncoder) + "\n")
    return path

def write_compatibility_results_jsonl(path: Path, items: list[RegimeContextCompatibilityResult]) -> Path:
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(i, cls=EnhancedJSONEncoder) + "\n")
    return path

def write_alignment_diagnostics_jsonl(path: Path, items: list[AlignmentDiagnosticsProfile]) -> Path:
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(i, cls=EnhancedJSONEncoder) + "\n")
    return path

def write_alignment_readiness_gate_json(path: Path, item: RegimeAlignmentReadinessGate) -> Path:
    with open(path, "w") as f:
        json.dump(item, f, cls=EnhancedJSONEncoder, indent=2)
    return path

def read_regime_alignment_full_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_regime_alignment_reviews(data_root: Path) -> list[Path]:
    return sorted(list(regime_alignment_reviews_dir(data_root).glob("*.json")))

def get_latest_regime_alignment_review(data_root: Path) -> Path | None:
    files = list_regime_alignment_reviews(data_root)
    return files[-1] if files else None

def regime_alignment_store_summary(data_root: Path) -> dict[str, Any]:
    return {"reviews_count": len(list_regime_alignment_reviews(data_root))}
