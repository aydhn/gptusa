import pytest
from usa_signal_bot.release.advanced_acceptance_schema_validator import (
    validate_advanced_acceptance_column_names,
    validate_no_forbidden_advanced_acceptance_columns
)

def test_schema_validator():
    res = validate_advanced_acceptance_column_names(["normal", "target_weight", "other"])
    assert "target_weight" in res

    res2 = validate_no_forbidden_advanced_acceptance_columns(["normal", "target_weight", "other"])
    assert len(res2) == 1
    assert "target_weight" in res2[0]
