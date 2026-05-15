def update_metrics():
    with open('usa_signal_bot/observability/metrics_collector.py', 'r') as f:
        content = f.read()

    new_metrics = """
    def collect_regime_cost_metrics(self) -> List[OperationalMetric]:
        m = []
        try:
            from usa_signal_bot.regime_costs.regime_cost_store import get_latest_regime_cost_review, read_regime_cost_review_json

            latest_file = get_latest_regime_cost_review(self.data_root)
            if latest_file:
                rev = read_regime_cost_review_json(latest_file)
                snaps = rev.get("snapshots", [])

                high_risk = sum(1 for s in snaps if s.get("combined_regime") == "HIGH_RISK")
                blocked = sum(1 for s in snaps if s.get("combined_regime") == "BLOCKED")

                m.append(OperationalMetric(
                    metric_id=create_operational_metric_id(),
                    metric_type=MetricType.COUNTER,
                    name="regime_cost_high_risk_count",
                    value=high_risk,
                    timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    labels={"source": "regime_cost_review"},
                    status=OperationalMetricStatus.HEALTHY
                ))
                m.append(OperationalMetric(
                    metric_id=create_operational_metric_id(),
                    metric_type=MetricType.COUNTER,
                    name="adaptive_execution_block_count",
                    value=blocked,
                    timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    labels={"source": "regime_cost_review"},
                    status=OperationalMetricStatus.HEALTHY
                ))
        except Exception:
            pass
        return m
"""
    if "collect_regime_cost_metrics" not in content:
        # insert into class
        content = content.replace(
            "def collect_log_summaries",
            new_metrics + "\n    def collect_log_summaries"
        )
        # add to collect_all
        content = content.replace(
            "m.extend(self.collect_execution_metrics())",
            "m.extend(self.collect_execution_metrics())\n        m.extend(self.collect_regime_cost_metrics())"
        )
        with open('usa_signal_bot/observability/metrics_collector.py', 'w') as f:
            f.write(content)

update_metrics()
