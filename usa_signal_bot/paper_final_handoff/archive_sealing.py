from typing import Any, Dict
import hashlib
import json
from usa_signal_bot.paper_final_handoff.final_handoff_models import SealedReadinessArchiveManifest
from usa_signal_bot.core.enums import SealedArchiveStatus

def stable_archive_hash(payload: Dict[str, Any]) -> str:
    # Ensure stable sorting for hash
    s = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def archive_seal_payload(manifest: SealedReadinessArchiveManifest) -> Dict[str, Any]:
    d = manifest.__dict__.copy()
    # Remove fields that change during sealing
    d.pop('archive_hash', None)
    d.pop('sealed', None)
    d.pop('immutable', None)
    d.pop('status', None)
    return d

def seal_readiness_archive(manifest: SealedReadinessArchiveManifest) -> SealedReadinessArchiveManifest:
    payload = archive_seal_payload(manifest)
    manifest.archive_hash = stable_archive_hash(payload)
    manifest.sealed = True
    manifest.immutable = True
    manifest.status = SealedArchiveStatus.SEALED
    return manifest

def verify_archive_seal(manifest: SealedReadinessArchiveManifest) -> bool:
    if not manifest.sealed or not manifest.archive_hash:
        return False
    payload = archive_seal_payload(manifest)
    return manifest.archive_hash == stable_archive_hash(payload)

def archive_sealing_summary(manifest: SealedReadinessArchiveManifest) -> Dict[str, Any]:
    return {"sealed": manifest.sealed, "hash": manifest.archive_hash}

def archive_sealing_to_text(manifest: SealedReadinessArchiveManifest) -> str:
    return f"ArchiveSealing: sealed={manifest.sealed}, hash={manifest.archive_hash}"
