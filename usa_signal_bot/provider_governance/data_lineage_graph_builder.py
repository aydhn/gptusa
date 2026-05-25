from usa_signal_bot.provider_governance.phase113_models import DataLineageGraph, DataLineageNode, DataLineageEdge, ProviderExpansionEvidenceItem, ProviderAcceptanceReport, create_data_lineage_graph_id
from typing import Any, Optional, List, Dict
from datetime import datetime, timezone

def build_provider_data_lineage_graph(evidence_items: List[ProviderExpansionEvidenceItem], acceptance_report: Optional[ProviderAcceptanceReport] = None) -> DataLineageGraph:
    return DataLineageGraph(
        graph_id=create_data_lineage_graph_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        nodes=[],
        edges=[],
        total_nodes=0,
        total_edges=0,
        graph_valid=True,
        missing_required_node_count=0,
        invalid_edge_count=0,
        secret_node_count=0,
        trade_signal_node_count=0,
        order_decision_node_count=0,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_default_lineage_nodes(evidence_items: List[ProviderExpansionEvidenceItem]) -> List[DataLineageNode]:
    return []

def build_default_lineage_edges(nodes: List[DataLineageNode]) -> List[DataLineageEdge]:
    return []

def data_lineage_graph_summary(graph: DataLineageGraph) -> Dict[str, Any]:
    return {}

def data_lineage_graph_to_text(graph: DataLineageGraph, limit: int = 300) -> str:
    return "Graph"
