from usa_signal_bot.research_workflow.workflow_validation import (
    validate_no_live_execution_language_in_workflow,
)


def test_workflow_validation():
    rep = validate_no_live_execution_language_in_workflow("kesin al")
    assert not rep.valid
    rep = validate_no_live_execution_language_in_workflow("safe string")
    assert rep.valid


import pytest
from unittest.mock import patch
from usa_signal_bot.research_workflow.workflow_validation import (
    validate_research_workflow_review_report,
)
from usa_signal_bot.research_workflow.workflow_models import (
    ResearchWorkflowReview,
    ResearchWorkflowReportType,
)
from usa_signal_bot.core.exceptions import ResearchWorkflowValidationError


def test_validate_research_workflow_review_report_success():
    # Setup a valid ResearchWorkflowReview
    review = ResearchWorkflowReview(
        review_id="test",
        created_at_utc="2024",
        report_type=ResearchWorkflowReportType.WEEKLY,
        repair_items=[],
        hypotheses=[],
        experiment_plans=[],
        decision_log_entries=[],
        output_paths={},
        warnings=[],
        errors=[],
    )
    # validate_research_workflow_review requires empty or valid items, here lists are empty so it will pass
    rep = validate_research_workflow_review_report(review)
    assert rep.valid
    assert rep.error_count == 0
    assert rep.issue_count == 0


@patch(
    "usa_signal_bot.research_workflow.workflow_validation.validate_research_workflow_review"
)
def test_validate_research_workflow_review_report_error(mock_validate):
    # Setup to raise ResearchWorkflowValidationError
    mock_validate.side_effect = ResearchWorkflowValidationError("Mock validation error")

    review = ResearchWorkflowReview(
        review_id="test",
        created_at_utc="2024",
        report_type=ResearchWorkflowReportType.WEEKLY,
        repair_items=[],
        hypotheses=[],
        experiment_plans=[],
        decision_log_entries=[],
        output_paths={},
        warnings=[],
        errors=[],
    )
    rep = validate_research_workflow_review_report(review)
    assert not rep.valid
    assert rep.error_count == 2
    assert rep.issue_count == 1
    assert rep.issues[0].severity == "ERROR"
    assert "Mock validation error" in rep.issues[0].message
