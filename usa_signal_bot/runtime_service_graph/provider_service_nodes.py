from typing import List
from usa_signal_bot.runtime_service_graph.phase103_models import RuntimeServiceNode
from usa_signal_bot.core.enums import RuntimeServiceKind, RuntimeServiceStatus

def build_market_data_provider_node() -> RuntimeServiceNode:
    return RuntimeServiceNode(
        service_id="provider.market_data_interface",
        service_name="provider.market_data_interface",
        kind=RuntimeServiceKind.PROVIDER_INTERFACE,
        status=RuntimeServiceStatus.READY_METADATA_ONLY,
        package_path="usa_signal_bot.provider",
        capabilities=["market_data_fetch"],
        dependencies=["core.config", "data.cache"]
    )

def build_fundamental_provider_node() -> RuntimeServiceNode:
    return RuntimeServiceNode(
        service_id="provider.fundamental_interface",
        service_name="provider.fundamental_interface",
        kind=RuntimeServiceKind.PROVIDER_INTERFACE,
        status=RuntimeServiceStatus.READY_METADATA_ONLY,
        package_path="usa_signal_bot.provider",
        capabilities=["fundamental_data_fetch"],
        dependencies=["core.config", "data.cache"]
    )

def build_macro_provider_node() -> RuntimeServiceNode:
    return RuntimeServiceNode(
        service_id="provider.macro_interface",
        service_name="provider.macro_interface",
        kind=RuntimeServiceKind.PROVIDER_INTERFACE,
        status=RuntimeServiceStatus.READY_METADATA_ONLY,
        package_path="usa_signal_bot.provider",
        capabilities=["macro_data_fetch"],
        dependencies=["core.config", "data.cache"]
    )

def build_calendar_provider_node() -> RuntimeServiceNode:
    return RuntimeServiceNode(
        service_id="provider.calendar_interface",
        service_name="provider.calendar_interface",
        kind=RuntimeServiceKind.PROVIDER_INTERFACE,
        status=RuntimeServiceStatus.READY_METADATA_ONLY,
        package_path="usa_signal_bot.provider",
        capabilities=["calendar_data_fetch"],
        dependencies=["core.config", "data.cache"]
    )

def build_news_metadata_provider_node() -> RuntimeServiceNode:
    return RuntimeServiceNode(
        service_id="provider.news_metadata_interface",
        service_name="provider.news_metadata_interface",
        kind=RuntimeServiceKind.PROVIDER_INTERFACE,
        status=RuntimeServiceStatus.READY_METADATA_ONLY,
        package_path="usa_signal_bot.provider",
        capabilities=["news_metadata_fetch"],
        dependencies=["core.config", "data.cache"]
    )

def build_symbol_universe_provider_node() -> RuntimeServiceNode:
    return RuntimeServiceNode(
        service_id="provider.symbol_universe_interface",
        service_name="provider.symbol_universe_interface",
        kind=RuntimeServiceKind.PROVIDER_INTERFACE,
        status=RuntimeServiceStatus.READY_METADATA_ONLY,
        package_path="usa_signal_bot.provider",
        capabilities=["symbol_universe_fetch"],
        dependencies=["core.config", "data.cache"]
    )

def build_provider_service_nodes() -> List[RuntimeServiceNode]:
    return [
        build_market_data_provider_node(),
        build_fundamental_provider_node(),
        build_macro_provider_node(),
        build_calendar_provider_node(),
        build_news_metadata_provider_node(),
        build_symbol_universe_provider_node()
    ]
