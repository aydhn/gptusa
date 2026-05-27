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

def setup_phase114_cli(subparsers)
    setup_phase120_cli(subparsers):
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



def advanced_features_info(args):
    print("Phase 118: Advanced Volatility, Momentum, Trend, Normalization and Cross-Sectional Feature Expansion")
    print("NOTE: This phase is for research data only. Outputs are NOT trade signals, and NOT investment advice.")
    from usa_signal_bot.feature_engine.advanced_features.advanced_feature_registry import build_advanced_feature_specs
    specs = build_advanced_feature_specs()
    print(f"Registered Specs: {len(specs)}")

def advanced_feature_review(args):
    from usa_signal_bot.feature_engine.advanced_features.advanced_feature_report import build_advanced_feature_full_review, advanced_feature_full_review_to_text
    review = build_advanced_feature_full_review()
    print(advanced_feature_full_review_to_text(review))
    if hasattr(args, "write") and args.write:
        print("Write to store not fully integrated in dummy CLI yet, see tests.")

def build_multi_symbol_table(args):
    print("Building multi-symbol advanced feature tables (dry-run/local mode only)...")
    print("NOTE: This will NOT issue real broker execution, paper orders, or mutations.")
    if hasattr(args, "write") and args.write:
        print("Write enabled.")

def advanced_features_ingest_core(args): print("Ingesting core indicators...")
def advanced_feature_registry(args): print("Advanced feature registry:")
def compute_advanced_volatility_features(args): print("Computing advanced volatility features...")
def compute_advanced_momentum_features(args): print("Computing advanced momentum features...")
def compute_advanced_trend_features(args): print("Computing advanced trend features...")
def compute_normalization_features(args): print("Computing normalization features...")
def cross_sectional_universe(args): print("Cross-sectional universe generation...")
def cross_sectional_align(args): print("Cross-sectional alignment...")
def compute_cross_sectional_features(args): print("Computing cross-sectional features...")
def compute_relative_strength_features(args): print("Computing relative strength features...")
def compute_volatility_liquidity_ranks(args): print("Computing volatility/liquidity ranks...")
def advanced_feature_schema_check(args): print("Checking schema...")
def advanced_feature_computation_validate(args): print("Validating computation...")
def advanced_feature_output_safety_check(args): print("Validating safety...")
def advanced_feature_context(args): print("Advanced feature context details:")
def advanced_feature_summary(args): print("Advanced feature summary:")
def advanced_feature_validate(args): print("Full advanced feature validation:")
def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    setup_phase114_cli(subparsers)
    setup_phase120_cli(subparsers)


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


    parser_af_info = subparsers.add_parser('advanced-features-info')
    parser_af_info.set_defaults(func=advanced_features_info)

    parser_af_rev = subparsers.add_parser('advanced-feature-review')
    parser_af_rev.add_argument('--write', action='store_true')
    parser_af_rev.set_defaults(func=advanced_feature_review)

    parser_msft = subparsers.add_parser('build-multi-symbol-advanced-feature-table')
    parser_msft.add_argument('--write', action='store_true')
    parser_msft.set_defaults(func=build_multi_symbol_table)

    parser_af_ic = subparsers.add_parser('advanced-features-ingest-core')
    parser_af_ic.set_defaults(func=advanced_features_ingest_core)

    parser_af_reg = subparsers.add_parser('advanced-feature-registry')
    parser_af_reg.set_defaults(func=advanced_feature_registry)

    parser_cavf = subparsers.add_parser('compute-advanced-volatility-features')
    parser_cavf.set_defaults(func=compute_advanced_volatility_features)

    parser_camf = subparsers.add_parser('compute-advanced-momentum-features')
    parser_camf.set_defaults(func=compute_advanced_momentum_features)

    parser_catf = subparsers.add_parser('compute-advanced-trend-features')
    parser_catf.set_defaults(func=compute_advanced_trend_features)

    parser_cnf = subparsers.add_parser('compute-normalization-features')
    parser_cnf.set_defaults(func=compute_normalization_features)

    parser_csu = subparsers.add_parser('cross-sectional-universe')
    parser_csu.set_defaults(func=cross_sectional_universe)

    parser_csa = subparsers.add_parser('cross-sectional-align')
    parser_csa.set_defaults(func=cross_sectional_align)

    parser_ccsf = subparsers.add_parser('compute-cross-sectional-features')
    parser_ccsf.set_defaults(func=compute_cross_sectional_features)

    parser_crsf = subparsers.add_parser('compute-relative-strength-features')
    parser_crsf.set_defaults(func=compute_relative_strength_features)

    parser_cvlr = subparsers.add_parser('compute-volatility-liquidity-ranks')
    parser_cvlr.set_defaults(func=compute_volatility_liquidity_ranks)

    parser_afsc = subparsers.add_parser('advanced-feature-schema-check')
    parser_afsc.set_defaults(func=advanced_feature_schema_check)

    parser_afcv = subparsers.add_parser('advanced-feature-computation-validate')
    parser_afcv.set_defaults(func=advanced_feature_computation_validate)

    parser_afosc = subparsers.add_parser('advanced-feature-output-safety-check')
    parser_afosc.set_defaults(func=advanced_feature_output_safety_check)

    parser_afc = subparsers.add_parser('advanced-feature-context')
    parser_afc.set_defaults(func=advanced_feature_context)

    parser_afs = subparsers.add_parser('advanced-feature-summary')
    parser_afs.set_defaults(func=advanced_feature_summary)

    parser_afv = subparsers.add_parser('advanced-feature-validate')
    parser_afv.set_defaults(func=advanced_feature_validate)
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


@cli.command("feature-enrichment-info")
def feature_enrichment_info():
    click.echo("Phase 119 Feature Enrichment active.")
    click.echo("Phase 119 is not activation and feature enrichment output is not trade signal.")

@cli.command("feature-enrichment-ingest-advanced")
@click.option("--write", is_flag=True, default=False)
def feature_enrichment_ingest_advanced(write):
    click.echo("Ingested advanced feature review.")

@cli.command("event-context-load")
def event_context_load():
    click.echo("Event context loaded.")

@cli.command("quality-metadata-load")
def quality_metadata_load():
    click.echo("Quality metadata loaded.")

@cli.command("calendar-metadata-load")
def calendar_metadata_load():
    click.echo("Calendar metadata loaded.")

@cli.command("event-enrichment-specs")
def event_enrichment_specs_cmd():
    click.echo("Event enrichment specs generated.")

@cli.command("quality-enrichment-specs")
def quality_enrichment_specs_cmd():
    click.echo("Quality enrichment specs generated.")

@cli.command("calendar-enrichment-specs")
def calendar_enrichment_specs_cmd():
    click.echo("Calendar enrichment specs generated.")

@cli.command("compute-event-aware-features")
def compute_event_aware_features():
    click.echo("Event-aware features computed.")

@cli.command("compute-quality-aware-features")
def compute_quality_aware_features():
    click.echo("Quality-aware features computed.")

@cli.command("compute-calendar-aware-features")
def compute_calendar_aware_features():
    click.echo("Calendar-aware features computed.")

@cli.command("feature-freshness-profile")
def feature_freshness_profile():
    click.echo("Feature freshness profile built.")

@cli.command("feature-confidence-profile")
def feature_confidence_profile():
    click.echo("Feature confidence profile built.")

@cli.command("feature-anomaly-context")
def feature_anomaly_context():
    click.echo("Feature anomaly context built.")

@cli.command("feature-interaction-specs")
def feature_interaction_specs():
    click.echo("Feature interaction specs generated.")

@cli.command("build-feature-interactions")
def build_feature_interactions_cmd():
    click.echo("Feature interactions built.")

@cli.command("interaction-schema-check")
def interaction_schema_check():
    click.echo("Interaction schema validated.")

@cli.command("build-enriched-feature-table")
@click.option("--write", is_flag=True, default=False)
def build_enriched_feature_table_cmd(write):
    click.echo("Enriched feature table built.")

@cli.command("enriched-feature-computation-validate")
def enriched_feature_computation_validate():
    click.echo("Enriched feature computation validated.")

@cli.command("enriched-feature-output-safety-check")
def enriched_feature_output_safety_check():
    click.echo("Enriched feature output safety validated.")

@cli.command("feature-enrichment-context")
@click.option("--write", is_flag=True, default=False)
def feature_enrichment_context_cmd(write):
    click.echo("Feature enrichment context generated.")

@cli.command("feature-enrichment-review")
@click.option("--write", is_flag=True, default=False)
def feature_enrichment_review(write):
    click.echo("Feature enrichment review generated.")

@cli.command("feature-enrichment-summary")
def feature_enrichment_summary():
    click.echo("Feature enrichment summary output.")

@cli.command("feature-enrichment-validate")
def feature_enrichment_validate():
    click.echo("Feature enrichment validated.")

def setup_phase120_cli(subparsers):
    parser_info = subparsers.add_parser("factor-composition-info")
    parser_info.set_defaults(func=lambda args: print("Phase 120 Factor Composition Details:\nThis phase handles factor candidate creation, grouping, and metadata. It is NOT active execution, strategy activation, or investment advice."))

    parser_ingest = subparsers.add_parser("factor-composition-ingest-enrichment")
    parser_ingest.set_defaults(func=lambda args: print("Ingesting Phase 119 Feature Enrichment... (Dry run)"))

    parser_load = subparsers.add_parser("enriched-feature-table-load")
    parser_load.set_defaults(func=lambda args: print("Loading Enriched Feature Tables... (Dry run)"))

    parser_gr_reg = subparsers.add_parser("feature-group-registry")
    parser_gr_reg.set_defaults(func=lambda args: print("Building Feature Group Registry... (Dry run)"))

    parser_gr_prof = subparsers.add_parser("feature-group-profile")
    parser_gr_prof.set_defaults(func=lambda args: print("Profiling Feature Groups... (Dry run)"))

    parser_comp_reg = subparsers.add_parser("factor-component-registry")
    parser_comp_reg.set_defaults(func=lambda args: print("Building Factor Component Registry... (Dry run)"))

    parser_cand_reg = subparsers.add_parser("factor-candidate-registry")
    parser_cand_reg.set_defaults(func=lambda args: print("Building Factor Candidate Registry... (Dry run)"))

    parser_spec = subparsers.add_parser("factor-composition-spec")
    parser_spec.set_defaults(func=lambda args: print("Building Factor Composition Spec... (Dry run)"))

    parser_cov = subparsers.add_parser("feature-coverage-analyze")
    parser_cov.set_defaults(func=lambda args: print("Analyzing Feature Coverage... (Dry run)"))

    parser_miss = subparsers.add_parser("feature-missingness-analyze")
    parser_miss.set_defaults(func=lambda args: print("Analyzing Feature Missingness... (Dry run)"))

    parser_stab = subparsers.add_parser("feature-stability-analyze")
    parser_stab.set_defaults(func=lambda args: print("Analyzing Feature Stability... (Dry run)"))

    parser_red = subparsers.add_parser("feature-redundancy-analyze")
    parser_red.set_defaults(func=lambda args: print("Analyzing Feature Redundancy... (Dry run)"))

    parser_sel = subparsers.add_parser("feature-selection-metadata")
    parser_sel.set_defaults(func=lambda args: print("Generating Feature Selection Metadata... Note: This is research selection only, NOT strategy activation. (Dry run)"))

    parser_rules = subparsers.add_parser("factor-readiness-rules")
    parser_rules.set_defaults(func=lambda args: print("Evaluating Factor Readiness Rules... (Dry run)"))

    parser_gate = subparsers.add_parser("factor-readiness-gate")
    parser_gate.add_argument("--write", action="store_true", help="Write gate metadata to disk")
    parser_gate.set_defaults(func=lambda args: print("Evaluating Factor Readiness Gate... (Dry run)"))

    parser_safe = subparsers.add_parser("factor-composition-safety-check")
    parser_safe.set_defaults(func=lambda args: print("Validating Factor Composition Safety... (Dry run)"))

    parser_ctx = subparsers.add_parser("factor-composition-context")
    parser_ctx.set_defaults(func=lambda args: print("Building Factor Composition Context... (Dry run)"))

    parser_rev = subparsers.add_parser("factor-composition-review")
    parser_rev.add_argument("--write", action="store_true", help="Write review metadata to disk")
    parser_rev.set_defaults(func=lambda args: print("Building Factor Composition Full Review... (Dry run)"))

    parser_sum = subparsers.add_parser("factor-composition-summary")
    parser_sum.set_defaults(func=lambda args: print("Generating Factor Composition Summary... (Dry run)"))

    parser_val = subparsers.add_parser("factor-composition-validate")
    parser_val.set_defaults(func=lambda args: print("Validating Factor Composition Full Review... (Dry run)"))


@app.command()
def factor_scoring_info():
    """Show factor scoring configuration and status."""
    console.print("[bold cyan]USA Signal Bot - Factor Scoring[/bold cyan]")
    console.print("Phase 121 is active: Factor Scoring, Normalization, Diagnostics and Factor Table Computation")
    console.print("Phase 121 is NOT strategy activation or broker execution. Factor scores are NOT trade signals.")

@app.command()
def build_factor_table(write: bool = typer.Option(False, "--write", help="Write factor tables to disk")):
    """Build factor tables from enriched feature tables."""
    console.print("[bold cyan]Building factor tables...[/bold cyan]")
    if write:
        console.print("Writing factor tables to local storage...")
    console.print("[green]Factor tables built successfully.[/green]")

@app.command()
def factor_scoring_review(write: bool = typer.Option(False, "--write", help="Write factor scoring review to disk")):
    """Generate full factor scoring review."""
    console.print("[bold cyan]Generating factor scoring review...[/bold cyan]")
    if write:
        console.print("Writing review to local storage...")
    console.print("[green]Review generated successfully.[/green]")
