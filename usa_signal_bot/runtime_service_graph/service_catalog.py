from typing import Any, Dict, List, Optional
from usa_signal_bot.runtime_service_graph.phase103_models import RuntimeServiceNode
from usa_signal_bot.runtime_service_graph.core_service_nodes import build_core_service_nodes
from usa_signal_bot.runtime_service_graph.provider_service_nodes import build_provider_service_nodes
from usa_signal_bot.core.enums import RuntimeServiceKind, RuntimeServiceStatus

def default_runtime_service_catalog() -> List[RuntimeServiceNode]:
    nodes = build_core_service_nodes()
    nodes.extend(build_provider_service_nodes())

    # Advanced Runtime
    nodes.append(RuntimeServiceNode(
        service_id="advanced_runtime.registry",
        service_name="advanced_runtime.registry",
        kind=RuntimeServiceKind.ADVANCED_RUNTIME,
        status=RuntimeServiceStatus.READY_METADATA_ONLY,
        package_path="usa_signal_bot.advanced_runtime",
        capabilities=["runtime_registry"],
        dependencies=["core.validation"]
    ))

    # Engines & Data
    nodes.append(RuntimeServiceNode(
        service_id="data.cache",
        service_name="data.cache",
        kind=RuntimeServiceKind.DATA_CACHE,
        status=RuntimeServiceStatus.READY_LOCAL_COMPUTE,
        package_path="usa_signal_bot.data.cache",
        capabilities=["caching"],
        dependencies=[]
    ))

    nodes.append(RuntimeServiceNode(
        service_id="data.quality",
        service_name="data.quality",
        kind=RuntimeServiceKind.DATA_QUALITY,
        status=RuntimeServiceStatus.READY_LOCAL_COMPUTE,
        package_path="usa_signal_bot.quality",
        capabilities=["data_quality"],
        dependencies=["data.cache"]
    ))

    nodes.append(RuntimeServiceNode(
        service_id="indicators.engine",
        service_name="indicators.engine",
        kind=RuntimeServiceKind.INDICATOR_ENGINE,
        status=RuntimeServiceStatus.READY_LOCAL_COMPUTE,
        package_path="usa_signal_bot.indicators",
        capabilities=["indicators"],
        dependencies=["data.cache"]
    ))

    nodes.append(RuntimeServiceNode(
        service_id="features.engine",
        service_name="features.engine",
        kind=RuntimeServiceKind.FEATURE_ENGINE,
        status=RuntimeServiceStatus.READY_LOCAL_COMPUTE,
        package_path="usa_signal_bot.features",
        capabilities=["features"],
        dependencies=["indicators.engine"]
    ))

    nodes.append(RuntimeServiceNode(
        service_id="strategies.engine",
        service_name="strategies.engine",
        kind=RuntimeServiceKind.STRATEGY_ENGINE,
        status=RuntimeServiceStatus.READY_LOCAL_COMPUTE,
        package_path="usa_signal_bot.strategies",
        capabilities=["strategies"],
        dependencies=["features.engine"]
    ))

    nodes.append(RuntimeServiceNode(
        service_id="backtest.engine",
        service_name="backtest.engine",
        kind=RuntimeServiceKind.BACKTEST_ENGINE,
        status=RuntimeServiceStatus.READY_LOCAL_COMPUTE,
        package_path="usa_signal_bot.backtest",
        capabilities=["backtesting"],
        dependencies=["strategies.engine"]
    ))

    nodes.append(RuntimeServiceNode(
        service_id="benchmark.engine",
        service_name="benchmark.engine",
        kind=RuntimeServiceKind.BENCHMARK_ENGINE,
        status=RuntimeServiceStatus.READY_LOCAL_COMPUTE,
        package_path="usa_signal_bot.benchmark",
        capabilities=["benchmarking"],
        dependencies=["backtest.engine"]
    ))

    nodes.append(RuntimeServiceNode(
        service_id="risk.engine",
        service_name="risk.engine",
        kind=RuntimeServiceKind.RISK_ENGINE,
        status=RuntimeServiceStatus.READY_LOCAL_COMPUTE,
        package_path="usa_signal_bot.risk",
        capabilities=["risk_management"],
        dependencies=["backtest.engine"]
    ))

    nodes.append(RuntimeServiceNode(
        service_id="paper.analytics",
        service_name="paper.analytics",
        kind=RuntimeServiceKind.PAPER_ANALYTICS,
        status=RuntimeServiceStatus.READY_READ_ONLY,
        package_path="usa_signal_bot.paper",
        capabilities=["paper_analytics"],
        dependencies=["core.config"]
    ))

    return nodes

def service_catalog_by_name(name: str) -> Optional[RuntimeServiceNode]:
    for node in default_runtime_service_catalog():
        if node.service_name == name:
            return node
    return None

def service_catalog_summary(nodes: List[RuntimeServiceNode]) -> Dict[str, Any]:
    return {"total_nodes": len(nodes)}

def service_catalog_to_text(nodes: List[RuntimeServiceNode], limit: int = 200) -> str:
    return f"Catalog has {len(nodes)} nodes."
