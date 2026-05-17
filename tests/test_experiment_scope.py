
from usa_signal_bot.research_workflow.experiment_scope import experiment_scope_risk_level
from usa_signal_bot.core.enums import ExperimentScope, ResearchRiskLevel

def test_scope_risk():
    assert experiment_scope_risk_level(ExperimentScope.PORTFOLIO_LEVEL) == ResearchRiskLevel.HIGH
