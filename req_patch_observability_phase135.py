import sys

def patch_observability():
    file_path = "usa_signal_bot/observability/metrics_collector.py"
    try:
        with open(file_path, "r") as f:
            content = f.read()

        if "latest_regime_final_closure_context_count" not in content:
            content = content.replace(
                "latest_regime_monitoring_context_count: int = 0",
                "latest_regime_monitoring_context_count: int = 0\n    latest_regime_final_closure_context_count: int = 0\n    latest_artifact_chain_reference_count: int = 0\n    latest_artifact_chain_validation_pass_count: int = 0\n    latest_final_closure_pass_count: int = 0\n    latest_freeze_seal_created_count: int = 0\n    latest_final_safety_audit_pass_count: int = 0\n    latest_ml_input_contract_count: int = 0\n    latest_ml_kickoff_gate_pass_count: int = 0\n    latest_phase135_model_training_violation_count: int = 0\n    latest_phase135_model_prediction_violation_count: int = 0\n    latest_phase135_execution_violation_count: int = 0\n    latest_phase135_activation_violation_count: int = 0\n    latest_phase135_deployment_violation_count: int = 0\n    latest_phase135_daemon_violation_count: int = 0"
            )
            with open(file_path, "w") as f:
                f.write(content)
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    patch_observability()
