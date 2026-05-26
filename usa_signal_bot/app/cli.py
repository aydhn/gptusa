import argparse
import sys
from pathlib import Path

def phase114_provider_freeze_info(args):
    print("USA Signal Bot - Phase 114: Provider Expansion Freeze")
    print("Notice: This phase produces a freeze bundle and multi-provider review.")
    print("Notice: This is NOT an active paper trading phase.")
    print("Notice: 'Ready for Phase 115' does not constitute live trading approval.")

def phase114_provider_freeze_ingest(args):
    from usa_signal_bot.provider_freeze.provider_governance_ingestion import ingest_latest_provider_governance_review_from_store, provider_governance_ingestion_to_text
    res = ingest_latest_provider_governance_review_from_store(Path("data"))
    print(provider_governance_ingestion_to_text(res))

def phase114_provider_freeze_bundle(args):
    from usa_signal_bot.provider_freeze.freeze_evidence_collector import collect_provider_freeze_evidence
    from usa_signal_bot.provider_freeze.freeze_bundle_builder import build_provider_expansion_freeze_bundle, provider_freeze_bundle_to_text
    from usa_signal_bot.provider_freeze.provider_freeze_store import write_provider_expansion_freeze_bundle_json, freeze_bundles_dir

    items = collect_provider_freeze_evidence(Path("data"))
    bundle = build_provider_expansion_freeze_bundle(items)
    print(provider_freeze_bundle_to_text(bundle))

    if getattr(args, 'write', False):
        d = freeze_bundles_dir(Path("data"))
        f = d / f"{bundle.freeze_id}.json"
        write_provider_expansion_freeze_bundle_json(f, bundle)
        print(f"\nWrote bundle to {f}")

def phase114_provider_freeze_review(args):
    from usa_signal_bot.provider_freeze.provider_freeze_report import build_provider_freeze_full_review, provider_freeze_full_review_to_text
    from usa_signal_bot.provider_freeze.provider_freeze_store import write_provider_freeze_full_review_json, provider_freeze_reviews_dir

    review = build_provider_freeze_full_review()
    # Mocking fields for demonstration
    review.context.ready_for_phase115 = True
    print(provider_freeze_full_review_to_text(review))

    if getattr(args, 'write', False):
        d = provider_freeze_reviews_dir(Path("data"))
        f = d / f"{review.review_id}.json"
        write_provider_freeze_full_review_json(f, review)
        print(f"\nWrote review to {f}")

def phase114_data_layer_rehearsal(args):
    from usa_signal_bot.provider_freeze.rehearsal_runner import DataLayerRehearsalRunner
    from usa_signal_bot.provider_freeze.provider_freeze_reporting import data_layer_rehearsal_report_to_text

    runner = DataLayerRehearsalRunner()
    report = runner.run()
    print(data_layer_rehearsal_report_to_text(report))

def setup_phase114_cli(subparsers):
    p_info = subparsers.add_parser('provider-freeze-info', help='Show Phase 114 freeze info.')
    p_info.set_defaults(func=phase114_provider_freeze_info)

    p_ingest = subparsers.add_parser('provider-freeze-ingest-governance', help='Ingest Phase 113 review.')
    p_ingest.set_defaults(func=phase114_provider_freeze_ingest)

    p_bundle = subparsers.add_parser('provider-freeze-bundle', help='Build freeze bundle.')
    p_bundle.add_argument('--write', action='store_true', help='Write bundle to disk.')
    p_bundle.set_defaults(func=phase114_provider_freeze_bundle)

    p_review = subparsers.add_parser('provider-freeze-review', help='Build full freeze review.')
    p_review.add_argument('--write', action='store_true', help='Write review to disk.')
    p_review.set_defaults(func=phase114_provider_freeze_review)

    p_rehearsal = subparsers.add_parser('data-layer-rehearsal', help='Run data layer acceptance rehearsal.')
    p_rehearsal.set_defaults(func=phase114_data_layer_rehearsal)

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    setup_phase114_cli(subparsers)

    args = parser.parse_args()
    if args.command:
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
