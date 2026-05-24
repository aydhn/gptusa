import re

def update_exceptions():
    with open('usa_signal_bot/core/exceptions.py', 'r') as f:
        content = f.read()

    new_exceptions = """
class PrePaperHandoffFreezeGateError(USASignalBotError):
    pass

class HandoffFreezeSimulatorDossierIngestionError(USASignalBotError):
    pass

class HandoffFreezeEligibilityError(USASignalBotError):
    pass

class SandboxRuntimeAdmissionReplayPlanError(USASignalBotError):
    pass

class SandboxRuntimeAdmissionReplayEngineError(USASignalBotError):
    pass

class SandboxRuntimeAdmissionReplayAnalyzerError(USASignalBotError):
    pass

class SimulatorEvidenceFreezeError(USASignalBotError):
    pass

class SimulatorEvidenceFreezeValidationError(USASignalBotError):
    pass

class HandoffFreezeRuleError(USASignalBotError):
    pass

class HandoffFreezeAssertionError(USASignalBotError):
    pass

class FinalHandoffFreezeGateError(USASignalBotError):
    pass

class HandoffFreezeGateValidationError(USASignalBotError):
    pass

class HandoffFreezeContinuityError(USASignalBotError):
    pass

class HandoffFreezeSafetyValidatorError(USASignalBotError):
    pass

class HandoffFreezeAuditError(USASignalBotError):
    pass

class HandoffFreezeStorageError(USASignalBotError):
    pass

class HandoffFreezeValidationError(USASignalBotError):
    pass

class HandoffFreezeReportingError(USASignalBotError):
    pass
"""
    if "PrePaperHandoffFreezeGateError" not in content:
        content += new_exceptions

    with open('usa_signal_bot/core/exceptions.py', 'w') as f:
        f.write(content)
    print("Exceptions updated.")

if __name__ == '__main__':
    update_exceptions()
