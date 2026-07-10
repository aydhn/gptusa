
import unittest
import pandas as pd
import numpy as np

from usa_signal_bot.portfolio.construction.sandbox_candidate_builder import (
    merge_candidate_overrides,
    PortfolioSandboxCandidate
)

class TestSandboxCandidateBuilder(unittest.TestCase):
    def test_merge_candidate_overrides(self):
        candidates = [
            PortfolioSandboxCandidate(
                candidate_id="c_0", created_at_utc="2023-01-01", symbol="SYM0",
                candidate_valid=True, eligible_for_sandbox=True,
                sizing_score=0.5, risk_budget_score=0.5, robustness_score=0.5,
                liquidity_score=0.5, cost_score=0.5, diversification_group="D",
                sandbox_notes=[], live_signal=False, order_decision=False,
                actual_target_weight=None, actual_portfolio_weight=None,
                actual_allocation=None, actual_position_size=None, order_size=None,
                capital_allocation=None, research_data_only=True, warnings=[],
                errors=[], risk_flags=[], metadata={}
            )
        ]

        df = pd.DataFrame({
            'symbol': ['SYM0', 'SYM1'],
            'eligible_for_sandbox': [False, True],
            'sizing_score': [0.8, 0.9],
            'diversification_group': ['A', 'B']
        })

        result = merge_candidate_overrides(candidates, df)

        self.assertEqual(len(result), 2)

        # Check SYM0 (existing)
        sym0 = next(c for c in result if c.symbol == 'SYM0')
        self.assertFalse(sym0.eligible_for_sandbox)
        self.assertEqual(sym0.sizing_score, 0.8)
        self.assertEqual(sym0.diversification_group, 'A')

        # Check SYM1 (new)
        sym1 = next(c for c in result if c.symbol == 'SYM1')
        self.assertTrue(sym1.eligible_for_sandbox)
        self.assertEqual(sym1.sizing_score, 0.9)
        self.assertEqual(sym1.diversification_group, 'B')
        self.assertEqual(sym1.metadata['inferred_from'], 'dataframe_override')

if __name__ == '__main__':
    unittest.main()
