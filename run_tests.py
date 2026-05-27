import sys
sys.path.append('.')

from tests.test_phase119 import *

test_ingest_advanced_feature_review_payload()
test_ingest_invalid_payload()
test_build_specs()
test_feature_builders()
test_interaction_builder()
test_enriched_feature_table_builder()
test_profiles()

print("All tests passed.")
