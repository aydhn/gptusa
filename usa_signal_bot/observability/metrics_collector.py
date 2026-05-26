
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


# Phase 117 Observability
def get_latest_core_indicator_context_count(): return 0
def get_latest_core_indicator_spec_count(): return 0
def get_latest_core_indicator_computation_result_count(): return 0
def get_latest_core_feature_table_count(): return 0
def get_latest_core_feature_column_count(): return 0
def get_latest_core_feature_warmup_null_count(): return 0
def get_latest_core_feature_output_safety_violation_count(): return 0
def get_latest_core_indicator_trade_signal_violation_count(): return 0
def get_latest_phase117_execution_violation_count(): return 0
