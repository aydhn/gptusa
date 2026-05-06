import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from usa_signal_bot.core.enums import AlertType
from usa_signal_bot.notifications.alert_models import AlertPolicy

@dataclass
class AlertCooldownRecord:
    policy_id: str
    alert_type: AlertType
    last_triggered_at_utc: str
    cooldown_until_utc: str
    count: int

def alert_cooldown_record_to_dict(record: AlertCooldownRecord) -> dict:
    return {
        "policy_id": record.policy_id,
        "alert_type": record.alert_type.value if hasattr(record.alert_type, "value") else record.alert_type,
        "last_triggered_at_utc": record.last_triggered_at_utc,
        "cooldown_until_utc": record.cooldown_until_utc,
        "count": record.count
    }

class AlertCooldownManager:
    def __init__(self, default_cooldown_seconds: int = 3600):
        self.default_cooldown_seconds = default_cooldown_seconds
        self._records: Dict[str, AlertCooldownRecord] = {}

    def is_in_cooldown(self, policy: AlertPolicy, now_utc: Optional[str] = None) -> Tuple[bool, Optional[AlertCooldownRecord]]:
        if policy.cooldown_seconds <= 0:
            return False, None

        now_dt = datetime.datetime.fromisoformat(now_utc) if now_utc else datetime.datetime.now(datetime.timezone.utc)
        record = self._records.get(policy.policy_id)
        if not record:
            return False, None

        cd_dt = datetime.datetime.fromisoformat(record.cooldown_until_utc)
        if now_dt < cd_dt:
            return True, record

        return False, record

    def remember(self, policy: AlertPolicy, now_utc: Optional[str] = None) -> AlertCooldownRecord:
        now_dt = datetime.datetime.fromisoformat(now_utc) if now_utc else datetime.datetime.now(datetime.timezone.utc)
        cd_seconds = policy.cooldown_seconds if policy.cooldown_seconds is not None else self.default_cooldown_seconds

        cd_dt = now_dt + datetime.timedelta(seconds=cd_seconds)

        record = self._records.get(policy.policy_id)
        if record:
            record.last_triggered_at_utc = now_dt.isoformat()
            record.cooldown_until_utc = cd_dt.isoformat()
            record.count += 1
        else:
            record = AlertCooldownRecord(
                policy_id=policy.policy_id,
                alert_type=policy.alert_type,
                last_triggered_at_utc=now_dt.isoformat(),
                cooldown_until_utc=cd_dt.isoformat(),
                count=1
            )
            self._records[policy.policy_id] = record

        return record

    def clear_expired(self, now_utc: Optional[str] = None) -> int:
        now_dt = datetime.datetime.fromisoformat(now_utc) if now_utc else datetime.datetime.now(datetime.timezone.utc)
        expired_keys = []
        for k, v in self._records.items():
            if datetime.datetime.fromisoformat(v.cooldown_until_utc) <= now_dt:
                expired_keys.append(k)

        for k in expired_keys:
            del self._records[k]

        return len(expired_keys)

    def list_records(self) -> List[AlertCooldownRecord]:
        return list(self._records.values())

    def clear_all(self) -> int:
        count = len(self._records)
        self._records.clear()
        return count
