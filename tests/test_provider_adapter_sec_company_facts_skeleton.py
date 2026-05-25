
from usa_signal_bot.data_providers.adapters.sec_company_facts_skeleton import SecCompanyFactsProviderSkeleton
from usa_signal_bot.core.enums import DataProviderName

def test_sec_skeleton():
    skel = SecCompanyFactsProviderSkeleton()
    assert skel.provider_name == DataProviderName.SEC_COMPANY_FACTS
    assert skel.skeleton_only is True
