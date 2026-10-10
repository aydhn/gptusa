import unittest
from unittest.mock import MagicMock
from usa_signal_bot.provider_quality.selection_safety_validator import (
    validate_provider_selection_safety,
    validate_provider_ranking_safety,
    validate_provider_quality_context_safety,
    collect_provider_quality_risk_flags,
    selection_safety_validator_summary,
    selection_safety_validator_to_text
)
from usa_signal_bot.core.enums import ProviderQualityRiskFlag

class TestSelectionSafetyValidator(unittest.TestCase):
    def test_validate_provider_selection_safety(self):
        score = MagicMock()
        score.decision.value = "PREFER_FOR_RESEARCH_DATA"
        score.explanation = "good data"
        score.selectable_for_research = True
        self.assertEqual(validate_provider_selection_safety(score), [])

        score.explanation = "has trade signal"
        self.assertEqual(validate_provider_selection_safety(score), ["Explanation contains unsafe execution language"])

        score.explanation = "good data"
        score.selectable_for_research = False
        self.assertEqual(validate_provider_selection_safety(score), ["Score decision contradicts research selection capability"])

    def test_validate_provider_ranking_safety(self):
        ranking = MagicMock()
        ranking.ranking_is_research_data_only = True
        ranking.produces_trade_signal = False
        ranking.produces_order_decision = False
        self.assertEqual(validate_provider_ranking_safety(ranking), [])

        ranking.ranking_is_research_data_only = False
        ranking.produces_trade_signal = True
        ranking.produces_order_decision = True
        errors = validate_provider_ranking_safety(ranking)
        self.assertIn("ranking_is_research_data_only must be True", errors)
        self.assertIn("produces_trade_signal must be False", errors)
        self.assertIn("produces_order_decision must be False", errors)

    def test_validate_provider_quality_context_safety(self):
        context = MagicMock()
        context.research_data_only = True
        for flag in [
            "produces_trade_signal", "produces_order_decision", "network_used",
            "paid_api_used", "scraping_used", "html_parsing_used", "broker_used",
            "order_created", "paper_state_mutated", "telegram_real_sent",
            "dashboard_started"
        ]:
            setattr(context, flag, False)
        self.assertEqual(validate_provider_quality_context_safety(context), [])

        context.research_data_only = False
        context.produces_trade_signal = True
        errors = validate_provider_quality_context_safety(context)
        self.assertIn("research_data_only is False", errors)
        self.assertIn("produces_trade_signal is True", errors)

    def test_collect_provider_quality_risk_flags(self):
        self.assertEqual(collect_provider_quality_risk_flags(None), [])

        context = MagicMock()
        context.risk_flags = ["FLAG1"]

        q = MagicMock()
        q.risk_flags = ["FLAG2"]
        c = MagicMock()
        c.risk_flags = ["FLAG3"]
        q.components = [c]
        context.data_quality_scores = [q]

        t = MagicMock()
        t.risk_flags = ["FLAG4"]
        context.trust_profiles = [t]

        s = MagicMock()
        s.risk_flags = ["FLAG5"]
        context.selection_scores = [s]

        r = MagicMock()
        r.risk_flags = ["FLAG1", "FLAG6"]
        context.rankings = [r]

        flags = collect_provider_quality_risk_flags(context)
        self.assertEqual(set(flags), {"FLAG1", "FLAG2", "FLAG3", "FLAG4", "FLAG5", "FLAG6"})

    def test_selection_safety_validator_summary(self):
        self.assertEqual(selection_safety_validator_summary([]), {"safe": True, "error_count": 0, "errors": []})
        errors = ["error 1"]
        self.assertEqual(selection_safety_validator_summary(errors), {"safe": False, "error_count": 1, "errors": errors})

    def test_selection_safety_validator_to_text(self):
        self.assertEqual(selection_safety_validator_to_text([]), "Selection Safety Validator: PASSED")
        errors = ["error 1", "error 2"]
        self.assertEqual(selection_safety_validator_to_text(errors), "Selection Safety Validator: FAILED\n  error 1\n  error 2")

if __name__ == '__main__':
    unittest.main()
