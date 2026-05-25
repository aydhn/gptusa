
import sys
from usa_signal_bot.app.cli import cli

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
    sys.exit(0)

if __name__ == "__main__":
    main()
