import pytest
from usa_signal_bot.backtesting.allocation_drift import *

def test_allocation_drift():
    config = default_allocation_drift_config()
    assert config is not None
