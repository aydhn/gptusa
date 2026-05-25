
from usa_signal_bot.data_providers.interfaces.base import BaseDataProvider

def test_interface_base():
    base = BaseDataProvider()
    assert base.skeleton_only is True
