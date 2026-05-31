import sys

def patch_quality():
    file_path = "usa_signal_bot/quality/data_quality_evaluator.py"
    try:
        with open(file_path, "r") as f:
            content = f.read()

        if "phase135_research_freeze_ingestion_score" not in content:
            content = content.replace(
                "phase134_research_freeze_score: int = 100",
                "phase134_research_freeze_score: int = 100\n    phase135_research_freeze_ingestion_score: int = 100\n    phase135_artifact_chain_validation_score: int = 100\n    phase135_final_closure_validation_score: int = 100\n    phase135_freeze_seal_score: int = 100\n    phase135_final_safety_audit_score: int = 100\n    phase135_ml_input_contract_score: int = 100\n    phase135_ml_kickoff_gate_score: int = 100\n    phase135_safety_score: int = 100\n    phase135_non_execution_compliance_score: int = 100\n    phase135_no_model_training_compliance_score: int = 100\n    phase135_no_model_prediction_compliance_score: int = 100\n    phase135_no_deployment_compliance_score: int = 100\n    phase135_no_daemon_compliance_score: int = 100"
            )
            with open(file_path, "w") as f:
                f.write(content)
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    patch_quality()
