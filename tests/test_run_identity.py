from usa_signal_bot.scheduler.run_identity import (
    create_run_identity, default_owner, get_hostname_safe,
    get_process_id_safe, build_run_metadata, run_identity_to_text
)
from usa_signal_bot.core.enums import RunLockScope

def test_create_run_identity():
    identity = create_run_identity(RunLockScope.SCAN, owner="test_owner")
    assert identity.run_type == RunLockScope.SCAN
    assert identity.owner == "test_owner"
    assert identity.hostname is not None
    assert identity.process_id is not None
    assert identity.created_at_utc is not None

def test_default_owner():
    owner = default_owner()
    assert isinstance(owner, str)
    assert len(owner) > 0

def test_build_run_metadata_redaction():
    cmd = "python script.py --token secret_xyz123 --key my_key"
    metadata = build_run_metadata(command=cmd)
    assert "secret_xyz123" not in metadata["command"]
    assert "my_key" not in metadata["command"]
    assert "[REDACTED]" in metadata["command"]

def test_run_identity_to_text():
    identity = create_run_identity(RunLockScope.SCAN, owner="test_owner")
    text = run_identity_to_text(identity)
    assert "Run:" in text
    assert "Owner: test_owner" in text
