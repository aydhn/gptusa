import pandas as pd
from usa_signal_bot.portfolio.foundation.candidate_universe_contract import (
    build_candidate_universe_contract, validate_candidate_universe_contract
)

def test_candidate_universe_contract():
    df = pd.DataFrame({"symbol": ["AAPL", "MSFT"]})
    contract = build_candidate_universe_contract({}, df)
    assert contract.candidate_count == 2
    assert "AAPL" in contract.symbols
    assert len(validate_candidate_universe_contract(contract)) == 0
