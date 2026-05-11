from typing import List
from usa_signal_bot.taskqueue.task_models import LocalTask, create_local_task_id
from usa_signal_bot.core.enums import LocalTaskType, LocalTaskStatus, TaskPriority, RunLockScope
from usa_signal_bot.core.exceptions import TaskCatalogError

def scan_task(dry_run: bool = True) -> LocalTask:
    return LocalTask(task_id=create_local_task_id("scan"), task_type=LocalTaskType.SCAN_RUN, name="Nightly Universe Scan", priority=TaskPriority.HIGH, status=LocalTaskStatus.CREATED, command="python -m usa_signal_bot active-universe-plan --dry-run" if dry_run else "python -m usa_signal_bot active-universe-plan", lock_scope=RunLockScope.SCAN, estimated_duration_seconds=600.0, estimated_cpu_pct=40.0, estimated_gpu_pct=0.0, estimated_ram_mb=1024.0, estimated_disk_mb=50.0, estimated_network_mb=100.0, dry_run=dry_run)

def paper_task(dry_run: bool = True) -> LocalTask:
    return LocalTask(task_id=create_local_task_id("paper"), task_type=LocalTaskType.PAPER_RUN, name="Local Paper Trading Simulation", priority=TaskPriority.NORMAL, status=LocalTaskStatus.CREATED, command="python -m usa_signal_bot basket-simulate --dry-run" if dry_run else "python -m usa_signal_bot basket-simulate", lock_scope=RunLockScope.PAPER, estimated_duration_seconds=300.0, estimated_cpu_pct=25.0, estimated_gpu_pct=0.0, estimated_ram_mb=512.0, estimated_disk_mb=25.0, estimated_network_mb=0.0, dry_run=dry_run)

def backtest_task(dry_run: bool = True) -> LocalTask:
    return LocalTask(task_id=create_local_task_id("backtest"), task_type=LocalTaskType.BACKTEST_RUN, name="Historical Backtest Evaluation", priority=TaskPriority.NORMAL, status=LocalTaskStatus.CREATED, command="python -m usa_signal_bot backtest-run-signals", lock_scope=RunLockScope.BACKTEST, estimated_duration_seconds=1800.0, estimated_cpu_pct=70.0, estimated_gpu_pct=0.0, estimated_ram_mb=2048.0, estimated_disk_mb=200.0, estimated_network_mb=0.0, dry_run=dry_run)

def regression_smoke_task(dry_run: bool = True) -> LocalTask:
    return LocalTask(task_id=create_local_task_id("regression"), task_type=LocalTaskType.REGRESSION_RUN, name="E2E Regression Harness", priority=TaskPriority.HIGH, status=LocalTaskStatus.CREATED, command="python -m usa_signal_bot smoke", lock_scope=RunLockScope.REGRESSION, estimated_duration_seconds=1200.0, estimated_cpu_pct=60.0, estimated_gpu_pct=0.0, estimated_ram_mb=1536.0, estimated_disk_mb=200.0, estimated_network_mb=0.0, dry_run=dry_run)

def release_rehearsal_task(dry_run: bool = True) -> LocalTask:
    return LocalTask(task_id=create_local_task_id("release"), task_type=LocalTaskType.RELEASE_REHEARSAL, name="Release Rehearsal Packaging", priority=TaskPriority.NORMAL, status=LocalTaskStatus.CREATED, command="python -m usa_signal_bot taskqueue-plan --dry-run", lock_scope=RunLockScope.RELEASE, estimated_duration_seconds=300.0, estimated_cpu_pct=30.0, estimated_gpu_pct=0.0, estimated_ram_mb=1024.0, estimated_disk_mb=100.0, estimated_network_mb=0.0, dry_run=dry_run)

def quality_acceptance_task(dry_run: bool = True) -> LocalTask:
    return LocalTask(task_id=create_local_task_id("quality"), task_type=LocalTaskType.QUALITY_ACCEPTANCE, name="System Quality Acceptance", priority=TaskPriority.HIGH, status=LocalTaskStatus.CREATED, command="python -m usa_signal_bot acceptance-evaluate --scope e2e", lock_scope=RunLockScope.QUALITY, estimated_duration_seconds=300.0, estimated_cpu_pct=25.0, estimated_gpu_pct=0.0, estimated_ram_mb=512.0, estimated_disk_mb=25.0, estimated_network_mb=0.0, dry_run=dry_run)

def retention_review_task(dry_run: bool = True) -> LocalTask:
    return LocalTask(task_id=create_local_task_id("retention"), task_type=LocalTaskType.RETENTION_REVIEW, name="Data Retention Review", priority=TaskPriority.NORMAL, status=LocalTaskStatus.CREATED, command="python -m usa_signal_bot retention-info", lock_scope=RunLockScope.RETENTION, estimated_duration_seconds=180.0, estimated_cpu_pct=20.0, estimated_gpu_pct=0.0, estimated_ram_mb=256.0, estimated_disk_mb=50.0, estimated_network_mb=0.0, dry_run=dry_run)

def cleanup_dry_run_task(dry_run: bool = True) -> LocalTask:
    return LocalTask(task_id=create_local_task_id("cleanup"), task_type=LocalTaskType.CLEANUP_DRY_RUN, name="Cleanup Dry Run Evaluation", priority=TaskPriority.LOW, status=LocalTaskStatus.CREATED, command="python -m usa_signal_bot cleanup-dry-run", lock_scope=RunLockScope.RETENTION, estimated_duration_seconds=200.0, estimated_cpu_pct=25.0, estimated_gpu_pct=0.0, estimated_ram_mb=512.0, estimated_disk_mb=100.0, estimated_network_mb=0.0, dry_run=dry_run)

def observability_health_task(dry_run: bool = True) -> LocalTask:
    return LocalTask(task_id=create_local_task_id("observability"), task_type=LocalTaskType.OBSERVABILITY_HEALTH, name="Observability Metrics Snapshot", priority=TaskPriority.NORMAL, status=LocalTaskStatus.CREATED, command="python -m usa_signal_bot observability-info", lock_scope=RunLockScope.OBSERVABILITY, estimated_duration_seconds=120.0, estimated_cpu_pct=15.0, estimated_gpu_pct=0.0, estimated_ram_mb=256.0, estimated_disk_mb=10.0, estimated_network_mb=0.0, dry_run=dry_run)

def incident_review_task(dry_run: bool = True) -> LocalTask:
    return LocalTask(task_id=create_local_task_id("incident"), task_type=LocalTaskType.INCIDENT_REVIEW, name="Incident Report Review", priority=TaskPriority.URGENT, status=LocalTaskStatus.CREATED, command="python -m usa_signal_bot incident-info", lock_scope=RunLockScope.INCIDENT, estimated_duration_seconds=120.0, estimated_cpu_pct=20.0, estimated_gpu_pct=0.0, estimated_ram_mb=256.0, estimated_disk_mb=10.0, estimated_network_mb=0.0, dry_run=dry_run)

def maintenance_check_task(dry_run: bool = True) -> LocalTask:
    return LocalTask(task_id=create_local_task_id("maintenance"), task_type=LocalTaskType.MAINTENANCE_CHECK, name="Local Maintenance Check", priority=TaskPriority.NORMAL, status=LocalTaskStatus.CREATED, command="python -m usa_signal_bot storage-check", lock_scope=RunLockScope.MAINTENANCE, estimated_duration_seconds=180.0, estimated_cpu_pct=20.0, estimated_gpu_pct=0.0, estimated_ram_mb=256.0, estimated_disk_mb=100.0, estimated_network_mb=0.0, dry_run=dry_run)

def notification_dry_run_task(dry_run: bool = True) -> LocalTask:
    return LocalTask(task_id=create_local_task_id("notification"), task_type=LocalTaskType.NOTIFICATION_DRY_RUN, name="Notification Pipeline Dry Run", priority=TaskPriority.NORMAL, status=LocalTaskStatus.CREATED, command="python -m usa_signal_bot taskqueue-notification-preview", lock_scope=RunLockScope.NOTIFICATION, estimated_duration_seconds=60.0, estimated_cpu_pct=10.0, estimated_gpu_pct=0.0, estimated_ram_mb=128.0, estimated_disk_mb=5.0, estimated_network_mb=0.0, dry_run=dry_run)

def config_validation_task(dry_run: bool = True) -> LocalTask:
    return LocalTask(task_id=create_local_task_id("config_validation"), task_type=LocalTaskType.CONFIG_VALIDATION, name="Configuration Guard Validation", priority=TaskPriority.HIGH, status=LocalTaskStatus.CREATED, command="python -m usa_signal_bot validate-config", lock_scope=RunLockScope.GLOBAL, estimated_duration_seconds=30.0, estimated_cpu_pct=10.0, estimated_gpu_pct=0.0, estimated_ram_mb=128.0, estimated_disk_mb=5.0, estimated_network_mb=0.0, dry_run=dry_run)

def health_check_task(dry_run: bool = True) -> LocalTask:
    return LocalTask(task_id=create_local_task_id("health"), task_type=LocalTaskType.HEALTH_CHECK, name="System Health Check", priority=TaskPriority.HIGH, status=LocalTaskStatus.CREATED, command="python -m usa_signal_bot health", lock_scope=RunLockScope.GLOBAL, estimated_duration_seconds=60.0, estimated_cpu_pct=15.0, estimated_gpu_pct=0.0, estimated_ram_mb=256.0, estimated_disk_mb=10.0, estimated_network_mb=0.0, dry_run=dry_run)

def default_local_tasks(dry_run: bool = True) -> List[LocalTask]:
    return [config_validation_task(dry_run), health_check_task(dry_run), scan_task(dry_run), paper_task(dry_run), backtest_task(dry_run), regression_smoke_task(dry_run), quality_acceptance_task(dry_run), observability_health_task(dry_run), retention_review_task(dry_run), cleanup_dry_run_task(dry_run), incident_review_task(dry_run), maintenance_check_task(dry_run), notification_dry_run_task(dry_run)]

def task_for_type(task_type: LocalTaskType, dry_run: bool = True) -> LocalTask:
    mapping = {LocalTaskType.SCAN_RUN: scan_task, LocalTaskType.PAPER_RUN: paper_task, LocalTaskType.BACKTEST_RUN: backtest_task, LocalTaskType.REGRESSION_RUN: regression_smoke_task, LocalTaskType.RELEASE_REHEARSAL: release_rehearsal_task, LocalTaskType.QUALITY_ACCEPTANCE: quality_acceptance_task, LocalTaskType.RETENTION_REVIEW: retention_review_task, LocalTaskType.CLEANUP_DRY_RUN: cleanup_dry_run_task, LocalTaskType.OBSERVABILITY_HEALTH: observability_health_task, LocalTaskType.INCIDENT_REVIEW: incident_review_task, LocalTaskType.MAINTENANCE_CHECK: maintenance_check_task, LocalTaskType.NOTIFICATION_DRY_RUN: notification_dry_run_task, LocalTaskType.CONFIG_VALIDATION: config_validation_task, LocalTaskType.HEALTH_CHECK: health_check_task}
    if task_type in mapping:
        return mapping[task_type](dry_run)
    raise TaskCatalogError(f"No default catalog task for type {task_type}")

def local_tasks_to_text(tasks: List[LocalTask]) -> str:
    lines = ["Local Task Catalog Summary", "=" * 40]
    for t in tasks:
        lines.append(f"- [{t.task_id}] {t.name}")
        lines.append(f"  Type: {t.task_type.value} | Priority: {t.priority.value}")
        lines.append(f"  Command: {t.command}")
        lines.append(f"  Cost: {t.estimated_cpu_pct}% CPU | {t.estimated_ram_mb}MB RAM | {t.estimated_duration_seconds}s\n")
    return "\n".join(lines)
