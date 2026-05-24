import re

with open("usa_signal_bot/quality/data_quality_evaluator.py", "r") as f:
    content = f.read()

new_func = """
def evaluate_normalized_runtime_registry_quality(registry: Any) -> QualityScorecard:
    scorecard = QualityScorecard(scorecard_id="qs_advanced_runtime")

    if getattr(registry, 'activation_allowed', False) or getattr(registry, 'active_paper_enabled', False) or getattr(registry, 'broker_execution_enabled', False) or getattr(registry, 'paper_state_mutation_enabled', False) or getattr(registry, 'telegram_real_send_enabled', False) or getattr(registry, 'scraping_enabled', False) or getattr(registry, 'dashboard_enabled', False):
        scorecard.phase102_non_execution_compliance_score = 0.0
    else:
        scorecard.phase102_non_execution_compliance_score = 100.0
        scorecard.phase102_runtime_registry_score = 100.0 if getattr(registry, 'registry_normalized', False) else 50.0
        scorecard.phase102_config_surface_score = 100.0 if getattr(registry, 'config_surface_clean', False) else 50.0
        scorecard.phase102_provider_contract_score = 100.0 if getattr(registry, 'provider_interfaces_ready', False) else 50.0
        scorecard.phase102_provider_safety_score = 100.0 if getattr(registry, 'safety_policy_valid', False) else 0.0
    return scorecard
"""

if "evaluate_normalized_runtime_registry_quality" not in content:
    content = content + "\n" + new_func + "\n"
    with open("usa_signal_bot/quality/data_quality_evaluator.py", "w") as f:
        f.write(content)
