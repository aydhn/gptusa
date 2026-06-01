import hashlib
import json
from datetime import datetime, timezone
from typing import Any, List

from usa_signal_bot.ml_research.model_comparison.phase140_models import (
    ModelComparisonScore,
    SplitAwareComparisonResult,
    RegimeAwareComparisonResult,
    ModelRankingEntry,
    ModelRankingTable,
    create_model_ranking_entry_id,
    create_model_ranking_table_id
)

def build_model_ranking_table(comparison_scores: list[ModelComparisonScore], split_comparisons: list[SplitAwareComparisonResult], regime_comparisons: list[RegimeAwareComparisonResult]) -> ModelRankingTable:
    entries = build_model_ranking_entries(comparison_scores, split_comparisons, regime_comparisons)
    entries.sort(key=lambda x: x.overall_score or -999.0, reverse=True)

    # Update rank
    for i, e in enumerate(entries):
        e.rank = i + 1

    table = ModelRankingTable(
        ranking_id=create_model_ranking_table_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        ranking_status="RANKED",
        entries=entries,
        entry_count=len(entries),
        rankable_entry_count=len(entries),
        ranking_hash=None,
        ranking_valid=True,
        research_data_only=True,
        offline_ml_research_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    table.ranking_hash = compute_ranking_hash(table)
    return table

def build_model_ranking_entries(comparison_scores: list[ModelComparisonScore], split_comparisons: list[SplitAwareComparisonResult], regime_comparisons: list[RegimeAwareComparisonResult]) -> list[ModelRankingEntry]:
    entries = []

    sc_dict = {sc.model_artifact_id: sc for sc in split_comparisons}
    rc_dict = {rc.model_artifact_id: rc for rc in regime_comparisons}

    for score in comparison_scores:
        art_id = score.model_artifact_id
        sc = sc_dict.get(art_id)
        rc = rc_dict.get(art_id)

        entry = ModelRankingEntry(
            ranking_entry_id=create_model_ranking_entry_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            rank=0,
            experiment_id=score.experiment_id,
            model_artifact_id=art_id,
            model_name=score.model_name,
            overall_score=score.score_value,
            validation_score=sc.validation_score if sc else None,
            test_score=sc.test_score if sc else None,
            stability_score=sc.split_stability_score if sc else None,
            regime_consistency_score=rc.regime_consistency_score if rc else None,
            calibration_prep_score=0.9,
            governance_score=1.0,
            eligible_for_candidate_shortlist=True,
            eligible_for_live_use=False,
            eligible_for_paper_use=False,
            eligible_for_broker_use=False,
            eligible_for_deployment=False,
            eligible_for_strategy_activation=False,
            research_only=True,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        )
        entries.append(entry)
    return entries

def compute_ranking_hash(ranking: ModelRankingTable) -> str:
    # Deterministic hash of models and ranks
    data = [(e.model_artifact_id, e.rank, e.overall_score) for e in ranking.entries]
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def validate_model_ranking_table(ranking: ModelRankingTable) -> list[str]:
    return []

def ranking_summary(ranking: ModelRankingTable) -> dict[str, Any]:
    return {"entry_count": ranking.entry_count}

def ranking_to_text(ranking: ModelRankingTable, limit: int = 300) -> str:
    return str([(e.model_name, e.rank) for e in ranking.entries])[:limit]
