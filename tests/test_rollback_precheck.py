from usa_signal_bot.incident.rollback_precheck import check_rollback_source_exists
from usa_signal_bot.incident.rollback_models import RollbackSource
from usa_signal_bot.core.enums import RollbackSourceType, RollbackSafetyStatus

def test_source_exists(tmp_path):
    p = tmp_path / "src.zip"
    src = RollbackSource("1", RollbackSourceType.BACKUP_ARCHIVE, str(p), None, None, True)
    item = check_rollback_source_exists(src)
    assert item.status == RollbackSafetyStatus.BLOCKED
    p.touch()
    item2 = check_rollback_source_exists(src)
    assert item2.status == RollbackSafetyStatus.SAFE
