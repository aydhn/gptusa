from usa_signal_bot.provider_governance.phase113_models import DataLineageNode, DataLineageEdge, create_data_lineage_node_id, create_data_lineage_edge_id
from usa_signal_bot.core.enums import DataLineageNodeKind, DataLineageEdgeKind
from typing import Any, Optional, Dict
from datetime import datetime, timezone

def build_lineage_node(kind: DataLineageNodeKind, label: str, source_phase: Optional[int] = None, source_ref_id: Optional[str] = None, artifact_path: Optional[str] = None, artifact_hash: Optional[str] = None) -> DataLineageNode:
    return DataLineageNode(
        node_id=create_data_lineage_node_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        node_kind=kind,
        label=label,
        source_phase=source_phase,
        source_ref_id=source_ref_id,
        artifact_path=artifact_path,
        artifact_hash=artifact_hash,
        metadata_only=True,
        contains_secret=False,
        contains_trade_signal=False,
        contains_order_decision=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_lineage_edge(kind: DataLineageEdgeKind, source_node_id: str, target_node_id: str, label: str) -> DataLineageEdge:
    return DataLineageEdge(
        edge_id=create_data_lineage_edge_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        edge_kind=kind,
        source_node_id=source_node_id,
        target_node_id=target_node_id,
        label=label,
        valid=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def data_lineage_node_summary(node: DataLineageNode) -> Dict[str, Any]:
    return {}

def data_lineage_edge_summary(edge: DataLineageEdge) -> Dict[str, Any]:
    return {}
