from typing import List, Tuple, Dict, Set
from usa_signal_bot.taskqueue.task_models import LocalTask, TaskDependency, create_task_dependency_id
from usa_signal_bot.core.enums import LocalTaskType
from usa_signal_bot.core.exceptions import DependencyPlannerError

def build_task_dependencies(tasks: List[LocalTask]) -> List[TaskDependency]:
    deps, task_map = [], {t.task_type: t.task_id for t in tasks}
    def add_dep(t_type, d_on, reason):
        if t_type in task_map and d_on in task_map: deps.append(TaskDependency(create_task_dependency_id(task_map[t_type], task_map[d_on]), task_map[t_type], task_map[d_on], True, reason))
    add_dep(LocalTaskType.HEALTH_CHECK, LocalTaskType.CONFIG_VALIDATION, "Health check needs valid config")
    add_dep(LocalTaskType.SCAN_RUN, LocalTaskType.HEALTH_CHECK, "Scan runs after health check")
    add_dep(LocalTaskType.PAPER_RUN, LocalTaskType.SCAN_RUN, "Paper run needs latest scan signals")
    add_dep(LocalTaskType.QUALITY_ACCEPTANCE, LocalTaskType.REGRESSION_RUN, "Quality check after regression")
    add_dep(LocalTaskType.RELEASE_REHEARSAL, LocalTaskType.QUALITY_ACCEPTANCE, "Release after quality passes")
    add_dep(LocalTaskType.CLEANUP_DRY_RUN, LocalTaskType.RETENTION_REVIEW, "Cleanup after retention review")
    add_dep(LocalTaskType.NOTIFICATION_DRY_RUN, LocalTaskType.HEALTH_CHECK, "Notification after health check")
    return deps

def validate_task_dependencies(tasks: List[LocalTask], dependencies: List[TaskDependency]) -> Tuple[bool, List[str], List[str]]:
    valid, warnings, errors, task_ids = True, [], [], {t.task_id for t in tasks}
    for dep in dependencies:
        if dep.task_id not in task_ids:
            errors.append(f"Unknown task_id: {dep.task_id}")
            valid = False
        if dep.depends_on_task_id not in task_ids:
            if dep.required:
                errors.append(f"Task {dep.task_id} requires missing dependency: {dep.depends_on_task_id}")
                valid = False
    if detect_dependency_cycles(tasks, dependencies):
        errors.append("Dependency cycles detected")
        valid = False
    return valid, warnings, errors

def detect_dependency_cycles(tasks: List[LocalTask], dependencies: List[TaskDependency]) -> List[List[str]]:
    adj = {t.task_id: [] for t in tasks}
    for d in dependencies:
        if d.task_id in adj and d.depends_on_task_id in adj: adj[d.task_id].append(d.depends_on_task_id)
    visited, rec_stack, cycles = set(), set(), []
    def dfs(node: str, path: List[str]):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)
        for neighbor in adj.get(node, []):
            if neighbor not in visited: dfs(neighbor, path)
            elif neighbor in rec_stack: cycles.append(path[path.index(neighbor):].copy())
        rec_stack.remove(node)
        path.pop()
    for t in tasks:
        if t.task_id not in visited: dfs(t.task_id, [])
    return cycles

def topological_sort_local_tasks(tasks: List[LocalTask], dependencies: List[TaskDependency]) -> List[LocalTask]:
    adj, in_degree = {t.task_id: [] for t in tasks}, {t.task_id: 0 for t in tasks}
    for d in dependencies:
        if d.task_id in adj and d.depends_on_task_id in adj:
            adj[d.depends_on_task_id].append(d.task_id)
            in_degree[d.task_id] += 1
    queue = [t.task_id for t in tasks if in_degree[t.task_id] == 0]
    sorted_ids = []
    while queue:
        queue.sort()
        curr = queue.pop(0)
        sorted_ids.append(curr)
        for neighbor in adj[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0: queue.append(neighbor)
    if len(sorted_ids) != len(tasks): raise DependencyPlannerError("Cycle detected")
    task_map = {t.task_id: t for t in tasks}
    return [task_map[tid] for tid in sorted_ids]
