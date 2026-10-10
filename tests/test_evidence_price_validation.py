import pandas as pd

from usa_signal_bot.evidence.corporate_actions import validate_adjusted_prices


def _px(vals):
    idx = pd.bdate_range("2020-01-01", periods=len(vals))
    return pd.DataFrame({"X": vals}, index=idx), idx


def test_real_large_move_is_not_flagged_by_default():
    px, _ = _px([100.0] * 5 + [147.0] * 5)  # +47% earnings gap, no split on file
    assert validate_adjusted_prices(px) == []
    kinds = {i.kind for i in validate_adjusted_prices(px, include_large_moves=True)}
    assert kinds == {"LARGE_MOVE"}


def test_split_shaped_jump_without_split_row_is_unexplained():
    px, _ = _px([100.0] * 5 + [50.0] * 5)
    kinds = {i.kind for i in validate_adjusted_prices(px)}
    assert kinds == {"UNEXPLAINED_JUMP"}


def test_split_date_slack_catches_shifted_split_row():
    px, idx = _px([100.0] * 5 + [50.0] * 5)
    splits = pd.DataFrame({"symbol": ["X"], "date": [idx[4]], "ratio": [2.0]})  # one day early
    kinds = {i.kind for i in validate_adjusted_prices(px, splits)}
    assert kinds == {"UNADJUSTED_SPLIT"}


def test_adjusted_series_with_split_row_is_clean():
    px, idx = _px([50.0] * 10)
    splits = pd.DataFrame({"symbol": ["X"], "date": [idx[5]], "ratio": [2.0]})
    assert validate_adjusted_prices(px, splits) == []
