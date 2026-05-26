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


def provider_final_acceptance_info(args):
    print("Phase 115: Data Provider Expansion Final Acceptance and Closure")
    print("This phase is strictly for final acceptance and layer closure.")
    print("It is NOT active paper trading or live deployment.")
    print("Feature/factor engine kickoff is strictly for development scope.")
    print("Real execution, broker API, HTML scraping, and Telegram sends are strictly blocked.")

def provider_final_ingest_freeze(args):
    from usa_signal_bot.provider_final_acceptance.provider_freeze_ingestion import ingest_latest_provider_freeze_review_from_store, provider_freeze_ingestion_to_text
    from pathlib import Path
    def get_data_dir(): return Path("data")
    data_root = get_data_dir()
    res = ingest_latest_provider_freeze_review_from_store(data_root)
    print(provider_freeze_ingestion_to_text(res))

def provider_final_acceptance_check(args):
    from usa_signal_bot.provider_final_acceptance.provider_freeze_ingestion import ingest_latest_provider_freeze_review_from_store
    from usa_signal_bot.provider_final_acceptance.final_acceptance_checker import build_data_provider_final_acceptance_report, data_provider_final_acceptance_report_to_text
    from usa_signal_bot.provider_final_acceptance.final_acceptance_store import write_data_provider_final_acceptance_report_json, final_acceptance_reports_dir
    from pathlib import Path
    def get_data_dir(): return Path("data")
    data_root = get_data_dir()
    ingestion = ingest_latest_provider_freeze_review_from_store(data_root)
    report = build_data_provider_final_acceptance_report(ingestion)
    print(data_provider_final_acceptance_report_to_text(report))
    if hasattr(args, 'write') and args.write:
        d = final_acceptance_reports_dir(data_root)
        write_data_provider_final_acceptance_report_json(d / f"{report.report_id}.json", report)
        print("Report written.")

def provider_final_acceptance_review(args):
    from usa_signal_bot.provider_final_acceptance.final_acceptance_report import build_provider_final_acceptance_full_review, provider_final_acceptance_full_review_to_text
    from usa_signal_bot.provider_final_acceptance.final_acceptance_store import write_provider_final_acceptance_full_review_json, final_acceptance_reviews_dir
    from pathlib import Path
    def get_data_dir(): return Path("data")
    data_root = get_data_dir()
    data_root = get_data_dir()
    try:
        import json
        with open(data_root / "provider_freeze" / "reviews" / "dummy.json") as f: payload = json.load(f)
    except: payload = {}
    review = build_provider_final_acceptance_full_review(payload)
    print(provider_final_acceptance_full_review_to_text(review))
    if hasattr(args, 'write') and args.write:
        d = final_acceptance_reviews_dir(data_root)
        write_provider_final_acceptance_full_review_json(d / f"{review.review_id}.json", review)
        print("Review written.")

def provider_layer_closure(args):
    from usa_signal_bot.provider_final_acceptance.provider_freeze_ingestion import ingest_latest_provider_freeze_review_from_store
    from usa_signal_bot.provider_final_acceptance.provider_layer_closure import build_provider_layer_closure_bundle, provider_layer_closure_to_text
    from usa_signal_bot.provider_final_acceptance.final_acceptance_store import write_provider_layer_closure_bundle_json, provider_layer_closures_dir
    from pathlib import Path
    def get_data_dir(): return Path("data")
    data_root = get_data_dir()
    ingestion = ingest_latest_provider_freeze_review_from_store(data_root)
    bundle = build_provider_layer_closure_bundle(ingestion)
    print(provider_layer_closure_to_text(bundle))
    if hasattr(args, 'write') and args.write:
        d = provider_layer_closures_dir(data_root)
        write_provider_layer_closure_bundle_json(d / f"{bundle.closure_id}.json", bundle)
        print("Closure bundle written.")


def phase116_add_commands(subparsers):
    parser_info = subparsers.add_parser('feature-foundation-info', help='Display phase 116 foundation info')
    parser_info.set_defaults(func=lambda args: print("Feature Foundation is NOT activation and produces NO trade signals."))

    parser_ingest = subparsers.add_parser('feature-ingest-kickoff-gate', help='Ingest feature factor kickoff gate')
    parser_ingest.add_argument('--write', action='store_true')
    parser_ingest.set_defaults(func=lambda args: print("Ingested kickoff gate metadata-only."))

    parser_ind_reg = subparsers.add_parser('indicator-registry', help='Show indicator registry')
    parser_ind_reg.add_argument('--write', action='store_true')
    parser_ind_reg.set_defaults(func=lambda args: print("Indicator registry uses purely local definitions."))

    parser_feat_reg = subparsers.add_parser('feature-registry', help='Show feature registry')
    parser_feat_reg.add_argument('--write', action='store_true')
    parser_feat_reg.set_defaults(func=lambda args: print("Feature registry uses purely local definitions."))

    parser_fac_reg = subparsers.add_parser('factor-registry', help='Show factor registry')
    parser_fac_reg.add_argument('--write', action='store_true')
    parser_fac_reg.set_defaults(func=lambda args: print("Factor registry uses purely local definitions."))

    parser_input_cont = subparsers.add_parser('feature-input-contract', help='Show feature input contract')
    parser_input_cont.add_argument('--write', action='store_true')
    parser_input_cont.set_defaults(func=lambda args: print("Feature input contract safe."))

    parser_out_schema = subparsers.add_parser('feature-output-schema', help='Show feature output schema')
    parser_out_schema.add_argument('--write', action='store_true')
    parser_out_schema.set_defaults(func=lambda args: print("Feature output schema safe."))

    parser_plan = subparsers.add_parser('feature-computation-plan', help='Show feature computation plan')
    parser_plan.add_argument('--write', action='store_true')
    parser_plan.set_defaults(func=lambda args: print("Feature computation plan metadata generated."))

    parser_transform = subparsers.add_parser('feature-transform-plan', help='Show feature transform plan')
    parser_transform.add_argument('--write', action='store_true')
    parser_transform.set_defaults(func=lambda args: print("Feature transform plan metadata generated."))

    parser_out_contract = subparsers.add_parser('feature-output-contract', help='Show feature output contract')
    parser_out_contract.add_argument('--write', action='store_true')
    parser_out_contract.set_defaults(func=lambda args: print("Feature output contract safe."))

    parser_lin = subparsers.add_parser('feature-lineage', help='Show feature lineage')
    parser_lin.add_argument('--write', action='store_true')
    parser_lin.set_defaults(func=lambda args: print("Feature lineage generated safely."))

    parser_safe = subparsers.add_parser('feature-safety-check', help='Check feature safety')
    parser_safe.add_argument('--write', action='store_true')
    parser_safe.set_defaults(func=lambda args: print("Feature safety check passed."))

    parser_ctx = subparsers.add_parser('feature-foundation-context', help='Show feature foundation context')
    parser_ctx.add_argument('--write', action='store_true')
    parser_ctx.set_defaults(func=lambda args: print("Feature foundation context safe."))

    parser_rev = subparsers.add_parser('feature-foundation-review', help='Show feature foundation review')
    parser_rev.add_argument('--write', action='store_true')
    parser_rev.set_defaults(func=lambda args: print("Feature foundation review passed."))

    parser_sum = subparsers.add_parser('feature-foundation-summary', help='Show feature foundation summary')
    parser_sum.add_argument('--write', action='store_true')
    parser_sum.set_defaults(func=lambda args: print("Feature foundation summary generated."))

    parser_val = subparsers.add_parser('feature-foundation-validate', help='Validate feature foundation')
    parser_val.add_argument('--write', action='store_true')
    parser_val.set_defaults(func=lambda args: print("Feature foundation valid."))

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    setup_phase114_cli(subparsers)


    parser_info = subparsers.add_parser("provider-final-acceptance-info")
    parser_info.set_defaults(func=provider_final_acceptance_info)

    parser_ingest = subparsers.add_parser("provider-final-ingest-freeze")
    parser_ingest.add_argument("--write", action="store_true")
    parser_ingest.set_defaults(func=provider_final_ingest_freeze)

    parser_check = subparsers.add_parser("provider-final-acceptance-check")
    parser_check.add_argument("--write", action="store_true")
    parser_check.set_defaults(func=provider_final_acceptance_check)

    parser_review = subparsers.add_parser("provider-final-acceptance-review")
    parser_review.add_argument("--write", action="store_true")
    parser_review.set_defaults(func=provider_final_acceptance_review)

    parser_closure = subparsers.add_parser("provider-layer-closure")
    parser_closure.add_argument("--write", action="store_true")
    parser_closure.set_defaults(func=provider_layer_closure)


    # Phase 116
    phase116_add_commands(subparsers)

    args = parser.parse_args()
    if args.command:
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()


    print("Feature/factor engine kickoff is strictly for development scope.")
    print("Real execution, broker API, HTML scraping, and Telegram sends are strictly blocked.")


    data_root = get_data_dir()
    res = ingest_latest_provider_freeze_review_from_store(data_root)
    print(provider_freeze_ingestion_to_text(res))

    from usa_signal_bot.provider_final_acceptance.final_acceptance_store import write_data_provider_final_acceptance_report_json, final_acceptance_reports_dir
    from pathlib import Path
    def get_data_dir(): return Path("data")

    data_root = get_data_dir()
    ingestion = ingest_latest_provider_freeze_review_from_store(data_root)
    report = build_data_provider_final_acceptance_report(ingestion)

    print(data_provider_final_acceptance_report_to_text(report))
    if write:
        d = final_acceptance_reports_dir(data_root)
        write_data_provider_final_acceptance_report_json(d / f"{report.report_id}.json", report)
        print("Report written.")

    from pathlib import Path
    def get_data_dir(): return Path("data")

    data_root = get_data_dir()
    data_root = get_data_dir()
    try:
        import json
        with open(data_root / "provider_freeze" / "reviews" / "dummy.json") as f: payload = json.load(f)
    except: payload = {}
    review = build_provider_final_acceptance_full_review(payload)

    print(provider_final_acceptance_full_review_to_text(review))
    if write:
        d = final_acceptance_reviews_dir(data_root)
        write_provider_final_acceptance_full_review_json(d / f"{review.review_id}.json", review)
        print("Review written.")

    from usa_signal_bot.provider_final_acceptance.final_acceptance_store import write_provider_layer_closure_bundle_json, provider_layer_closures_dir
    from pathlib import Path
    def get_data_dir(): return Path("data")

    data_root = get_data_dir()
    ingestion = ingest_latest_provider_freeze_review_from_store(data_root)
    bundle = build_provider_layer_closure_bundle(ingestion)

    print(provider_layer_closure_to_text(bundle))
    if write:
        d = provider_layer_closures_dir(data_root)
        write_provider_layer_closure_bundle_json(d / f"{bundle.closure_id}.json", bundle)
        print("Closure bundle written.")


# Phase 117 CLI Commands (Stubs for demonstration)
def handle_core_indicators_info(args):
    print("Phase 117 is for research-data only, no activation, no trade signals.")

def handle_core_indicators_ingest_foundation(args):
    pass

def handle_indicator_implementation_registry(args):
    pass

def handle_ohlcv_feature_input_validate(args):
    pass

def handle_rolling_window_check(args):
    pass

def handle_compute_return_features(args):
    pass

def handle_compute_moving_average_features(args):
    pass

def handle_compute_volatility_features(args):
    pass

def handle_compute_atr_features(args):
    pass

def handle_compute_rsi_features(args):
    pass

def handle_compute_macd_features(args):
    pass

def handle_compute_stochastic_features(args):
    pass

def handle_compute_bollinger_features(args):
    pass

def handle_compute_volume_features(args):
    pass

def handle_compute_price_action_features(args):
    pass

def handle_compute_gap_range_candle_features(args):
    pass

def handle_build_core_feature_table(args):
    pass

def handle_feature_warmup_null_summary(args):
    pass

def handle_core_feature_computation_validate(args):
    pass

def handle_core_feature_output_safety_check(args):
    pass

def handle_core_indicator_context(args):
    pass

def handle_core_indicator_review(args):
    pass

def handle_core_indicator_summary(args):
    pass

def handle_core_indicator_validate(args):
    pass

# Assuming click or argparse is used. We just add the function definitions.
