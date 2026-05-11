import os
import socket
from datetime import datetime, timezone
from typing import Any, Dict, Optional
import getpass
from usa_signal_bot.core.enums import RunLockScope
from usa_signal_bot.scheduler.scheduler_models import RunIdentity, create_run_id

def default_owner() -> str:
    try:
        return getpass.getuser()
    except Exception:
        return "local_scheduler_user"

def get_hostname_safe() -> str:
    try:
        return socket.gethostname()
    except Exception:
        return "localhost"

def get_process_id_safe() -> Optional[int]:
    try:
        return os.getpid()
    except Exception:
        return None

def create_run_identity(
    scope: RunLockScope,
    owner: Optional[str] = None,
    idempotency_key: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> RunIdentity:
    if not owner:
        owner = default_owner()
    now_utc = datetime.now(timezone.utc).isoformat()
    return RunIdentity(
        run_id=create_run_id(),
        run_type=scope,
        owner=owner,
        hostname=get_hostname_safe(),
        process_id=get_process_id_safe(),
        created_at_utc=now_utc,
        idempotency_key=idempotency_key,
        metadata=metadata or {}
    )

def build_run_metadata(command: Optional[str] = None, extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    metadata = {}
    if command:
        # Redact potentially sensitive command parts
        parts = command.split()
        safe_parts = []
        for p in parts:
            if "key" in p.lower() or "secret" in p.lower() or "token" in p.lower():
                safe_parts.append("[REDACTED]")
            else:
                safe_parts.append(p)
        metadata["command"] = " ".join(safe_parts)
    if extra:
        metadata.update(extra)
    return metadata

def run_identity_summary(identity: RunIdentity) -> Dict[str, Any]:
    return {
        "run_id": identity.run_id,
        "owner": identity.owner,
        "host": identity.hostname,
        "pid": identity.process_id
    }

def run_identity_to_text(identity: RunIdentity) -> str:
    return f"Run: {identity.run_id} | Owner: {identity.owner} | Host: {identity.hostname}:{identity.process_id}"
