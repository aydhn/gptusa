import unittest
import pandas as pd
from usa_signal_bot.portfolio.sizing.sizing_input_resolver import build_sizing_candidates

class TestSizingInputResolver(unittest.TestCase):
    def test_build_sizing_candidates(self):
        df = pd.DataFrame({
            'symbol': ['AAPL', 'MSFT'],
            'volatility_proxy': [0.1, 0.2],
            'drawdown_proxy': [0.05, 0.1],
            'cost_proxy': [0.01, 0.02],
            'liquidity_proxy': [1000, 2000],
            'robustness_proxy': [0.8, 0.9],
            'risk_budget_proxy': [0.03, 0.04]
        })

        candidates = build_sizing_candidates({}, df)
        self.assertEqual(len(candidates), 2)

        self.assertEqual(candidates[0].symbol, 'AAPL')
        self.assertEqual(candidates[0].volatility_proxy, 0.1)
        self.assertEqual(candidates[0].drawdown_proxy, 0.05)

        self.assertEqual(candidates[1].symbol, 'MSFT')
        self.assertEqual(candidates[1].volatility_proxy, 0.2)
        self.assertEqual(candidates[1].drawdown_proxy, 0.1)

    def test_build_sizing_candidates_missing_columns(self):
        df = pd.DataFrame({
            'symbol': ['AAPL', 'MSFT'],
            # Intentionally missing other proxy columns
        })

        candidates = build_sizing_candidates({}, df)
        self.assertEqual(len(candidates), 2)

        self.assertEqual(candidates[0].symbol, 'AAPL')
        # get() on dict will return None if not present, and we didn't specify a default for these except symbol
        self.assertIsNone(candidates[0].volatility_proxy)

    def test_build_sizing_candidates_none_df(self):
        candidates = build_sizing_candidates({}, None)
        self.assertEqual(len(candidates), 0)

if __name__ == '__main__':
    unittest.main()
