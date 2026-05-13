import tempfile
from pathlib import Path
from usa_signal_bot.execution.execution_store import execution_store_dir, write_execution_realism_review_json
from usa_signal_bot.execution.liquidity_models import ExecutionRealismReview
from usa_signal_bot.core.enums import ExecutionReportType

def test_store():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d)
        ed = execution_store_dir(p)
        assert ed.exists()

        rev = ExecutionRealismReview(
            review_id="id",
            created_at_utc="",
            report_type=ExecutionReportType.FULL_EXECUTION_REVIEW,
            symbols=["SPY"],
            liquidity_profiles=[],
            tradability_results=[],
            borrowability_results=[]
        )
        write_execution_realism_review_json(ed / "test.json", rev)
        assert (ed / "test.json").exists()
