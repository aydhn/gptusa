import hashlib
import json
from datetime import datetime, timezone
from typing import Any, List

from usa_signal_bot.ml_research.model_comparison.phase140_models import (
    ModelCardComparisonUpdate,
    ModelRankingTable,
    ModelRankingEntry,
    CandidateShortlist,
    CalibrationReadinessProfile,
    create_model_card_comparison_update_id
)

def update_model_cards_with_comparison_results(model_card_payloads: list[dict[str, Any]], ranking: ModelRankingTable, shortlist: CandidateShortlist, calibration_profiles: list[CalibrationReadinessProfile]) -> list[ModelCardComparisonUpdate]:
    updates = []

    ranking_dict = {e.model_artifact_id: e for e in ranking.entries}
    calib_dict = {p.model_artifact_id: p for p in calibration_profiles}

    for payload in model_card_payloads:
        art_id = payload.get("model_artifact_id")
        entry = ranking_dict.get(art_id)
        prof = calib_dict.get(art_id)
        if entry:
            updates.append(update_model_card_with_ranking(payload, entry, prof))

    return updates

def update_model_card_with_ranking(card_payload: dict[str, Any] | None, ranking_entry: ModelRankingEntry | None, calibration_profile: CalibrationReadinessProfile | None = None) -> ModelCardComparisonUpdate:
    art_id = ranking_entry.model_artifact_id if ranking_entry else None
    exp_id = ranking_entry.experiment_id if ranking_entry else None

    up = ModelCardComparisonUpdate(
        update_id=create_model_card_comparison_update_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        source_model_card_update_id=None,
        model_artifact_id=art_id,
        experiment_id=exp_id,
        ranking_entry_id=ranking_entry.ranking_entry_id if ranking_entry else None,
        updated_sections=["model_comparison_rank", "calibration_preparation"],
        rendered_markdown="## Model Ranking\n\nResearch only rank.",
        rendered_text="Model Ranking: Research only rank.",
        update_hash=None,
        comparison_status_updated=True,
        ranking_status_updated=True,
        calibration_preparation_updated=True,
        non_activation_notice_preserved=True,
        not_investment_advice=True,
        not_trade_signal=True,
        not_deployment_artifact=True,
        research_data_only=True,
        investment_advice=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    up.update_hash = compute_model_card_comparison_update_hash(up)
    return up

def render_model_card_comparison_update_markdown(update: ModelCardComparisonUpdate) -> str:
    return update.rendered_markdown or ""

def render_model_card_comparison_update_text(update: ModelCardComparisonUpdate) -> str:
    return update.rendered_text or ""

def compute_model_card_comparison_update_hash(update: ModelCardComparisonUpdate) -> str:
    data = [update.model_artifact_id, update.ranking_entry_id]
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def validate_model_card_comparison_updates(items: list[ModelCardComparisonUpdate]) -> list[str]:
    return []

def model_card_comparison_update_summary(items: list[ModelCardComparisonUpdate]) -> dict[str, Any]:
    return {"count": len(items)}

def model_card_comparison_update_to_text(items: list[ModelCardComparisonUpdate], limit: int = 300) -> str:
    return str([u.update_id for u in items])[:limit]
