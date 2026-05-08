from pathlib import Path
from usa_signal_bot.core.enums import BackupScope
from usa_signal_bot.release.backup_restore import create_backup_request, build_backup, validate_backup, restore_dry_run

def test_backup_restore_flow(tmp_path):
    req = create_backup_request(BackupScope.CONFIG_ONLY, str(tmp_path / "out"))

    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    (cfg_dir / "test.yaml").write_text("a: 1")

    res = build_backup(tmp_path, tmp_path / "data", req)
    assert res.status.value == "CREATED"
    assert Path(res.backup_path).exists()

    val_res = validate_backup(Path(res.backup_path))
    assert val_res.status.value == "VALIDATED"

    rst_res = restore_dry_run(Path(res.backup_path), tmp_path / "restore")
    assert rst_res.status.value == "RESTORE_DRY_RUN_PASSED"
    assert len(rst_res.conflicts) == 0
