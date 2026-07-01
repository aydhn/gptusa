import unittest
from usa_signal_bot.taskqueue.resource_estimator import estimate_batch_resources
from usa_signal_bot.taskqueue.task_models import LocalTask

class DummyEnum:
    def __init__(self, value):
        self.value = value

class TestResourceEstimator(unittest.TestCase):
    def test_estimate_batch_resources(self):
        tasks = [
            LocalTask(
                task_id="t1",
                task_type=DummyEnum("test"),
                name="test task",
                priority=DummyEnum("priority"),
                status=DummyEnum("status"),
                command="cmd",
                lock_scope=DummyEnum("lock"),
                dry_run=True, estimated_gpu_pct=None,
                estimated_cpu_pct=10.5,
                estimated_ram_mb=500.0,
                estimated_disk_mb=100.0,
                estimated_network_mb=10.0,
                estimated_duration_seconds=5.0
            ),
            LocalTask(
                task_id="t2",
                task_type=DummyEnum("test"),
                name="test task",
                priority=DummyEnum("priority"),
                status=DummyEnum("status"),
                command="cmd",
                lock_scope=DummyEnum("lock"),
                dry_run=True, estimated_gpu_pct=None,
                estimated_cpu_pct=20.0,
                estimated_ram_mb=None,
                estimated_disk_mb=200.0,
                estimated_network_mb=None,
                estimated_duration_seconds=10.0
            ),
            LocalTask(
                task_id="t3",
                task_type=DummyEnum("test"),
                name="test task",
                priority=DummyEnum("priority"),
                status=DummyEnum("status"),
                command="cmd",
                lock_scope=DummyEnum("lock"),
                dry_run=True, estimated_gpu_pct=None,
                estimated_cpu_pct=None,
                estimated_ram_mb=250.0,
                estimated_disk_mb=None,
                estimated_network_mb=5.0,
                estimated_duration_seconds=None
            )
        ]

        result = estimate_batch_resources(tasks)

        self.assertEqual(result["total_cpu_pct"], 30.5)
        self.assertEqual(result["total_ram_mb"], 750.0)
        self.assertEqual(result["total_disk_mb"], 300.0)
        self.assertEqual(result["total_network_mb"], 15.0)
        self.assertEqual(result["total_duration_seconds"], 15.0)
        self.assertEqual(result["task_count"], 3)

if __name__ == '__main__':
    unittest.main()
