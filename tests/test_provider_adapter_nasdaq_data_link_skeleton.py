
from usa_signal_bot.data_providers.adapters.nasdaq_data_link_skeleton import NasdaqDataLinkFreeProviderSkeleton
from usa_signal_bot.core.enums import DataProviderName

def test_nasdaq_skeleton():
    skel = NasdaqDataLinkFreeProviderSkeleton()
    assert skel.provider_name == DataProviderName.NASDAQ_DATA_LINK_FREE
    assert skel.skeleton_only is True
