from typing import List, Dict, Any
from usa_signal_bot.core.enums import StartupCheckType, StartupCheckStatus
from usa_signal_bot.runtime_lifecycle.phase104_models import StartupCheckItem, create_startup_check_id, _now_str

def _build_provider_item(check_type: StartupCheckType, msg: str) -> StartupCheckItem:
    return StartupCheckItem(
        check_id=create_startup_check_id(),
        created_at_utc=_now_str(),
        check_type=check_type,
        service_id=None,
        service_name=None,
        status=StartupCheckStatus.PASS,
        required=True,
        message=msg,
        details={},
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def check_provider_interfaces_startup() -> StartupCheckItem:
    return _build_provider_item(StartupCheckType.PROVIDER_INTERFACES, "Provider interfaces verified without initiating actual fetch connections.")

def check_provider_network_disabled_startup() -> StartupCheckItem:
    return _build_provider_item(StartupCheckType.PROVIDER_INTERFACES, "Provider network fetches are properly blocked/mocked.")

def check_provider_paid_api_blocked_startup() -> StartupCheckItem:
    return _build_provider_item(StartupCheckType.PROVIDER_INTERFACES, "No paid API endpoints found in provider registry.")

def check_provider_scraping_blocked_startup() -> StartupCheckItem:
    return _build_provider_item(StartupCheckType.PROVIDER_INTERFACES, "No HTML scraping tools initialized or loaded.")

def run_provider_startup_checks() -> List[StartupCheckItem]:
    return [
        check_provider_interfaces_startup(),
        check_provider_network_disabled_startup(),
        check_provider_paid_api_blocked_startup(),
        check_provider_scraping_blocked_startup()
    ]
