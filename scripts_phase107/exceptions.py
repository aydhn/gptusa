print("Adding exceptions...")
ADDITION = """
class DataProviderRuntimeError(CoreError):
    pass

class ProviderAbstractionIngestionError(DataProviderRuntimeError):
    pass

class ProviderCacheKeyError(DataProviderRuntimeError):
    pass

class ProviderCacheLookupDryRunError(DataProviderRuntimeError):
    pass

class ProviderFetchDryRunPlannerError(DataProviderRuntimeError):
    pass

class ProviderFetchDryRunExecutorError(DataProviderRuntimeError):
    pass

class ProviderRuntimeRegistryError(DataProviderRuntimeError):
    pass

class ProviderRuntimePolicyError(DataProviderRuntimeError):
    pass

class ProviderRuntimeValidationError(DataProviderRuntimeError):
    pass

class ProviderContractTestRunnerError(DataProviderRuntimeError):
    pass

class ProviderFixtureFactoryError(DataProviderRuntimeError):
    pass

class OhlcvSchemaValidationError(DataProviderRuntimeError):
    pass

class ProviderRuntimeStoreError(DataProviderRuntimeError):
    pass

class ProviderRuntimeReportingError(DataProviderRuntimeError):
    pass
"""
with open("usa_signal_bot/core/exceptions.py", "r") as f:
    content = f.read()
if "DataProviderRuntimeError" not in content:
    content += "\n" + ADDITION
    with open("usa_signal_bot/core/exceptions.py", "w") as f:
        f.write(content)
