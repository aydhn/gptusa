import unittest
from unittest.mock import MagicMock

# standard module imports
from usa_signal_bot.provider_quality.phase109_models import (
    validate_provider_cache_ingestion_result,
)
from usa_signal_bot.core.exceptions import ProviderQualityValidationError

class TestValidateProviderCacheIngestionResult(unittest.TestCase):
    def _create_valid_item(self):
        item = MagicMock()
        item.provider_cache_ready = True
        item.stale_fresh_policy_valid = True
        item.fallback_dry_run_ready = True
        item.source_comparison_ready = True
        item.metadata_only = True

        item.network_enabled_by_default = False
        item.paid_api_enabled = False
        item.scraping_enabled = False
        item.html_parse_enabled = False
        item.broker_execution_enabled = False
        item.order_creation_enabled = False
        item.paper_state_mutation_enabled = False
        item.telegram_real_send_enabled = False
        item.dashboard_enabled = False
        return item

    def test_happy_path_valid_item(self):
        item = self._create_valid_item()
        # Should not raise an exception
        validate_provider_cache_ingestion_result(item)
        item.warnings.append.assert_not_called()

    def test_provider_cache_ready_is_false(self):
        item = self._create_valid_item()
        item.provider_cache_ready = False
        with self.assertRaisesRegex(ProviderQualityValidationError, "provider_cache_ready must be True"):
            validate_provider_cache_ingestion_result(item)

    def test_stale_fresh_policy_valid_is_false(self):
        item = self._create_valid_item()
        item.stale_fresh_policy_valid = False
        with self.assertRaisesRegex(ProviderQualityValidationError, "stale_fresh_policy_valid must be True"):
            validate_provider_cache_ingestion_result(item)

    def test_fallback_dry_run_ready_is_false(self):
        item = self._create_valid_item()
        item.fallback_dry_run_ready = False
        with self.assertRaisesRegex(ProviderQualityValidationError, "fallback_dry_run_ready must be True"):
            validate_provider_cache_ingestion_result(item)

    def test_metadata_only_is_false(self):
        item = self._create_valid_item()
        item.metadata_only = False
        with self.assertRaisesRegex(ProviderQualityValidationError, "metadata_only must be True"):
            validate_provider_cache_ingestion_result(item)

    def test_network_enabled_by_default_is_true(self):
        item = self._create_valid_item()
        item.network_enabled_by_default = True
        with self.assertRaisesRegex(ProviderQualityValidationError, "network_enabled_by_default must be False"):
            validate_provider_cache_ingestion_result(item)

    def test_paid_api_enabled_is_true(self):
        item = self._create_valid_item()
        item.paid_api_enabled = True
        with self.assertRaisesRegex(ProviderQualityValidationError, "paid_api_enabled must be False"):
            validate_provider_cache_ingestion_result(item)

    def test_scraping_enabled_is_true(self):
        item = self._create_valid_item()
        item.scraping_enabled = True
        with self.assertRaisesRegex(ProviderQualityValidationError, "scraping_enabled must be False"):
            validate_provider_cache_ingestion_result(item)

    def test_html_parse_enabled_is_true(self):
        item = self._create_valid_item()
        item.html_parse_enabled = True
        with self.assertRaisesRegex(ProviderQualityValidationError, "html_parse_enabled must be False"):
            validate_provider_cache_ingestion_result(item)

    def test_broker_execution_enabled_is_true(self):
        item = self._create_valid_item()
        item.broker_execution_enabled = True
        with self.assertRaisesRegex(ProviderQualityValidationError, "broker_execution_enabled must be False"):
            validate_provider_cache_ingestion_result(item)

    def test_order_creation_enabled_is_true(self):
        item = self._create_valid_item()
        item.order_creation_enabled = True
        with self.assertRaisesRegex(ProviderQualityValidationError, "order_creation_enabled must be False"):
            validate_provider_cache_ingestion_result(item)

    def test_paper_state_mutation_enabled_is_true(self):
        item = self._create_valid_item()
        item.paper_state_mutation_enabled = True
        with self.assertRaisesRegex(ProviderQualityValidationError, "paper_state_mutation_enabled must be False"):
            validate_provider_cache_ingestion_result(item)

    def test_telegram_real_send_enabled_is_true(self):
        item = self._create_valid_item()
        item.telegram_real_send_enabled = True
        with self.assertRaisesRegex(ProviderQualityValidationError, "telegram_real_send_enabled must be False"):
            validate_provider_cache_ingestion_result(item)

    def test_dashboard_enabled_is_true(self):
        item = self._create_valid_item()
        item.dashboard_enabled = True
        with self.assertRaisesRegex(ProviderQualityValidationError, "dashboard_enabled must be False"):
            validate_provider_cache_ingestion_result(item)

    def test_warning_appended_when_source_comparison_ready_is_false(self):
        item = self._create_valid_item()
        item.source_comparison_ready = False
        validate_provider_cache_ingestion_result(item)
        item.warnings.append.assert_called_once_with("source_comparison_ready is false")

if __name__ == "__main__":
    unittest.main()
