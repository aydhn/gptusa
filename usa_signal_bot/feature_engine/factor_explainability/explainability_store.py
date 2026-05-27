import json
from pathlib import Path
from typing import Any

from usa_signal_bot.core.exceptions import ExplainabilityStoreError
from usa_signal_bot.feature_engine.factor_explainability.phase123_models import (
    ExplainabilityContext,
    ExplainabilityFullReview,
    FeatureAttributionSpec,
    FeatureAttributionResult,
    FactorContributionProfile,
    FactorInterpretationSummary,
    ResearchReportDocument,
    ReportQaRuleResult,
    explainability_context_to_dict,
    explainability_full_review_to_dict,
    feature_attribution_spec_to_dict,
    feature_attribution_result_to_dict,
    factor_contribution_profile_to_dict,
    factor_interpretation_summary_to_dict,
    research_report_document_to_dict,
    report_qa_rule_result_to_dict
)

def explainability_store_dir(data_root: Path) -> Path:
    p = data_root / "feature_engine" / "factor_explainability"
    p.mkdir(parents=True, exist_ok=True)
    return p

def explainability_contexts_dir(data_root: Path) -> Path:
    p = explainability_store_dir(data_root) / "contexts"
    p.mkdir(parents=True, exist_ok=True)
    return p

def explainability_reviews_dir(data_root: Path) -> Path:
    p = explainability_store_dir(data_root) / "reviews"
    p.mkdir(parents=True, exist_ok=True)
    return p

def attribution_specs_dir(data_root: Path) -> Path:
    p = explainability_store_dir(data_root) / "attribution_specs"
    p.mkdir(parents=True, exist_ok=True)
    return p

def attribution_results_dir(data_root: Path) -> Path:
    p = explainability_store_dir(data_root) / "attribution_results"
    p.mkdir(parents=True, exist_ok=True)
    return p

def contribution_profiles_dir(data_root: Path) -> Path:
    p = explainability_store_dir(data_root) / "contribution_profiles"
    p.mkdir(parents=True, exist_ok=True)
    return p

def interpretation_summaries_dir(data_root: Path) -> Path:
    p = explainability_store_dir(data_root) / "interpretations"
    p.mkdir(parents=True, exist_ok=True)
    return p

def research_reports_dir(data_root: Path) -> Path:
    p = explainability_store_dir(data_root) / "research_reports"
    p.mkdir(parents=True, exist_ok=True)
    return p

def report_qa_dir(data_root: Path) -> Path:
    p = explainability_store_dir(data_root) / "report_qa"
    p.mkdir(parents=True, exist_ok=True)
    return p

def _write_json(path: Path, payload: dict) -> Path:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)
    return path

def _write_jsonl(path: Path, items: list[dict]) -> Path:
    with open(path, 'w', encoding='utf-8') as f:
        for it in items:
            f.write(json.dumps(it) + "\n")
    return path

def write_explainability_context_json(path: Path, item: ExplainabilityContext) -> Path:
    return _write_json(path, explainability_context_to_dict(item))

def write_explainability_full_review_json(path: Path, item: ExplainabilityFullReview) -> Path:
    return _write_json(path, explainability_full_review_to_dict(item))

def write_attribution_specs_jsonl(path: Path, items: list[FeatureAttributionSpec]) -> Path:
    return _write_jsonl(path, [feature_attribution_spec_to_dict(x) for x in items])

def write_attribution_results_jsonl(path: Path, items: list[FeatureAttributionResult]) -> Path:
    return _write_jsonl(path, [feature_attribution_result_to_dict(x) for x in items])

def write_contribution_profiles_jsonl(path: Path, items: list[FactorContributionProfile]) -> Path:
    return _write_jsonl(path, [factor_contribution_profile_to_dict(x) for x in items])

def write_interpretation_summaries_jsonl(path: Path, items: list[FactorInterpretationSummary]) -> Path:
    return _write_jsonl(path, [factor_interpretation_summary_to_dict(x) for x in items])

def write_research_report_document_json(path: Path, item: ResearchReportDocument) -> Path:
    return _write_json(path, research_report_document_to_dict(item))

def write_report_qa_results_jsonl(path: Path, items: list[ReportQaRuleResult]) -> Path:
    return _write_jsonl(path, [report_qa_rule_result_to_dict(x) for x in items])

def read_explainability_full_review_json(path: Path) -> dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def list_explainability_reviews(data_root: Path) -> list[Path]:
    d = explainability_reviews_dir(data_root)
    return list(d.glob("*.json"))

def get_latest_explainability_review(data_root: Path) -> Path | None:
    files = list_explainability_reviews(data_root)
    if not files:
        return None
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0]

def explainability_store_summary(data_root: Path) -> dict[str, Any]:
    return {"reviews_count": len(list_explainability_reviews(data_root))}
