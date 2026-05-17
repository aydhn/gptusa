
from usa_signal_bot.research_workflow.workflow_models import RepairQueueItem, create_repair_queue_item_id
from usa_signal_bot.core.enums import RepairItemType, RepairPriority, RepairStatus
import datetime

def test_repair_queue_item():
    item = RepairQueueItem(
        item_id=create_repair_queue_item_id(), created_at_utc=datetime.datetime.utcnow().isoformat(),
        item_type=RepairItemType.STRATEGY_RULE, priority=RepairPriority.HIGH, status=RepairStatus.NEW,
        target_scope=None, target_name="T1", title="T1", description="D1", source_failure_modes=[],
        evidence_refs=[], diagnostic_severity="HIGH", evidence_quality="HIGH", suggested_safe_action="Review",
        linked_hypothesis_ids=[], warnings=[], errors=[]
    )
    assert item.target_name == "T1"
