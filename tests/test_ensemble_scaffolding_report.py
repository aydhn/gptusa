import pytest
from usa_signal_bot.ml_research.ensemble_scaffolding.ensemble_scaffolding_report import build_ensemble_scaffolding_full_review

def test_build_scaffold():
    rev = build_ensemble_scaffolding_full_review()
    assert rev.report_type == "FULL_PHASE142_REVIEW"
