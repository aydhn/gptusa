
import unittest
from usa_signal_bot.research_governance.evidence_pack import build_evidence_pack_from_comparison_report
from usa_signal_bot.research_governance.governance_models import EvidencePackStatus

class TestEvidencePack(unittest.TestCase):
    def test_evidence_pack(self):
        pack = build_evidence_pack_from_comparison_report({})
        self.assertIn(pack.status, [EvidencePackStatus.MISSING_REQUIRED_EVIDENCE, EvidencePackStatus.INVALID])
