import re

with open("usa_signal_bot/core/exceptions.py", "r") as f:
    content = f.read()

new_classes = """
class AdvancedRuntimeError(Exception): pass
class TransitionReviewIngestionError(Exception): pass
class RuntimeModeRegistryError(Exception): pass
class CapabilityPolicyError(Exception): pass
class NormalizedRuntimeRegistryError(Exception): pass
class ConfigSurfaceError(Exception): pass
class ConfigCleanupError(Exception): pass
class ConfigConflictDetectorError(Exception): pass
class ConfigMigrationHintsError(Exception): pass
class ProviderContractError(Exception): pass
class ProviderInterfaceError(Exception): pass
class ProviderCapabilityManifestError(Exception): pass
class ProviderSafetyManifestError(Exception): pass
class ProviderErrorTaxonomyError(Exception): pass
class ProviderRateLimitContractError(Exception): pass
class ProviderCachePolicyError(Exception): pass
class ProviderQualityHintError(Exception): pass
class ProviderInterfaceValidationError(Exception): pass
class SafetyPolicyValidationError(Exception): pass
class RuntimeRegistryStorageError(Exception): pass
class RuntimeRegistryValidationError(Exception): pass
class RuntimeRegistryReportingError(Exception): pass
"""

if "class AdvancedRuntimeError" not in content:
    content = content + "\n" + new_classes + "\n"
    with open("usa_signal_bot/core/exceptions.py", "w") as f:
        f.write(content)
