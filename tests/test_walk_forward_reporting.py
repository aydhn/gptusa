from usa_signal_bot.backtesting.walk_forward_reporting import (
    walk_forward_window_to_text, walk_forward_limitations_text
)
from usa_signal_bot.backtesting.walk_forward_models import WalkForwardWindow
from usa_signal_bot.core.enums import WalkForwardMode, WalkForwardWindowStatus

def test_walk_forward_window_to_text():
    w = WalkForwardWindow("w1", 1, WalkForwardMode.ROLLING, "A", "B", "C", "D", "E", "F", WalkForwardWindowStatus.CREATED)
    txt = walk_forward_window_to_text(w)
    assert "w1" in txt
    assert "ROLLING" in txt

def test_limitations_text():
    txt = walk_forward_limitations_text()
    assert "WALK-FORWARD LIMITATIONS" in txt
