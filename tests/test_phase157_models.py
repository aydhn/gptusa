from usa_signal_bot.portfolio.risk_reporting.phase157_models import (
    create_optimizer_prototype_ingestion_id
)

def test_create_optimizer_prototype_ingestion_id():
    id_str = create_optimizer_prototype_ingestion_id()
    assert id_str.startswith("ingest_")
    assert len(id_str) > 7
