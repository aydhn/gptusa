from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from usa_signal_bot.taskqueue.task_models import LocalTask
from usa_signal_bot.core.enums import RunWindowStatus, LocalTaskType
import uuid

@dataclass
class RunWindow:
    window_id: str
    name: str
    start_hour_local: int
    end_hour_local: int
    allowed_task_types: List[LocalTaskType]
    max_duration_seconds: float
    status: RunWindowStatus
    metadata: Dict[str, Any] = field(default_factory=dict)

def default_run_windows() -> List[RunWindow]:
    return [RunWindow(f"win_light_{uuid.uuid4().hex[:6]}", "Light Maintenance", 8, 23, [LocalTaskType.HEALTH_CHECK, LocalTaskType.CONFIG_VALIDATION, LocalTaskType.OBSERVABILITY_HEALTH, LocalTaskType.INCIDENT_REVIEW, LocalTaskType.NOTIFICATION_DRY_RUN], 3600.0, RunWindowStatus.OPEN, {}), RunWindow(f"win_heavy_{uuid.uuid4().hex[:6]}", "Heavy Research", 22, 7, [LocalTaskType.BACKTEST_RUN, LocalTaskType.REGRESSION_RUN, LocalTaskType.RELEASE_REHEARSAL, LocalTaskType.SCAN_RUN, LocalTaskType.QUALITY_ACCEPTANCE, LocalTaskType.NOTIFICATION_DRY_RUN], 14400.0, RunWindowStatus.OPEN, {}), RunWindow(f"win_cleanup_{uuid.uuid4().hex[:6]}", "Cleanup Review", 10, 18, [LocalTaskType.RETENTION_REVIEW, LocalTaskType.CLEANUP_DRY_RUN, LocalTaskType.NOTIFICATION_DRY_RUN], 3600.0, RunWindowStatus.OPEN, {})]

def classify_current_run_window(now_local_hour: Optional[int] = None, windows: Optional[List[RunWindow]] = None) -> Optional[RunWindow]:
    now_local_hour = now_local_hour if now_local_hour is not None else datetime.now().hour
    for w in (windows or default_run_windows()):
        if w.start_hour_local < w.end_hour_local and w.start_hour_local <= now_local_hour <= w.end_hour_local: return w
        elif w.start_hour_local > w.end_hour_local and (now_local_hour >= w.start_hour_local or now_local_hour <= w.end_hour_local): return w
    return None

def task_allowed_in_window(task: LocalTask, window: Optional[RunWindow]) -> bool:
    return task.task_type in window.allowed_task_types if window else True

def filter_tasks_by_run_window(tasks: List[LocalTask], window: Optional[RunWindow]) -> Tuple[List[LocalTask], List[LocalTask]]:
    allowed, outside = [], []
    for t in tasks:
        (allowed if task_allowed_in_window(t, window) else outside).append(t)
    return allowed, outside

def run_windows_to_text(windows: List[RunWindow]) -> str:
    lines = ["Run Windows", "=" * 40]
    for w in windows:
        lines.extend([f"[{w.name}] {w.start_hour_local:02d}:00 - {w.end_hour_local:02d}:00", f"Allowed Tasks: {', '.join(t.value for t in w.allowed_task_types)}", "-" * 20])
    return "\n".join(lines)
