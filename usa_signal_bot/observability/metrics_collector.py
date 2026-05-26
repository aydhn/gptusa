
class MetricsCollector:
    def __init__(self):
        self.latest_provider_freeze_context_count = 0
        self.latest_provider_expansion_freeze_count = 0
        self.latest_provider_freeze_valid_count = 0
        self.latest_multi_provider_review_count = 0
        self.latest_multi_provider_review_pass_count = 0
        self.latest_data_layer_rehearsal_count = 0
        self.latest_data_layer_rehearsal_pass_count = 0
        self.latest_output_contract_pass_count = 0
        self.latest_freeze_artifact_manifest_count = 0
        self.latest_freeze_secret_violation_count = 0
        self.latest_freeze_trade_signal_violation_count = 0
        self.latest_phase114_execution_violation_count = 0

    def record_freeze_metrics(self, bundle):
        self.latest_provider_expansion_freeze_count += 1
        if bundle.freeze_valid:
            self.latest_provider_freeze_valid_count += 1
        self.latest_freeze_secret_violation_count += bundle.secret_violation_count
        self.latest_freeze_trade_signal_violation_count += bundle.trade_signal_violation_count
        self.latest_phase114_execution_violation_count += bundle.execution_violation_count

# Phase 113 Observability dummy
def collect_phase113_metrics(): pass
