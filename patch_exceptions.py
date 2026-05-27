import sys
import os
# do not run from usa_signal_bot/core to avoid shadowed stdlib
with open("usa_signal_bot/core/exceptions.py", "r") as f:
    content = f.read()

new_exceptions = """
class FeatureEnrichmentError(USASignalBotError):
    pass

class AdvancedFeatureIngestionError(FeatureEnrichmentError):
    pass

class EventContextLoaderError(FeatureEnrichmentError):
    pass

class QualityMetadataLoaderError(FeatureEnrichmentError):
    pass

class CalendarMetadataLoaderError(FeatureEnrichmentError):
    pass

class EventEnrichmentSpecError(FeatureEnrichmentError):
    pass

class QualityEnrichmentSpecError(FeatureEnrichmentError):
    pass

class CalendarEnrichmentSpecError(FeatureEnrichmentError):
    pass

class EventAwareFeatureError(FeatureEnrichmentError):
    pass

class QualityAwareFeatureError(FeatureEnrichmentError):
    pass

class CalendarAwareFeatureError(FeatureEnrichmentError):
    pass

class FeatureFreshnessError(FeatureEnrichmentError):
    pass

class FeatureConfidenceError(FeatureEnrichmentError):
    pass

class FeatureAnomalyContextError(FeatureEnrichmentError):
    pass

class FeatureInteractionSpecError(FeatureEnrichmentError):
    pass

class FeatureInteractionBuilderError(FeatureEnrichmentError):
    pass

class InteractionSchemaValidationError(FeatureEnrichmentError):
    pass

class EnrichedFeatureTableBuilderError(FeatureEnrichmentError):
    pass

class EnrichedFeatureComputationValidationError(FeatureEnrichmentError):
    pass

class EnrichedFeatureOutputSafetyValidationError(FeatureEnrichmentError):
    pass

class FeatureEnrichmentStoreError(FeatureEnrichmentError):
    pass

class FeatureEnrichmentValidationError(FeatureEnrichmentError):
    pass

class FeatureEnrichmentReportingError(FeatureEnrichmentError):
    pass
"""

if "FeatureEnrichmentError" not in content:
    content += "\n" + new_exceptions
    with open("usa_signal_bot/core/exceptions.py", "w") as f:
        f.write(content)
    print("Updated exceptions.py")
else:
    print("exceptions.py already updated")
