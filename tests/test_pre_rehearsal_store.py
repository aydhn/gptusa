import pytest
from pathlib import Path
from usa_signal_bot.paper_pre_rehearsal.pre_rehearsal_store import pre_paper_rehearsal_store_summary

def test_store_summary(tmp_path):
    s = pre_paper_rehearsal_store_summary(tmp_path)
    assert s["plans"] == 0
