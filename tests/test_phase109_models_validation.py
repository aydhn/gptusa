import unittest
import sys
from unittest.mock import patch, MagicMock


# Create a mock enum factory that supports standard instantiation and value retrieval
class CatchAllMockEnum:
    def __getattr__(self, name):
        return CatchAllMockEnum()


class MockProviderQualityValidationError(Exception):
    pass


class TestProviderCacheIngestionResultValidation(unittest.TestCase):
    def test_validation_logic(self):
        # We can just import inside the test method! This avoids ANY collection-time issues.

        # Patch the exceptions module to include the missing class
        mock_exceptions = MagicMock()
        mock_exceptions.ProviderQualityValidationError = (
            MockProviderQualityValidationError
        )

        with patch.dict(
            "sys.modules",
            {
                "pandas": MagicMock(),
                "usa_signal_bot.core.enums": CatchAllMockEnum(),
                "usa_signal_bot.core.exceptions": mock_exceptions,
            },
        ):
            from usa_signal_bot.provider_quality.phase109_models import (
                ProviderCacheIngestionResult,
                validate_provider_cache_ingestion_result,
            )

            # Valid item
            valid_item = ProviderCacheIngestionResult(
                ingestion_id="test_id",
                created_at_utc="2023-01-01T00:00:00Z",
                source_path=None,
                source_review_id=None,
                source_context_id=None,
                available=True,
                provider_cache_ready=True,
                stale_fresh_policy_valid=True,
                fallback_dry_run_ready=True,
                source_comparison_ready=True,
                metadata_only=True,
                cache_only_default=True,
                network_enabled_by_default=False,
                paid_api_enabled=False,
                scraping_enabled=False,
                html_parse_enabled=False,
                broker_execution_enabled=False,
                order_creation_enabled=False,
                paper_state_mutation_enabled=False,
                telegram_real_send_enabled=False,
                dashboard_enabled=False,
                valid_for_phase109=True,
                risk_flags=[],
                warnings=[],
                errors=[],
                metadata={},
            )

            # Happy path
            validate_provider_cache_ingestion_result(valid_item)
            self.assertEqual(len(valid_item.warnings), 0)

            # Missing cache ready
            valid_item.provider_cache_ready = False
            with self.assertRaisesRegex(
                MockProviderQualityValidationError, "provider_cache_ready must be True"
            ):
                validate_provider_cache_ingestion_result(valid_item)
            valid_item.provider_cache_ready = True

            # Missing stale policy
            valid_item.stale_fresh_policy_valid = False
            with self.assertRaisesRegex(
                MockProviderQualityValidationError,
                "stale_fresh_policy_valid must be True",
            ):
                validate_provider_cache_ingestion_result(valid_item)
            valid_item.stale_fresh_policy_valid = True

            # Missing fallback
            valid_item.fallback_dry_run_ready = False
            with self.assertRaisesRegex(
                MockProviderQualityValidationError,
                "fallback_dry_run_ready must be True",
            ):
                validate_provider_cache_ingestion_result(valid_item)
            valid_item.fallback_dry_run_ready = True

            # Missing source comparison
            valid_item.source_comparison_ready = False
            validate_provider_cache_ingestion_result(valid_item)
            self.assertIn("source_comparison_ready is false", valid_item.warnings)
            valid_item.source_comparison_ready = True

            # Missing metadata only
            valid_item.metadata_only = False
            with self.assertRaisesRegex(
                MockProviderQualityValidationError, "metadata_only must be True"
            ):
                validate_provider_cache_ingestion_result(valid_item)
            valid_item.metadata_only = True

            # Execution flags must be false
            flags = [
                (
                    "network_enabled_by_default",
                    "network_enabled_by_default must be False",
                ),
                ("paid_api_enabled", "paid_api_enabled must be False"),
                ("scraping_enabled", "scraping_enabled must be False"),
                ("html_parse_enabled", "html_parse_enabled must be False"),
                ("broker_execution_enabled", "broker_execution_enabled must be False"),
                ("order_creation_enabled", "order_creation_enabled must be False"),
                (
                    "paper_state_mutation_enabled",
                    "paper_state_mutation_enabled must be False",
                ),
                (
                    "telegram_real_send_enabled",
                    "telegram_real_send_enabled must be False",
                ),
                ("dashboard_enabled", "dashboard_enabled must be False"),
            ]

            for flag, msg in flags:
                setattr(valid_item, flag, True)
                with self.assertRaisesRegex(MockProviderQualityValidationError, msg):
                    validate_provider_cache_ingestion_result(valid_item)
                setattr(valid_item, flag, False)


if __name__ == "__main__":
    unittest.main()
