import pytest
from usa_signal_bot.core.enums import ComparisonSourceType, MatchStatus
from usa_signal_bot.comparison.comparison_models import ComparisonSourceSummary, MatchedTradePair
from usa_signal_bot.comparison.comparison_reporting import (
    comparison_source_summary_to_text, matched_trade_pair_to_text, comparison_limitations_text
)

def test_source_summary_text():
    s = ComparisonSourceSummary(ComparisonSourceType.PAPER_RUN, "p1", "path", 10, ["AAPL"], ["1d"], [], [])
    txt = comparison_source_summary_to_text(s)
    assert "PAPER_RUN" in txt
    assert "10 records" in txt

def test_matched_trade_text():
    p = MatchedTradePair("m1", "AAPL", "1d", None, None, None, MatchStatus.MATCHED, None, None, None, None, None, None, None, None, None, None, None, None, None, None, [], [])
    txt = matched_trade_pair_to_text(p)
    assert "AAPL" in txt
    assert "MATCHED" in txt

def test_limitations_text():
    txt = comparison_limitations_text()
    assert "NOT investment advice" in txt
    assert "No live orders" in txt
