from typing import Any, Dict
from unittest.mock import MagicMock, patch

import pytest

from usa_signal_bot.paper_final_handoff.promotion_dossier_adapter import (
    final_handoff_evidence_from_promotion_dossier,
    promotion_dossier_supports_final_handoff,
    attach_final_handoff_hint_to_promotion_dossier,
    promotion_dossier_final_handoff_summary,
    promotion_dossier_adapter_to_text,
)


@patch('usa_signal_bot.paper_final_handoff.promotion_dossier_adapter.FinalHandoffEvidenceRef')
@patch('usa_signal_bot.paper_final_handoff.promotion_dossier_adapter.create_final_handoff_evidence_ref_id')
@patch('usa_signal_bot.paper_final_handoff.promotion_dossier_adapter._ts')
def test_final_handoff_evidence_from_promotion_dossier(mock_ts, mock_create_id, mock_evidence_ref):
    mock_create_id.return_value = 'ref-123'
    mock_ts.return_value = '2023-01-01T00:00:00Z'
    mock_evidence_ref.return_value = 'mock_ref_obj'

    payload = {'dossier_id': 'doss-456'}

    result = final_handoff_evidence_from_promotion_dossier(payload)

    mock_evidence_ref.assert_called_once()

    # Check arguments explicitly since kwargs vs args can cause assert_called_once_with to fail
    _, kwargs = mock_evidence_ref.call_args
    assert kwargs.get('evidence_ref_id') == 'ref-123'
    assert kwargs.get('created_at_utc') == '2023-01-01T00:00:00Z'
    assert kwargs.get('source_type') == 'promotion_dossier'
    assert kwargs.get('source_id') == 'doss-456'
    assert kwargs.get('source_path') is None
    assert kwargs.get('required') is True
    assert kwargs.get('available') is True
    assert kwargs.get('stale') is False
    assert kwargs.get('summary') == {}
    assert kwargs.get('warnings') == []
    assert kwargs.get('errors') == []

    assert result == ['mock_ref_obj']


def test_promotion_dossier_supports_final_handoff():
    payload = {'dossier_id': 'doss-456'}
    result, reasons = promotion_dossier_supports_final_handoff(payload)
    assert result is True
    assert reasons == []


def test_attach_final_handoff_hint_to_promotion_dossier():
    payload = {'dossier_id': 'doss-456', 'other_key': 'val'}
    review_mock = MagicMock()
    review_mock.review_id = 'rev-789'

    result = attach_final_handoff_hint_to_promotion_dossier(payload, review_mock)

    assert result == {
        'dossier_id': 'doss-456',
        'other_key': 'val',
        'final_handoff_hint': 'rev-789'
    }
    assert payload == {'dossier_id': 'doss-456', 'other_key': 'val'}


def test_promotion_dossier_final_handoff_summary():
    payload = {'dossier_id': 'doss-456'}
    result = promotion_dossier_final_handoff_summary(payload)
    assert result == {'dossier': 'doss-456'}


def test_promotion_dossier_adapter_to_text():
    payload = {}
    result = promotion_dossier_adapter_to_text(payload)
    assert result == 'PromotionDossierAdapter'
