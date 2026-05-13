from usa_signal_bot.execution.execution_realism import ExecutionRealismEvaluator

def test_execution_realism():
    payload = {
        "SPY": [{"close": 100, "volume": 1000000}] * 60,
    }
    evaluator = ExecutionRealismEvaluator()
    review = evaluator.evaluate_symbol_payload(payload)
    assert review.symbols == ["SPY"]
    assert len(review.tradability_results) == 1
