import re

def update_metrics():
    with open('usa_signal_bot/observability/metrics_collector.py', 'r') as f:
        content = f.read()

    new_metrics = """
    def collect_handoff_freeze_metrics(self) -> List[OperationalMetric]:
        m = []
        try:
            from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_store import handoff_freeze_store_summary

            summary = handoff_freeze_store_summary(self.data_root)

            m.append(OperationalMetric(
                metric_id=create_operational_metric_id(),
                metric_type=MetricType.COUNTER,
                name="latest_handoff_freeze_gate_count",
                value=summary.get("gates", 0),
                timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                labels={"source": "handoff_freeze_store"},
                status=OperationalMetricStatus.HEALTHY
            ))
            m.append(OperationalMetric(
                metric_id=create_operational_metric_id(),
                metric_type=MetricType.COUNTER,
                name="latest_sandbox_runtime_admission_replay_count",
                value=summary.get("replay_results", 0),
                timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                labels={"source": "handoff_freeze_store"},
                status=OperationalMetricStatus.HEALTHY
            ))
            m.append(OperationalMetric(
                metric_id=create_operational_metric_id(),
                metric_type=MetricType.COUNTER,
                name="latest_simulator_evidence_freeze_count",
                value=summary.get("evidence_freezes", 0),
                timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                labels={"source": "handoff_freeze_store"},
                status=OperationalMetricStatus.HEALTHY
            ))
            m.append(OperationalMetric(
                metric_id=create_operational_metric_id(),
                metric_type=MetricType.COUNTER,
                name="phase_100_pre_paper_handoff_complete_count",
                value=summary.get("full_reviews", 0),
                timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                labels={"source": "handoff_freeze_store"},
                status=OperationalMetricStatus.HEALTHY
            ))
        except Exception:
            pass
        return m
"""
    if "collect_handoff_freeze_metrics" not in content:
        content = content.replace(
            "def collect_log_summaries",
            new_metrics + "\n    def collect_log_summaries"
        )
        content = content.replace(
            "m.extend(self.collect_execution_metrics())",
            "m.extend(self.collect_execution_metrics())\n        m.extend(self.collect_handoff_freeze_metrics())"
        )
        with open('usa_signal_bot/observability/metrics_collector.py', 'w') as f:
            f.write(content)

update_metrics()
