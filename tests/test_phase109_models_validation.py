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


class TestProviderQualityContextValidation(unittest.TestCase):
    def test_validation_logic(self):
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
                ProviderQualityContext,
                validate_provider_quality_context,
            )

            valid_item = ProviderQualityContext(
                context_id="test_ctx_id",
                created_at_utc="2023-01-01T00:00:00Z",
                status=CatchAllMockEnum(),
                decision=CatchAllMockEnum(),
                source_provider_cache_review_id=None,
                ingestion=MagicMock(),
                data_quality_scores=[],
                trust_profiles=[],
                selection_scores=[],
                rankings=[],
                provider_quality_ready=True,
                source_trust_ready=True,
                provider_selection_scoring_ready=True,
                metadata_only=True,
                research_data_only=True,
                produces_trade_signal=False,
                produces_order_decision=False,
                network_used=False,
                paid_api_used=False,
                scraping_used=False,
                html_parsing_used=False,
                broker_used=False,
                order_created=False,
                paper_state_mutated=False,
                telegram_real_sent=False,
                dashboard_started=False,
                risk_flags=[],
                warnings=[],
                errors=[],
                metadata={},
            )

            # Happy path
            validate_provider_quality_context(valid_item)

            # Missing research_data_only
            valid_item.research_data_only = False
            with self.assertRaisesRegex(
                MockProviderQualityValidationError, "research_data_only must be True"
            ):
                validate_provider_quality_context(valid_item)
            valid_item.research_data_only = True

            # Execution flags must be false
            flags = [
                ("produces_trade_signal", "produces_trade_signal must be False"),
                ("produces_order_decision", "produces_order_decision must be False"),
                ("network_used", "network_used must be False"),
                ("paid_api_used", "paid_api_used must be False"),
                ("scraping_used", "scraping_used must be False"),
                ("html_parsing_used", "html_parsing_used must be False"),
                ("broker_used", "broker_used must be False"),
                ("order_created", "order_created must be False"),
                ("paper_state_mutated", "paper_state_mutated must be False"),
                ("telegram_real_sent", "telegram_real_sent must be False"),
                ("dashboard_started", "dashboard_started must be False"),
            ]

            for flag, msg in flags:
                setattr(valid_item, flag, True)
                with self.assertRaisesRegex(MockProviderQualityValidationError, msg):
                    validate_provider_quality_context(valid_item)
                setattr(valid_item, flag, False)


if __name__ == "__main__":
    unittest.main()
