import pytest
from unittest.mock import patch, MagicMock
import usa_signal_bot.provider_quality.phase109_models as models

def test_create_provider_cache_ingestion_id_extra():
    id_val = models.create_provider_cache_ingestion_id()
    assert id_val.startswith('cache_ingest_')
    assert len(id_val) == len('cache_ingest_') + 8

def test_create_data_quality_component_id_extra():
    id_val = models.create_data_quality_component_id()
    assert id_val.startswith('dq_comp_')
    assert len(id_val) == len('dq_comp_') + 8
