
from usa_signal_bot.data_providers.adapters.yfinance_skeleton import YFinanceProviderSkeleton
from usa_signal_bot.core.enums import DataProviderName

def test_yfinance_skeleton():
    skel = YFinanceProviderSkeleton()
    assert skel.provider_name == DataProviderName.YFINANCE
    assert skel.skeleton_only is True
