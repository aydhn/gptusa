import pytest
from usa_signal_bot.transaction_costs.cost_reporting import transaction_cost_limitations_text

def test_limitations_text():
    text = transaction_cost_limitations_text()
    assert "No real broker orders" in text
    assert "NOT investment advice" in text
