
from usa_signal_bot.data_providers.adapters.fred_skeleton import FredCompatibleProviderSkeleton
from usa_signal_bot.core.enums import DataProviderName

def test_fred_skeleton():
    skel = FredCompatibleProviderSkeleton()
    assert skel.provider_name == DataProviderName.FRED_COMPATIBLE
    assert skel.skeleton_only is True
