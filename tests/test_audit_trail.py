
import unittest
from usa_signal_bot.research_governance.audit_trail import create_governance_audit_event

class TestAuditTrail(unittest.TestCase):
    def test_audit_trail(self):
        ev = create_governance_audit_event("test", "id1", {"secret": "123"})
        self.assertEqual(ev["payload"]["secret"], "***REDACTED***")
