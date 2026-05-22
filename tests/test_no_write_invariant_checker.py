from usa_signal_bot.paper_no_write_admission.no_write_invariant_checker import *
from usa_signal_bot.paper_no_write_admission.no_write_admission_models import NoWritePaperAdmissionContract
from usa_signal_bot.core.enums import NoWriteAdmissionContractStatus, NoWriteAdmissionDecision

def test_no_write_invariant_checker():
    c = NoWritePaperAdmissionContract("c", "now", NoWriteAdmissionContractStatus.CREATED, NoWriteAdmissionDecision.CREATE_NO_WRITE_CONTRACT, None, None, None, [], [], [], True, True, False, True, False, False, False, False, False, [], [], [], {})
    res = check_no_write_invariants(c)
    assert res is not None
