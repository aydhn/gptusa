from typing import Any, Dict, List
from usa_signal_bot.runtime_service_graph.phase103_models import RuntimeServiceNode

def build_capability_service_mapping(nodes: List[RuntimeServiceNode]) -> Dict[str, List[str]]:
    mapping = {}
    for node in nodes:
        for cap in node.capabilities:
            if cap not in mapping:
                mapping[cap] = []
            if node.service_id not in mapping[cap]:
                mapping[cap].append(node.service_id)
    return mapping

def services_for_capability(capability_name: str, mapping: Dict[str, List[str]]) -> List[str]:
    return mapping.get(capability_name, [])

def validate_capability_service_mapping(mapping: Dict[str, List[str]], nodes: List[RuntimeServiceNode]) -> List[str]:
    errors = []

    blocked_caps = [
        "broker", "order", "scraping", "telegram_real_send", "execution"
    ]

    for cap, services in mapping.items():
        if cap in blocked_caps:
            errors.append(f"Blocked capability '{cap}' mapped to services: {services}")

    return errors

def capability_service_mapping_summary(mapping: Dict[str, List[str]]) -> Dict[str, Any]:
    return {
        "total_capabilities": len(mapping),
        "capabilities": list(mapping.keys())
    }

def capability_service_mapping_to_text(mapping: Dict[str, List[str]]) -> str:
    return f"Mapped {len(mapping)} capabilities."
