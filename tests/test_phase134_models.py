import pytest
from usa_signal_bot.regime_classification.freeze_preparation.phase134_models import (
    create_regime_monitoring_ingestion_id,
    create_monitoring_validation_rule_id
)

def test_id_generation():
    i1 = create_regime_monitoring_ingestion_id()
    i2 = create_monitoring_validation_rule_id()
    assert i1.startswith("ingest_")
    assert i2.startswith("val_rule_")
    assert len(i1) > 7
    assert len(i2) > 9
