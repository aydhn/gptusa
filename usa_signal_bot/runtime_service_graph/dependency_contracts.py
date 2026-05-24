from typing import Any, Dict, List, Optional
from usa_signal_bot.runtime_service_graph.phase103_models import (
    RuntimeServiceNode,
    DependencyContract,
    create_dependency_contract_id
)
from usa_signal_bot.core.enums import DependencyType, DependencyContractStatus, RuntimeServiceGraphRiskFlag

def build_dependency_contract(
    source: RuntimeServiceNode,
    target: RuntimeServiceNode,
    dependency_type: DependencyType = DependencyType.REQUIRED
) -> DependencyContract:

    return DependencyContract(
        contract_id=create_dependency_contract_id(),
        source_service_id=source.service_id,
        target_service_id=target.service_id,
        dependency_type=dependency_type,
        status=DependencyContractStatus.VALID,
        allowed_capabilities=target.capabilities.copy(),
        requires_metadata_only=True,
        requires_read_only=True,
        allows_network=False,
        allows_execution=False,
        allows_broker=False,
        allows_order=False,
        allows_paper_mutation=False,
        allows_telegram_real_send=False,
        allows_scraping=False,
        allows_dashboard=False,
    )

def build_default_dependency_contracts(nodes: List[RuntimeServiceNode]) -> List[DependencyContract]:
    contracts = []
    nodes_by_id = {n.service_id: n for n in nodes}

    for node in nodes:
        for dep_id in node.dependencies:
            if dep_id in nodes_by_id:
                contracts.append(build_dependency_contract(node, nodes_by_id[dep_id]))

        for dep_id in node.optional_dependencies:
             if dep_id in nodes_by_id:
                 contracts.append(build_dependency_contract(node, nodes_by_id[dep_id], DependencyType.OPTIONAL))

    return contracts

def dependency_contract_for_service_pair(source_service_id: str, target_service_id: str, contracts: List[DependencyContract]) -> Optional[DependencyContract]:
    for c in contracts:
        if c.source_service_id == source_service_id and c.target_service_id == target_service_id:
            return c
    return None

def dependency_contract_summary(contracts: List[DependencyContract]) -> Dict[str, Any]:
    return {"total_contracts": len(contracts)}

def dependency_contracts_to_text(contracts: List[DependencyContract], limit: int = 200) -> str:
    return f"Generated {len(contracts)} dependency contracts."
