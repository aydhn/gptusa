import sys

def patch_exceptions():
    file_path = "usa_signal_bot/core/exceptions.py"
    with open(file_path, "r") as f:
        content = f.read()

    new_exceptions = """
class RegimeFinalClosureError(USASignalBotError):
    pass

class RegimeResearchFreezeIngestionError(USASignalBotError):
    pass

class ResearchFreezeArtifactLoaderError(USASignalBotError):
    pass

class ArtifactChainValidationError(USASignalBotError):
    pass

class FinalClosureRuleError(USASignalBotError):
    pass

class FinalClosureValidationError(USASignalBotError):
    pass

class FreezeSealGenerationError(USASignalBotError):
    pass

class FinalSafetyAuditError(USASignalBotError):
    pass

class MLInputContractBuilderError(USASignalBotError):
    pass

class MLKickoffReadinessGateError(USASignalBotError):
    pass

class FinalClosureHashingError(USASignalBotError):
    pass

class FinalClosureSchemaValidationError(USASignalBotError):
    pass

class FinalClosureSafetyValidationError(USASignalBotError):
    pass

class FinalClosureStoreError(USASignalBotError):
    pass

class FinalClosureReportingError(USASignalBotError):
    pass
"""
    if "RegimeFinalClosureError" not in content:
        content += new_exceptions

    with open(file_path, "w") as f:
        f.write(content)

if __name__ == "__main__":
    patch_exceptions()
