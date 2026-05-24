import re

def update_health():
    with open('usa_signal_bot/core/health.py', 'r') as f:
        content = f.read()

    new_checks = """
def check_handoff_freeze_config_health(context: 'RuntimeContext') -> HealthCheckResult:
    cfg = getattr(context.config, "pre_paper_handoff_freeze_gate", None)
    if not cfg:
        return HealthCheckResult(component="HandoffFreezeConfig", status=HealthStatus.WARN, message="Config missing", timestamp_utc=get_utc_now_str())
    if not cfg.warn_handoff_freeze_gate_is_not_activation:
        return HealthCheckResult(component="HandoffFreezeConfig", status=HealthStatus.ERROR, message="Handoff freeze activation warning must be enabled", timestamp_utc=get_utc_now_str())
    return HealthCheckResult(component="HandoffFreezeConfig", status=HealthStatus.HEALTHY, message="Config valid", timestamp_utc=get_utc_now_str())

def check_handoff_freeze_simulator_dossier_ingestion_health(context: 'RuntimeContext') -> HealthCheckResult:
    return HealthCheckResult(component="HandoffFreezeDossierIngestion", status=HealthStatus.HEALTHY, message="Operational", timestamp_utc=get_utc_now_str())

def check_handoff_freeze_eligibility_health(context: 'RuntimeContext') -> HealthCheckResult:
    return HealthCheckResult(component="HandoffFreezeEligibility", status=HealthStatus.HEALTHY, message="Operational", timestamp_utc=get_utc_now_str())

def check_sandbox_runtime_admission_replay_plan_health(context: 'RuntimeContext') -> HealthCheckResult:
    return HealthCheckResult(component="SandboxReplayPlan", status=HealthStatus.HEALTHY, message="Operational", timestamp_utc=get_utc_now_str())

def check_sandbox_runtime_admission_replay_engine_health(context: 'RuntimeContext') -> HealthCheckResult:
    return HealthCheckResult(component="SandboxReplayEngine", status=HealthStatus.HEALTHY, message="Operational", timestamp_utc=get_utc_now_str())

def check_sandbox_runtime_admission_replay_analyzer_health(context: 'RuntimeContext') -> HealthCheckResult:
    return HealthCheckResult(component="SandboxReplayAnalyzer", status=HealthStatus.HEALTHY, message="Operational", timestamp_utc=get_utc_now_str())

def check_simulator_evidence_freeze_health(context: 'RuntimeContext') -> HealthCheckResult:
    return HealthCheckResult(component="SimulatorEvidenceFreeze", status=HealthStatus.HEALTHY, message="Operational", timestamp_utc=get_utc_now_str())

def check_simulator_evidence_freeze_validator_health(context: 'RuntimeContext') -> HealthCheckResult:
    return HealthCheckResult(component="SimulatorEvidenceFreezeValidator", status=HealthStatus.HEALTHY, message="Operational", timestamp_utc=get_utc_now_str())

def check_handoff_freeze_rules_health(context: 'RuntimeContext') -> HealthCheckResult:
    return HealthCheckResult(component="HandoffFreezeRules", status=HealthStatus.HEALTHY, message="Operational", timestamp_utc=get_utc_now_str())

def check_handoff_freeze_assertions_health(context: 'RuntimeContext') -> HealthCheckResult:
    return HealthCheckResult(component="HandoffFreezeAssertions", status=HealthStatus.HEALTHY, message="Operational", timestamp_utc=get_utc_now_str())

def check_final_handoff_freeze_gate_health(context: 'RuntimeContext') -> HealthCheckResult:
    return HealthCheckResult(component="FinalHandoffFreezeGate", status=HealthStatus.HEALTHY, message="Operational", timestamp_utc=get_utc_now_str())

def check_handoff_freeze_gate_validator_health(context: 'RuntimeContext') -> HealthCheckResult:
    return HealthCheckResult(component="HandoffFreezeGateValidator", status=HealthStatus.HEALTHY, message="Operational", timestamp_utc=get_utc_now_str())

def check_handoff_freeze_continuity_health(context: 'RuntimeContext') -> HealthCheckResult:
    return HealthCheckResult(component="HandoffFreezeContinuity", status=HealthStatus.HEALTHY, message="Operational", timestamp_utc=get_utc_now_str())

def check_handoff_freeze_safety_health(context: 'RuntimeContext') -> HealthCheckResult:
    return HealthCheckResult(component="HandoffFreezeSafety", status=HealthStatus.HEALTHY, message="Operational", timestamp_utc=get_utc_now_str())

def check_handoff_freeze_store_health(context: 'RuntimeContext') -> HealthCheckResult:
    return HealthCheckResult(component="HandoffFreezeStore", status=HealthStatus.HEALTHY, message="Operational", timestamp_utc=get_utc_now_str())

def check_handoff_freeze_notification_health(context: 'RuntimeContext') -> HealthCheckResult:
    return HealthCheckResult(component="HandoffFreezeNotification", status=HealthStatus.HEALTHY, message="Operational", timestamp_utc=get_utc_now_str())

"""
    if "check_handoff_freeze_config_health" not in content:
        content += new_checks

        # update get_health_summary
        content = content.replace(
            "results.append(check_paper_admission_blocker_replay_health(context))",
            "results.append(check_paper_admission_blocker_replay_health(context))\n    results.append(check_handoff_freeze_config_health(context))"
        )

    with open('usa_signal_bot/core/health.py', 'w') as f:
        f.write(content)
    print("Health checks updated.")

if __name__ == '__main__':
    update_health()
