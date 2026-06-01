from usa_signal_bot.ml_research.model_comparison.phase140_models import (
    create_baseline_training_ingestion_id,
    BaselineTrainingIngestionResult,
    create_model_ranking_table_id,
    ModelRankingTable
)

def test_create_baseline_training_ingestion_id():
    id_val = create_baseline_training_ingestion_id()
    assert id_val.startswith("bti_")

def test_model_ranking_table_creation():
    id_val = create_model_ranking_table_id()
    assert id_val.startswith("mrt_")
