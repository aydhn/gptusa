
import unittest
from pathlib import Path
from usa_signal_bot.research_governance.governance_store import governance_store_dir

class TestGovernanceStore(unittest.TestCase):
    def test_governance_store(self):
        p = governance_store_dir(Path("data"))
        self.assertTrue(p.name == "research_governance")
