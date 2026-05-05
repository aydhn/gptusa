import pytest
from usa_signal_bot.backtesting.allocation_adapter import *

def test_allocation_adapter():
    config = default_allocation_to_order_config()
    assert config is not None
