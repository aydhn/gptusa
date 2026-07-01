from typing import List, Dict, Any, Optional
from usa_signal_bot.taskqueue.task_models import (
    LocalTask,
    ResourceEstimate,
    WorkloadBudget,
)
from usa_signal_bot.core.enums import ResourcePressure


def classify_resource_pressure(
    task: LocalTask, budget: Optional[WorkloadBudget] = None
) -> ResourcePressure:
    if task.estimated_cpu_pct is None or task.estimated_ram_mb is None:
        return ResourcePressure.UNKNOWN
    if budget:
        if (
            task.estimated_cpu_pct > budget.max_cpu_pct * 0.8
            or task.estimated_ram_mb > budget.max_ram_mb * 0.8
        ):
            return ResourcePressure.CRITICAL
        if (
            task.estimated_cpu_pct > budget.max_cpu_pct * 0.5
            or task.estimated_ram_mb > budget.max_ram_mb * 0.5
        ):
            return ResourcePressure.HIGH
    if task.estimated_cpu_pct > 60.0 or task.estimated_ram_mb > 4096.0:
        return ResourcePressure.HIGH
    if task.estimated_cpu_pct > 30.0 or task.estimated_ram_mb > 1024.0:
        return ResourcePressure.MODERATE
    return ResourcePressure.LOW


def estimate_task_resources(task: LocalTask) -> ResourceEstimate:
    warnings = []
    if task.estimated_cpu_pct is None:
        warnings.append("Missing CPU estimate")
    if task.estimated_ram_mb is None:
        warnings.append("Missing RAM estimate")
    return ResourceEstimate(
        task_id=task.task_id,
        cpu_pct=task.estimated_cpu_pct,
        gpu_pct=task.estimated_gpu_pct,
        ram_mb=task.estimated_ram_mb,
        disk_mb=task.estimated_disk_mb,
        network_mb=task.estimated_network_mb,
        duration_seconds=task.estimated_duration_seconds,
        pressure=classify_resource_pressure(task),
        warnings=warnings,
        errors=[],
    )


def estimate_tasks_resources(tasks: List[LocalTask]) -> List[ResourceEstimate]:
    return [estimate_task_resources(t) for t in tasks]


def estimate_batch_resources(tasks: List[LocalTask]) -> Dict[str, Any]:
    cpu = ram = disk = network = duration = 0.0
    for t in tasks:
        c = t.estimated_cpu_pct
        if c is not None:
            cpu += c
        r = t.estimated_ram_mb
        if r is not None:
            ram += r
        d = t.estimated_disk_mb
        if d is not None:
            disk += d
        n = t.estimated_network_mb
        if n is not None:
            network += n
        u = t.estimated_duration_seconds
        if u is not None:
            duration += u

    return {
        "total_cpu_pct": cpu,
        "total_ram_mb": ram,
        "total_disk_mb": disk,
        "total_network_mb": network,
        "total_duration_seconds": duration,
        "task_count": len(tasks),
    }


def resource_estimates_to_text(
    estimates: List[ResourceEstimate], limit: int = 50
) -> str:
    lines = ["Resource Estimates", "=" * 40]
    for e in estimates[:limit]:
        lines.extend(
            [
                f"Task ID: {e.task_id}",
                f"CPU: {e.cpu_pct}% | RAM: {e.ram_mb}MB | Pressure: {e.pressure.value}",
            ]
        )
        if e.warnings:
            lines.append(f"Warnings: {', '.join(e.warnings)}")
        lines.append("-" * 20)
    return "\n".join(lines)
