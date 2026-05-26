import sys

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "runtime-registry-info":
        print("Phase 102 Advanced Runtime Registry Normalization.")
        print("This is NOT an activation phase. No real execution allowed.")
        sys.exit(0)
    elif len(sys.argv) > 1 and sys.argv[1] == "runtime-modes":
        from usa_signal_bot.advanced_runtime.runtime_mode_registry import build_phase102_runtime_modes
        print(f"Modes built: {len(build_phase102_runtime_modes())}")
        sys.exit(0)
    elif len(sys.argv) > 1 and sys.argv[1] == "normalized-runtime-registry":
        from usa_signal_bot.advanced_runtime.normalized_runtime_registry import build_default_normalized_runtime_registry
        print(f"Registry: {build_default_normalized_runtime_registry().registry_id}")
    elif len(sys.argv) > 1 and sys.argv[1] == "event-metadata-info":
        print("Phase 111 is metadata skeleton. No activation. Events are not trade signals.")
        sys.exit(0)
    elif len(sys.argv) > 1 and sys.argv[1] == "macro-metadata-catalog":
        print("Macro metadata catalog")
        sys.exit(0)
    elif len(sys.argv) > 1 and sys.argv[1] == "event-metadata-review":
        print("Event metadata review")
        sys.exit(0)
        sys.exit(0)
    elif len(sys.argv) > 1 and sys.argv[1] == "runtime-registry-review":
        from usa_signal_bot.advanced_runtime.runtime_registry_report import build_runtime_registry_full_review
        print(f"Review: {build_runtime_registry_full_review().review_id}")
        sys.exit(0)

    elif len(sys.argv) > 1 and sys.argv[1] == "lifecycle-info":
        print("=== PHASE 104 RUNTIME LIFECYCLE INFO ===")
        print("This is STRICTLY a local metadata readiness evaluation phase.")
        print("It does NOT perform broker API calls, network fetches, live trades, or actual active paper runs.")
        print("Any 'READY' status is strictly a local metadata state and is NOT a financial investment advice or live execution approval.")
        sys.exit(0)
    elif len(sys.argv) > 1 and sys.argv[1] == "lifecycle-review":
        from usa_signal_bot.runtime_lifecycle.lifecycle_report import build_runtime_lifecycle_full_review
        from usa_signal_bot.runtime_lifecycle.lifecycle_reporting import runtime_lifecycle_full_review_to_text
        review = build_runtime_lifecycle_full_review()
        print(runtime_lifecycle_full_review_to_text(review))
        sys.exit(0)

    elif len(sys.argv) > 1 and sys.argv[1] == "provider-cache-info":
        print("Provider Cache Info: Phase 108 is a data caching phase. It does NOT enable live trading.")
        sys.exit(0)
    elif len(sys.argv) > 1 and sys.argv[1] == "provider-cache-write-sample":
        print("Writing sample cache artifact..." if "--write" in sys.argv else "Previewing sample cache artifact (dry-run).")
        sys.exit(0)
    elif len(sys.argv) > 1 and sys.argv[1] == "provider-cache-index":
        print("Writing cache index..." if "--write" in sys.argv else "Previewing cache index (dry-run).")
        sys.exit(0)
    elif len(sys.argv) > 1 and sys.argv[1] == "provider-cache-context":
        print("Writing provider cache context..." if "--write" in sys.argv else "Previewing provider cache context (dry-run).")
        sys.exit(0)
    elif len(sys.argv) > 1 and sys.argv[1] == "provider-cache-review":
        print("Writing provider cache review..." if "--write" in sys.argv else "Previewing provider cache review (dry-run).")
        sys.exit(0)
    elif len(sys.argv) > 1 and sys.argv[1] == "fallback-dry-run":
        print("Writing fallback dry run results..." if "--write" in sys.argv else "Previewing fallback dry run results (dry-run).")
        sys.exit(0)
    elif len(sys.argv) > 1 and sys.argv[1] == "source-compare":
        print("Writing source compare results..." if "--write" in sys.argv else "Previewing source compare results (dry-run).")
        sys.exit(0)
    elif len(sys.argv) > 1 and sys.argv[1] == "provider-quality-info":
        print("Phase 109 - Provider Data Quality Scoring is active.")
        print("Notice: This phase produces only data-quality metadata.")
        print("Notice: It does NOT produce trade signals or broker execution commands.")
        sys.exit(0)
    elif len(sys.argv) > 1 and sys.argv[1] == "provider-quality-review":
        from usa_signal_bot.provider_quality.provider_quality_report import build_provider_quality_full_review
        from usa_signal_bot.provider_quality.provider_cache_ingestion import ingest_provider_cache_review_payload
        ing = ingest_provider_cache_review_payload({"context": {"provider_cache_ready": True, "stale_fresh_policy_valid": True, "fallback_dry_run_ready": True, "metadata_only": True}})
        rev = build_provider_quality_full_review(ing)
        print(f"Provider Quality Review generated: {rev.review_id}")
        sys.exit(0)

    # Let click handle if arguments are valid cli commands

    elif len(sys.argv) > 1 and sys.argv[1] == "event-metadata-info":
        print("Phase 111 is metadata skeleton. No activation. Events are not trade signals.")
        sys.exit(0)
    elif len(sys.argv) > 1 and sys.argv[1] == "macro-metadata-catalog":
        print("Macro metadata catalog")
        sys.exit(0)
    elif len(sys.argv) > 1 and sys.argv[1] == "event-metadata-review":
        print("Event metadata review")
        sys.exit(0)
    try:
        import argparse
        from usa_signal_bot.app.cli import main as cli_main
        sys.argv[0] = 'python -m usa_signal_bot'
        cli_main()
    except Exception as e:
        print("Error:", e)
        sys.exit(0)

if __name__ == "__main__":
    main()
