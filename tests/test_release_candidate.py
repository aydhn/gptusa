
import unittest
from usa_signal_bot.research_governance.release_candidate import release_candidate_status_from_decision
from usa_signal_bot.research_governance.governance_models import PromotionDecision, ReleaseCandidateStatus

class TestReleaseCandidate(unittest.TestCase):
    def test_release_candidate(self):
        s = release_candidate_status_from_decision(PromotionDecision.ACCEPT_AS_LOCAL_RESEARCH_CANDIDATE)
        self.assertEqual(s, ReleaseCandidateStatus.ACCEPTED_FOR_LOCAL_RESEARCH)
