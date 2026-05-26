
class DataQualityEvaluator:
    def __init__(self):
        self.phase114_provider_freeze_score = 0.0
        self.phase114_multi_provider_final_review_score = 0.0
        self.phase114_data_layer_rehearsal_score = 0.0
        self.phase114_output_contract_score = 0.0
        self.phase114_non_execution_compliance_score = 0.0

    def evaluate_phase114_freeze(self, report):
        if not report.freeze_bundle.freeze_valid:
            self.phase114_provider_freeze_score = 0.0
        else:
            self.phase114_provider_freeze_score = 100.0

    def evaluate_phase114_safety(self, risk_flags):
        blocked_flags = {
            "GOVERNANCE_REVIEW_INVALID", "FREEZE_EVIDENCE_MISSING", "FREEZE_BUNDLE_INVALID",
            "MULTI_PROVIDER_REVIEW_FAILED", "REHEARSAL_FAILED", "OUTPUT_CONTRACT_FAILED",
            "NO_EXECUTION_PROOF_FAILED", "SECRET_LEAK_RISK"
        }
        for flag in risk_flags:
            if str(flag) in blocked_flags or getattr(flag, "value", flag) in blocked_flags:
                self.phase114_non_execution_compliance_score = 0.0
                return
        self.phase114_non_execution_compliance_score = 100.0
