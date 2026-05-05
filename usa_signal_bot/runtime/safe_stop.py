import datetime
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from usa_signal_bot.core.exceptions import SafeStopError

@dataclass
class SafeStopState:
    stop_requested: bool
    requested_at_utc: Optional[str] = None
    reason: Optional[str] = None
    requested_by: Optional[str] = None

def safe_stop_state_to_dict(state: SafeStopState) -> dict:
    return {
        "stop_requested": state.stop_requested,
        "requested_at_utc": state.requested_at_utc,
        "reason": state.reason,
        "requested_by": state.requested_by,
    }

def safe_stop_state_from_dict(data: dict) -> SafeStopState:
    return SafeStopState(
        stop_requested=data.get("stop_requested", False),
        requested_at_utc=data.get("requested_at_utc"),
        reason=data.get("reason"),
        requested_by=data.get("requested_by"),
    )

class SafeStopManager:
    def __init__(self, stop_file: Path):
        self.stop_file = stop_file

    def read_state(self) -> SafeStopState:
        if not self.stop_file.exists():
            return SafeStopState(stop_requested=False)
        try:
            with open(self.stop_file, "r") as f:
                data = json.load(f)
            return safe_stop_state_from_dict(data)
        except Exception:
            return SafeStopState(stop_requested=False)

    def is_stop_requested(self) -> bool:
        return self.read_state().stop_requested

    def check_or_raise(self) -> None:
        state = self.read_state()
        if state.stop_requested:
            raise SafeStopError(f"Safe stop requested: {state.reason or 'No reason provided'}")

    def request_stop(self, reason: str, requested_by: Optional[str] = None) -> SafeStopState:
        self.stop_file.parent.mkdir(parents=True, exist_ok=True)
        state = SafeStopState(
            stop_requested=True,
            requested_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            reason=reason,
            requested_by=requested_by
        )

        tmp_file = self.stop_file.with_suffix(".tmp")
        with open(tmp_file, "w") as f:
            json.dump(safe_stop_state_to_dict(state), f)
        tmp_file.replace(self.stop_file)

        return state

    def clear_stop(self) -> SafeStopState:
        if self.stop_file.exists():
            try:
                self.stop_file.unlink()
            except Exception:
                pass
        return SafeStopState(stop_requested=False)
