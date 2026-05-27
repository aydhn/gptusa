import json
import pandas as pd
from pathlib import Path
from typing import Any
import dataclasses
from usa_signal_bot.feature_engine.enriched_features.phase119_models import (
    FeatureEnrichmentContext, FeatureEnrichmentFullReview, FeatureEnrichmentSpec,
    FeatureInteractionSpec, FeatureEnrichmentResult, EnrichedFeatureTableResult,
    FeatureEnrichmentAudit
)

def feature_enrichment_store_dir(data_root: Path) -> Path:
    return data_root / "feature_engine" / "enriched_features"

def feature_enrichment_contexts_dir(data_root: Path) -> Path:
    return feature_enrichment_store_dir(data_root) / "contexts"

def feature_enrichment_reviews_dir(data_root: Path) -> Path:
    return feature_enrichment_store_dir(data_root) / "reviews"

def feature_enrichment_specs_dir(data_root: Path) -> Path:
    return feature_enrichment_store_dir(data_root) / "specs"

def feature_interaction_specs_dir(data_root: Path) -> Path:
    return feature_enrichment_store_dir(data_root) / "interaction_specs"

def enriched_feature_tables_dir(data_root: Path) -> Path:
    return feature_enrichment_store_dir(data_root) / "feature_tables"

def feature_enrichment_results_dir(data_root: Path) -> Path:
    return feature_enrichment_store_dir(data_root) / "results"

def feature_enrichment_audits_dir(data_root: Path) -> Path:
    return feature_enrichment_store_dir(data_root) / "audits"

def write_feature_enrichment_context_json(path: Path, item: FeatureEnrichmentContext) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(dataclasses.asdict(item), f, indent=2)
    return path

def write_feature_enrichment_full_review_json(path: Path, item: FeatureEnrichmentFullReview) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(dataclasses.asdict(item), f, indent=2)
    return path

def write_feature_enrichment_specs_jsonl(path: Path, items: list[FeatureEnrichmentSpec]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(dataclasses.asdict(item)) + "\n")
    return path

def write_feature_interaction_specs_jsonl(path: Path, items: list[FeatureInteractionSpec]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(dataclasses.asdict(item)) + "\n")
    return path

def write_feature_enrichment_results_jsonl(path: Path, items: list[FeatureEnrichmentResult]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(dataclasses.asdict(item)) + "\n")
    return path

def write_enriched_feature_table_result_json(path: Path, item: EnrichedFeatureTableResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(dataclasses.asdict(item), f, indent=2)
    return path

def write_enriched_feature_table_csv(path: Path, df: pd.DataFrame, overwrite: bool = False) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or overwrite:
        df.to_csv(path, index=False)
    return path

def write_feature_enrichment_audits_jsonl(path: Path, items: list[FeatureEnrichmentAudit]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(dataclasses.asdict(item)) + "\n")
    return path

def read_feature_enrichment_full_review_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return json.load(f)

def list_feature_enrichment_reviews(data_root: Path) -> list[Path]:
    d = feature_enrichment_reviews_dir(data_root)
    if not d.exists(): return []
    return list(d.glob("*.json"))

def get_latest_feature_enrichment_review(data_root: Path) -> Path | None:
    files = list_feature_enrichment_reviews(data_root)
    if not files: return None
    return sorted(files)[-1]

def feature_enrichment_store_summary(data_root: Path) -> dict[str, Any]:
    return {"review_count": len(list_feature_enrichment_reviews(data_root))}
