from usa_signal_bot.portfolio_construction.correlation_proxy import estimate_pairwise_correlation_proxy

def test_correlation_proxy():
    assert estimate_pairwise_correlation_proxy("AAPL", "AAPL").value == "VERY_HIGH"
    assert estimate_pairwise_correlation_proxy("AAPL", "MSFT", {"cluster": "tech"}, {"cluster": "tech"}).value == "HIGH"
