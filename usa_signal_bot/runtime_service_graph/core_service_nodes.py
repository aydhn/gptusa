from typing import List
from usa_signal_bot.runtime_service_graph.phase103_models import RuntimeServiceNode
from usa_signal_bot.core.enums import RuntimeServiceKind, RuntimeServiceStatus

def build_core_config_node() -> RuntimeServiceNode:
    return RuntimeServiceNode(
        service_id="core.config",
        service_name="core.config",
        kind=RuntimeServiceKind.CORE_CONFIG,
        status=RuntimeServiceStatus.READY_METADATA_ONLY,
        package_path="usa_signal_bot.core",
        capabilities=["config_management"],
        dependencies=[]
    )

def build_core_storage_node() -> RuntimeServiceNode:
    return RuntimeServiceNode(
        service_id="core.storage",
        service_name="core.storage",
        kind=RuntimeServiceKind.CORE_STORAGE,
        status=RuntimeServiceStatus.READY_LOCAL_COMPUTE,
        package_path="usa_signal_bot.core",
        capabilities=["local_storage"],
        dependencies=["core.config"]
    )

def build_core_validation_node() -> RuntimeServiceNode:
    return RuntimeServiceNode(
        service_id="core.validation",
        service_name="core.validation",
        kind=RuntimeServiceKind.CORE_VALIDATION,
        status=RuntimeServiceStatus.READY_LOCAL_COMPUTE,
        package_path="usa_signal_bot.core",
        capabilities=["validation"],
        dependencies=[]
    )

def build_core_health_node() -> RuntimeServiceNode:
    return RuntimeServiceNode(
        service_id="core.health",
        service_name="core.health",
        kind=RuntimeServiceKind.CORE_HEALTH,
        status=RuntimeServiceStatus.READY_LOCAL_COMPUTE,
        package_path="usa_signal_bot.core",
        capabilities=["health_checks"],
        dependencies=["core.validation"]
    )

def build_core_logging_node() -> RuntimeServiceNode:
    return RuntimeServiceNode(
        service_id="core.logging",
        service_name="core.logging",
        kind=RuntimeServiceKind.CORE_LOGGING,
        status=RuntimeServiceStatus.READY_LOCAL_COMPUTE,
        package_path="usa_signal_bot.core",
        capabilities=["logging"],
        dependencies=["core.config"]
    )

def build_core_serialization_node() -> RuntimeServiceNode:
    return RuntimeServiceNode(
        service_id="core.serialization",
        service_name="core.serialization",
        kind=RuntimeServiceKind.CORE_SERIALIZATION,
        status=RuntimeServiceStatus.READY_LOCAL_COMPUTE,
        package_path="usa_signal_bot.core",
        capabilities=["serialization"],
        dependencies=[]
    )

def build_runtime_context_node() -> RuntimeServiceNode:
    return RuntimeServiceNode(
        service_id="core.runtime_context",
        service_name="core.runtime_context",
        kind=RuntimeServiceKind.CORE_RUNTIME_CONTEXT,
        status=RuntimeServiceStatus.READY_METADATA_ONLY,
        package_path="usa_signal_bot.core",
        capabilities=["context_management"],
        dependencies=["core.config"]
    )

def build_cli_node() -> RuntimeServiceNode:
    return RuntimeServiceNode(
        service_id="app.cli",
        service_name="app.cli",
        kind=RuntimeServiceKind.CLI,
        status=RuntimeServiceStatus.READY_LOCAL_COMPUTE,
        package_path="usa_signal_bot.app",
        capabilities=["cli_routing"],
        dependencies=["core.config", "core.health"]
    )

def build_observability_node() -> RuntimeServiceNode:
    return RuntimeServiceNode(
        service_id="observability.metrics",
        service_name="observability.metrics",
        kind=RuntimeServiceKind.OBSERVABILITY,
        status=RuntimeServiceStatus.READY_LOCAL_COMPUTE,
        package_path="usa_signal_bot.observability",
        capabilities=["metrics_collection"],
        dependencies=["core.logging"]
    )

def build_notification_preview_node() -> RuntimeServiceNode:
    return RuntimeServiceNode(
        service_id="notifications.preview",
        service_name="notifications.preview",
        kind=RuntimeServiceKind.NOTIFICATION_PREVIEW,
        status=RuntimeServiceStatus.READY_LOCAL_COMPUTE,
        package_path="usa_signal_bot.notifications",
        capabilities=["notification_preview"],
        dependencies=["core.config"]
    )

def build_core_service_nodes() -> List[RuntimeServiceNode]:
    return [
        build_core_config_node(),
        build_core_storage_node(),
        build_core_validation_node(),
        build_core_health_node(),
        build_core_logging_node(),
        build_core_serialization_node(),
        build_runtime_context_node(),
        build_cli_node(),
        build_observability_node(),
        build_notification_preview_node()
    ]
