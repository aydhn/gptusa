import pandas as pd
from usa_signal_bot.portfolio.foundation.portfolio_input_resolver import (
    build_portfolio_input_references, validate_candidate_universe_input_frame
)

def test_portfolio_input_resolver():
    df = pd.DataFrame({"symbol": ["AAPL"], "research_note": ["ok"]})
    refs = build_portfolio_input_references({}, {"candidates": df})
    assert len(refs) == 1
    assert refs[0].available is True
    assert len(refs[0].errors) == 0

def test_forbidden_columns():
    df = pd.DataFrame({"symbol": ["AAPL"], "target_weight": [0.5]})
    errors = validate_candidate_universe_input_frame(df)
    assert len(errors) > 0
    assert "Forbidden columns detected" in str(errors[0])
