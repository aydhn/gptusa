import pytest
from unittest.mock import MagicMock, patch

from usa_signal_bot.portfolio_construction.portfolio_models import SectorClusterRecord
from usa_signal_bot.portfolio_construction.construction_validation import (
    validate_sector_cluster_records_report,
    PortfolioConstructionValidationIssue
)

def test_validate_sector_cluster_records_report_happy_path():
    # Setup
    item1 = MagicMock(spec=SectorClusterRecord)
    item2 = MagicMock(spec=SectorClusterRecord)

    # Execute
    with patch('usa_signal_bot.portfolio_construction.construction_validation.validate_sector_cluster_record') as mock_validate:
        report = validate_sector_cluster_records_report([item1, item2])

    # Verify
    assert mock_validate.call_count == 2
    assert report.valid is True
    assert report.error_count == 0
    assert len(report.issues) == 0

def test_validate_sector_cluster_records_report_error_path():
    # Setup
    item1 = MagicMock(spec=SectorClusterRecord)

    # Execute
    with patch('usa_signal_bot.portfolio_construction.construction_validation.validate_sector_cluster_record') as mock_validate:
        mock_validate.side_effect = ValueError("Invalid cluster data")
        report = validate_sector_cluster_records_report([item1])

    # Verify
    assert mock_validate.call_count == 1
    assert report.valid is False
    assert report.error_count == 1
    assert len(report.issues) == 1

    issue = report.issues[0]
    assert issue.severity == "ERROR"
    assert issue.field == "symbol"
    assert issue.message == "Invalid cluster data"
