import pytest
from usa_signal_bot.paper_pre_rehearsal.pre_rehearsal_reporting import pre_paper_store_summary_to_text

def test_reporting():
    summary = {"plans": 1, "runs": 2, "checkpoints": 3, "reviews": 4}
    text = pre_paper_store_summary_to_text(summary)
    assert "1 plans" in text
