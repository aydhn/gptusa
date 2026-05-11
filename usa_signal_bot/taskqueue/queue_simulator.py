from typing import List, Optional, Dict, Any
from usa_signal_bot.taskqueue.task_models import LocalTask, TaskPriorityScore
from usa_signal_bot.core.enums import LocalTaskStatus

class LocalTaskQueueSimulator:
    def __init__(self, tasks: Optional[List[LocalTask]] = None):
        self._tasks: Dict[str, LocalTask] = {}
        if tasks: self.enqueue_many(tasks)

    def enqueue(self, task: LocalTask) -> LocalTask:
        task.status = LocalTaskStatus.QUEUED
        self._tasks[task.task_id] = task
        return task

    def enqueue_many(self, tasks: List[LocalTask]) -> List[LocalTask]:
        for t in tasks: self.enqueue(t)
        return tasks

    def dequeue_next(self, scores: Optional[List[TaskPriorityScore]] = None) -> Optional[LocalTask]:
        task = self.peek_next(scores)
        if task: task.status = LocalTaskStatus.RUNNING
        return task

    def peek_next(self, scores: Optional[List[TaskPriorityScore]] = None) -> Optional[LocalTask]:
        queued = [t for t in self._tasks.values() if t.status == LocalTaskStatus.QUEUED]
        if not queued: return None
        if not scores: return queued[0]
        score_map = {s.task_id: s.score for s in scores}
        queued.sort(key=lambda t: (-score_map.get(t.task_id, 0.0), t.name))
        return queued[0]

    def list_tasks(self, status: Optional[LocalTaskStatus] = None) -> List[LocalTask]:
        return [t for t in self._tasks.values() if t.status == status] if status else list(self._tasks.values())

    def mark_task_status(self, task_id: str, status: LocalTaskStatus) -> Optional[LocalTask]:
        if task_id in self._tasks:
            self._tasks[task_id].status = status
            return self._tasks[task_id]
        return None

    def remove_task(self, task_id: str) -> Optional[LocalTask]:
        return self._tasks.pop(task_id, None)

    def clear_completed(self) -> int:
        to_remove = [tid for tid, t in self._tasks.items() if t.status in (LocalTaskStatus.COMPLETED, LocalTaskStatus.FAILED, LocalTaskStatus.SKIPPED)]
        for tid in to_remove: self._tasks.pop(tid)
        return len(to_remove)

    def queue_summary(self) -> Dict[str, Any]:
        counts = {}
        for t in self._tasks.values(): counts[t.status.value] = counts.get(t.status.value, 0) + 1
        return {"total_tasks": len(self._tasks), "status_counts": counts}
