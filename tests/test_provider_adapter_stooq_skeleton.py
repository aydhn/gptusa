
from usa_signal_bot.data_providers.adapters.stooq_skeleton import StooqProviderSkeleton
from usa_signal_bot.core.enums import DataProviderName

def test_stooq_skeleton():
    skel = StooqProviderSkeleton()
    assert skel.provider_name == DataProviderName.STOOQ
    assert skel.skeleton_only is True
