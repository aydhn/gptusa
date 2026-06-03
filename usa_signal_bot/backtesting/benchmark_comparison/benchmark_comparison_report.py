from usa_signal_bot.backtesting.benchmark_comparison.phase149_models import *
def build_benchmark_comparison_context() -> BenchmarkComparisonContext:
    return BenchmarkComparisonContext(context_id=create_benchmark_comparison_context_id(), created_at_utc="")
def build_benchmark_comparison_full_review() -> BenchmarkComparisonFullReview:
    return BenchmarkComparisonFullReview(review_id=create_benchmark_comparison_full_review_id(), created_at_utc="")
def benchmark_comparison_limitations_text() -> str: return ""
def benchmark_comparison_full_review_to_text(r, limit=300) -> str: return ""
