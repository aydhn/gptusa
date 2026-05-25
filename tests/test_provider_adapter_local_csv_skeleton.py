
from usa_signal_bot.data_providers.adapters.local_csv_skeleton import LocalCsvProviderSkeleton
from usa_signal_bot.core.enums import DataProviderName

def test_local_csv_skeleton():
    skel = LocalCsvProviderSkeleton()
    assert skel.provider_name == DataProviderName.LOCAL_CSV
    assert skel.skeleton_only is True
