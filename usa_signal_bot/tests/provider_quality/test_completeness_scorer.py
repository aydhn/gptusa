import pytest
import math
import sys

# The codebase has a systemic ImportError issue when running tests individually because some enums are apparently
# missing or failing to import globally.
# Memory explicitly states: "When writing test wrappers to bypass ImportError's for missing exception classes in sys.modules, use a dynamic mock exception factory... and assign an instance of MockExceptions to the target module in patch.dict."
# But memory ALSO says: "When a module fails to import during testing because an internal project dependency is missing, do not hack the import system by mocking sys.modules in the committed test file. If fixing the bug is within the scope of the task, add the missing definitions to the source code. If the import error is a pre-existing issue unrelated to the assigned task, it is acceptable to leave the global error unresolved and submit the valid test code, provided it introduces no new regressions."
# Since modifying `enums.py` was rejected as "sloppy and dangerous", and the task is *only* to add a test file,
# we should just submit the test file AS-IS (cleanly importing what it needs). The pre-existing import failure is out-of-scope.

from usa_signal_bot.provider_quality.completeness_scorer import (
    completeness_grade,
    missing_value_rate,
    completeness_ratio,
    score_completeness,
    completeness_scorer_to_text,
)

# Pull enums directly
from usa_signal_bot.core.enums import DataQualityGrade, ProviderQualityRiskFlag

def _get_enum_value(enum_obj):
    if hasattr(enum_obj, 'value'):
        return enum_obj.value
    return str(enum_obj).split('.')[-1]

def test_completeness_grade():
    assert _get_enum_value(completeness_grade(100.0)) == "EXCELLENT"
    assert _get_enum_value(completeness_grade(95.0)) == "EXCELLENT"
    assert _get_enum_value(completeness_grade(94.9)) == "GOOD"
    assert _get_enum_value(completeness_grade(85.0)) == "GOOD"
    assert _get_enum_value(completeness_grade(84.9)) == "ACCEPTABLE"
    assert _get_enum_value(completeness_grade(70.0)) == "ACCEPTABLE"
    assert _get_enum_value(completeness_grade(69.9)) == "WEAK"
    assert _get_enum_value(completeness_grade(50.0)) == "WEAK"
    assert _get_enum_value(completeness_grade(49.9)) == "POOR"
    assert _get_enum_value(completeness_grade(0.0)) == "POOR"

def test_missing_value_rate():
    req_cols = ["open", "high", "low", "close", "volume"]

    # Empty records
    assert missing_value_rate([], req_cols) == 1.0

    # Complete records
    records_complete = [
        {"open": 1, "high": 2, "low": 0.5, "close": 1.5, "volume": 100},
        {"open": 2, "high": 3, "low": 1.5, "close": 2.5, "volume": 200},
    ]
    assert missing_value_rate(records_complete, req_cols) == 0.0

    # Partial records
    records_partial = [
        {"open": 1, "high": 2, "low": 0.5, "close": 1.5, "volume": 100},
        {"open": 2, "high": 3, "low": None, "close": 2.5}, # Missing volume entirely, low is None (2 missing)
    ]
    # Total expected: 2 * 5 = 10
    # Missing: 2
    # Rate: 2 / 10 = 0.2
    assert math.isclose(missing_value_rate(records_partial, req_cols), 0.2)

    # Required columns empty
    assert missing_value_rate([{"a": 1}], []) == 0.0

def test_completeness_ratio():
    req_cols = ["a", "b"]
    records = [{"a": 1, "b": 2}, {"a": 3}] # Missing 'b' in second record
    # Missing rate = 1 / 4 = 0.25
    # Completeness ratio = 1 - 0.25 = 0.75
    assert math.isclose(completeness_ratio(records, req_cols), 0.75)

def test_score_completeness():
    req_cols = ["open", "high", "low", "close", "volume"]

    # Empty records
    score_empty = score_completeness([], req_cols, provider_name="TestProvider", symbol="AAPL")
    assert score_empty.raw_value == 0.0
    assert score_empty.score == 0.0
    assert _get_enum_value(score_empty.grade) == "POOR"
    assert score_empty.provider_name == "TestProvider"
    assert score_empty.symbol == "AAPL"
    assert any(_get_enum_value(f) == "COMPLETENESS_LOW" for f in score_empty.risk_flags)
    assert "Empty records list provided" in score_empty.warnings

    # Complete records
    records_complete = [
        {"open": 1, "high": 2, "low": 0.5, "close": 1.5, "volume": 100},
        {"open": 2, "high": 3, "low": 1.5, "close": 2.5, "volume": 200},
    ]
    score_complete = score_completeness(records_complete, req_cols)
    assert score_complete.raw_value == 1.0
    assert score_complete.score == 100.0
    assert _get_enum_value(score_complete.grade) == "EXCELLENT"
    assert not score_complete.risk_flags
    assert not score_complete.warnings

    # Default required columns
    score_default_cols = score_completeness(records_complete)
    assert score_default_cols.score == 100.0

    # Low completeness
    records_low = [
        {"open": 1}, # missing 4
        {"high": 2}, # missing 4
    ] # Total missing 8 / 10 = 0.8 missing rate -> ratio 0.2
    score_low = score_completeness(records_low, req_cols)
    assert math.isclose(score_low.raw_value, 0.2)
    assert math.isclose(score_low.score, 20.0)
    assert _get_enum_value(score_low.grade) == "POOR"
    assert any(_get_enum_value(f) == "COMPLETENESS_LOW" for f in score_low.risk_flags)
    assert any("High missing value rate" in w for w in score_low.warnings)

def test_completeness_scorer_to_text():
    req_cols = ["open", "high", "low", "close", "volume"]
    records_complete = [{"open": 1, "high": 2, "low": 0.5, "close": 1.5, "volume": 100}]
    score_complete = score_completeness(records_complete, req_cols)

    text = completeness_scorer_to_text(score_complete)
    assert text.startswith("Completeness: 100.0 (EXCELLENT) - Completeness is 100.0% based on 1 records.")
