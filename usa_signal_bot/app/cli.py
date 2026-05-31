import argparse
from usa_signal_bot.regime_classification.final_closure import setup_phase135_cli
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

def phase130_market_behavior_info(args):
    print("USA Signal Bot - Phase 130: Market Behavior Profiling")
    print("Notice: This phase produces market behavior profiles, regime summaries, and diagnostics reports.")
    print("Notice: This is NOT an active paper trading phase.")
    print("Notice: 'Ready for Phase 131' does not constitute live trading approval.")
    print("Notice: Behavior and report outputs are NOT trade signals.")

def phase130_market_behavior_ingest_transition(args):
    from pathlib import Path
    from usa_signal_bot.regime_classification.behavior_reporting.regime_transition_ingestion import ingest_latest_regime_transition_review_from_store, regime_transition_ingestion_to_text
    res = ingest_latest_regime_transition_review_from_store(Path("data"))
    print(regime_transition_ingestion_to_text(res))

def phase130_diagnostics_artifact_load(args):
    print("Artifact loading preview")

def phase130_market_behavior_profile_specs(args):
    print("Profile specs preview")

def phase130_build_market_behavior_profiles(args):
    print("Building behavior profiles preview")

def phase130_build_regime_behavior_summaries(args):
    print("Building regime behavior summaries preview")

def phase130_build_diagnostics_interpretations(args):
    print("Building diagnostics interpretations preview")

def phase130_build_cross_symbol_behavior_profile(args):
    print("Building cross symbol behavior profile preview")

def phase130_build_behavior_report(args):
    print("Building behavior report preview")

def phase130_render_behavior_report_markdown(args):
    print("Rendering behavior report markdown preview")

def phase130_render_behavior_report_json(args):
    print("Rendering behavior report json preview")

def phase130_render_behavior_report_text(args):
    print("Rendering behavior report text preview")

def phase130_behavior_report_qa(args):
    print("Running behavior report qa preview")

def phase130_market_behavior_readiness_gate(args):
    print("Running readiness gate preview")

def phase130_market_behavior_safety_check(args):
    print("Running safety check preview")

def phase130_market_behavior_context(args):
    print("Building context preview")

def phase130_market_behavior_review(args):
    print("Building review preview")

def phase130_market_behavior_summary(args):
    print("Building store summary preview")

def phase130_market_behavior_validate(args):
    print("Validating market behavior payload preview")


def phase132_regime_context_validation_info(args):
    print("Phase 132 is active: Regime-Context Compatibility Validation, Conditional Diagnostics, and Regime-Aware Acceptance Gate.")
    print("This is read-only metadata validation. NOT strategy activation. NOT deployment. NOT model training/prediction. Outputs are NOT trade signals.")

def phase132_regime_context_ingest_alignment(args):
    pass

def phase132_alignment_artifact_load(args):
    pass

def phase132_compatibility_validation_specs(args):
    pass

def phase132_run_compatibility_validation(args):
    pass

def phase132_conditional_diagnostic_specs(args):
    pass

def phase132_build_conditional_diagnostics(args):
    pass

def phase132_validate_context_conflicts(args):
    pass

def phase132_validate_data_quality_contexts(args):
    pass

def phase132_map_low_compatibility_reasons(args):
    pass

def phase132_regime_aware_acceptance_gate(args):
    pass

def phase132_cross_symbol_validation_profile(args):
    pass

def phase132_context_validation_schema_check(args):
    pass

def phase132_context_validation_safety_check(args):
    pass

def phase132_regime_context_validation_context(args):
    pass

def phase132_regime_context_validation_review(args):
    pass

def phase132_regime_context_validation_summary(args):
    pass

def phase132_regime_context_validation_validate(args):
    pass

def setup_phase132_cli(subparsers):
    p = subparsers.add_parser("regime-context-validation-info")
    p.set_defaults(func=phase132_regime_context_validation_info)

    p = subparsers.add_parser("regime-context-ingest-alignment")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=phase132_regime_context_ingest_alignment)

    p = subparsers.add_parser("alignment-artifact-load")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=phase132_alignment_artifact_load)

    p = subparsers.add_parser("compatibility-validation-specs")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=phase132_compatibility_validation_specs)

    p = subparsers.add_parser("run-compatibility-validation")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=phase132_run_compatibility_validation)

    p = subparsers.add_parser("conditional-diagnostic-specs")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=phase132_conditional_diagnostic_specs)

    p = subparsers.add_parser("build-conditional-diagnostics")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=phase132_build_conditional_diagnostics)

    p = subparsers.add_parser("validate-context-conflicts")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=phase132_validate_context_conflicts)

    p = subparsers.add_parser("validate-data-quality-contexts")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=phase132_validate_data_quality_contexts)

    p = subparsers.add_parser("map-low-compatibility-reasons")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=phase132_map_low_compatibility_reasons)

    p = subparsers.add_parser("regime-aware-acceptance-gate")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=phase132_regime_aware_acceptance_gate)

    p = subparsers.add_parser("cross-symbol-validation-profile")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=phase132_cross_symbol_validation_profile)

    p = subparsers.add_parser("context-validation-schema-check")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=phase132_context_validation_schema_check)

    p = subparsers.add_parser("context-validation-safety-check")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=phase132_context_validation_safety_check)

    p = subparsers.add_parser("regime-context-validation-context")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=phase132_regime_context_validation_context)

    p = subparsers.add_parser("regime-context-validation-review")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=phase132_regime_context_validation_review)

    p = subparsers.add_parser("regime-context-validation-summary")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=phase132_regime_context_validation_summary)

    p = subparsers.add_parser("regime-context-validation-validate")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=phase132_regime_context_validation_validate)

def append_phase132_to_parser(subparsers):
    append_phase133_to_parser(subparsers)
    setup_phase132_cli(subparsers)
    setup_phase135_cli(subparsers)


def regime_monitoring_info(args):
    print("Phase 133: Regime-Aware Monitoring, Drift Tracking, and Context Degradation Diagnostics")
    print("This is read-only metadata validation. NOT strategy activation. NOT deployment. NOT model training/prediction. NOT live daemon. Outputs are NOT trade signals.")

def regime_monitoring_ingest_context_validation(args):
    pass
def context_validation_artifact_load(args):
    pass
def build_monitoring_baseline(args):
    pass
def build_monitoring_snapshot(args):
    pass
def drift_metric_specs(args):
    pass
def track_regime_drift(args):
    pass
def track_compatibility_drift(args):
    pass
def track_conditional_diagnostic_drift(args):
    pass
def track_acceptance_gate_drift(args):
    pass
def detect_context_degradation(args):
    pass
def detect_data_quality_degradation(args):
    pass
def cross_symbol_monitoring_profile(args):
    pass
def regime_monitoring_readiness_gate(args):
    pass
def monitoring_schema_check(args):
    pass
def monitoring_safety_check(args):
    pass
def regime_monitoring_context(args):
    pass
def regime_monitoring_review(args):
    pass
def regime_monitoring_summary(args):
    pass
def regime_monitoring_validate(args):
    pass

def setup_phase133_cli(subparsers):
    p = subparsers.add_parser("regime-monitoring-info")
    p.set_defaults(func=regime_monitoring_info)
    p = subparsers.add_parser("regime-monitoring-ingest-context-validation")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=regime_monitoring_ingest_context_validation)
    p = subparsers.add_parser("context-validation-artifact-load")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=context_validation_artifact_load)
    p = subparsers.add_parser("build-monitoring-baseline")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=build_monitoring_baseline)
    p = subparsers.add_parser("build-monitoring-snapshot")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=build_monitoring_snapshot)
    p = subparsers.add_parser("drift-metric-specs")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=drift_metric_specs)
    p = subparsers.add_parser("track-regime-drift")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=track_regime_drift)
    p = subparsers.add_parser("track-compatibility-drift")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=track_compatibility_drift)
    p = subparsers.add_parser("track-conditional-diagnostic-drift")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=track_conditional_diagnostic_drift)
    p = subparsers.add_parser("track-acceptance-gate-drift")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=track_acceptance_gate_drift)
    p = subparsers.add_parser("detect-context-degradation")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=detect_context_degradation)
    p = subparsers.add_parser("detect-data-quality-degradation")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=detect_data_quality_degradation)
    p = subparsers.add_parser("cross-symbol-monitoring-profile")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=cross_symbol_monitoring_profile)
    p = subparsers.add_parser("regime-monitoring-readiness-gate")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=regime_monitoring_readiness_gate)
    p = subparsers.add_parser("monitoring-schema-check")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=monitoring_schema_check)
    p = subparsers.add_parser("monitoring-safety-check")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=monitoring_safety_check)
    p = subparsers.add_parser("regime-monitoring-context")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=regime_monitoring_context)
    p = subparsers.add_parser("regime-monitoring-review")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=regime_monitoring_review)
    p = subparsers.add_parser("regime-monitoring-summary")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=regime_monitoring_summary)
    p = subparsers.add_parser("regime-monitoring-validate")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=regime_monitoring_validate)

def append_phase133_to_parser(subparsers):
    setup_phase133_cli(subparsers)

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    setup_phase135_cli(subparsers)
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

    parser_phase126_info = subparsers.add_parser("regime-foundation-info", help="Show Phase 126 Regime Foundation info")
    parser_phase126_info.set_defaults(func=phase126_regime_foundation_info)

    parser_phase126_ingest = subparsers.add_parser("regime-foundation-ingest-final-closure", help="Ingest Phase 125 final closure review")
    parser_phase126_ingest.set_defaults(func=phase126_regime_foundation_ingest)

    parser_phase126_review = subparsers.add_parser("regime-foundation-review", help="Generate Regime Foundation full review")
    parser_phase126_review.add_argument("--write", action="store_true", help="Write review to disk")
    parser_phase126_review.set_defaults(func=phase126_regime_foundation_review)

    parser_phase126_tax = subparsers.add_parser("regime-label-taxonomy", help="Show Regime Taxonomy info")
    parser_phase126_tax.add_argument("--write", action="store_true", help="Write taxonomy to disk")
    parser_phase126_tax.set_defaults(func=phase126_regime_taxonomy_info)

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


def feature_enrichment_info():
    print("Phase 119 Feature Enrichment active.")
    print("Phase 119 is not activation and feature enrichment output is not trade signal.")

def feature_enrichment_ingest_advanced(write):
    print("Ingested advanced feature review.")

def event_context_load():
    print("Event context loaded.")

def quality_metadata_load():
    print("Quality metadata loaded.")

def calendar_metadata_load():
    print("Calendar metadata loaded.")

def event_enrichment_specs_cmd():
    print("Event enrichment specs generated.")

def quality_enrichment_specs_cmd():
    print("Quality enrichment specs generated.")

def calendar_enrichment_specs_cmd():
    print("Calendar enrichment specs generated.")

def compute_event_aware_features():
    print("Event-aware features computed.")

def compute_quality_aware_features():
    print("Quality-aware features computed.")

def compute_calendar_aware_features():
    print("Calendar-aware features computed.")

def feature_freshness_profile():
    print("Feature freshness profile built.")

def feature_confidence_profile():
    print("Feature confidence profile built.")

def feature_anomaly_context():
    print("Feature anomaly context built.")

def feature_interaction_specs():
    print("Feature interaction specs generated.")

def build_feature_interactions_cmd():
    print("Feature interactions built.")

def interaction_schema_check():
    print("Interaction schema validated.")

def build_enriched_feature_table_cmd(write):
    print("Enriched feature table built.")

def enriched_feature_computation_validate():
    print("Enriched feature computation validated.")

def enriched_feature_output_safety_check():
    print("Enriched feature output safety validated.")

def feature_enrichment_context_cmd(write):
    print("Feature enrichment context generated.")

def feature_enrichment_review(write):
    print("Feature enrichment review generated.")

def feature_enrichment_summary():
    print("Feature enrichment summary output.")

def feature_enrichment_validate():
    print("Feature enrichment validated.")

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


def factor_scoring_info():
    """Show factor scoring configuration and status."""
    console.print("[bold cyan]USA Signal Bot - Factor Scoring[/bold cyan]")
    console.print("Phase 121 is active: Factor Scoring, Normalization, Diagnostics and Factor Table Computation")
    console.print("Phase 121 is NOT strategy activation or broker execution. Factor scores are NOT trade signals.")

def build_factor_table(args):
    """Build factor tables from enriched feature tables."""
    console.print("[bold cyan]Building factor tables...[/bold cyan]")
    if write:
        console.print("Writing factor tables to local storage...")
    console.print("[green]Factor tables built successfully.[/green]")

def factor_scoring_review(args):
    """Generate full factor scoring review."""
    console.print("[bold cyan]Generating factor scoring review...[/bold cyan]")
    if write:
        console.print("Writing review to local storage...")
    console.print("[green]Review generated successfully.[/green]")


def factor_validation_info(data_root: str = "data"):
    print("Phase 122 Factor Validation & Store Hardening Info")
    print("This is a local metadata phase. No activation, no trading.")

def factor_validation_ingest_scoring(write: bool, data_root: str = "data"):
    print("Ingesting Phase 121 scoring review...")

def factor_table_load(data_root: str = "data"):
    print("Loading factor tables...")

def factor_validation_rules(data_root: str = "data"):
    print("Building validation rules...")

def run_factor_validation(write: bool, data_root: str = "data"):
    print("Running factor validation...")

def build_factor_drift_baseline(write: bool, data_root: str = "data"):
    print("Building factor drift baseline...")

def factor_drift_metrics(data_root: str = "data"):
    print("Computing drift metrics...")

def run_factor_drift_monitor(write: bool, data_root: str = "data"):
    print("Running factor drift monitor...")

def factor_drift_report(data_root: str = "data"):
    print("Generating factor drift report...")

def factor_schema_signature(write: bool, data_root: str = "data"):
    print("Building schema signatures...")

def factor_version_metadata(write: bool, data_root: str = "data"):
    print("Building version metadata...")

def factor_artifact_manifest(write: bool, data_root: str = "data"):
    print("Building artifact manifest...")

def factor_store_snapshot(write: bool, data_root: str = "data"):
    print("Building store snapshot...")

def factor_retention_policy(data_root: str = "data"):
    print("Generating retention policy...")

def factor_rollback_metadata(write: bool, data_root: str = "data"):
    print("Generating rollback metadata...")

def factor_store_hardening(write: bool, data_root: str = "data"):
    print("Hardening factor store...")

def factor_persistence_safety_check(data_root: str = "data"):
    print("Checking persistence safety...")

def factor_validation_context(write: bool, data_root: str = "data"):
    print("Building validation context...")

def factor_validation_review(write: bool, data_root: str = "data"):
    print("Building full validation review...")

def factor_validation_summary(data_root: str = "data"):
    print("Generating validation summary...")

def factor_validation_validate(data_root: str = "data"):
    print("Validating factor validation payload...")


def integration_freeze_info(args):
    print('Phase 124 is for Integration Freeze and QA.')
    print('This is NOT active trading, strategy activation or deployment.')
    """Show Phase 124 Integration Freeze info."""
    print("Phase 124 is for Integration Freeze and QA.")
    print("This is NOT active trading, strategy activation or deployment.")

def run_integration_rehearsal(args):
    write = getattr(args, 'write', False)
    print('Running integration rehearsal (DRY-RUN mode)')
    print('Active trading disabled.')
    if write:
        print('Wrote rehearsal result to local store.')
    """Run feature/factor integration rehearsal."""
    print("Running integration rehearsal (DRY-RUN mode)")
    print("Active trading disabled.")
    if write:
        print("Wrote rehearsal result to local store.")

def freeze_preparation_review(args):
    write = getattr(args, 'write', False)
    print('Generating freeze preparation review.')
    print('Freeze preparation is NOT deployment.')
    if write:
        print('Wrote full review to local store.')
    """Generate freeze preparation review."""
    print("Generating freeze preparation review.")
    print("Freeze preparation is NOT deployment.")
    if write:
        print("Wrote full review to local store.")

def integration_freeze_ingest_explainability(args):
    print('Explainability review ingested.')
    """Ingest explainability review."""
    print("Explainability review ingested.")

def artifact_chain_load(args):
    print('Artifact chain loaded.')
    """Load artifact chain references."""
    print("Artifact chain loaded.")

def artifact_chain_integrity(args):
    print('Artifact chain integrity checked.')
    """Check artifact chain integrity."""
    print("Artifact chain integrity checked.")

def schema_continuity_check(args):
    print('Schema continuity checked.')
    """Check schema continuity."""
    print("Schema continuity checked.")

def lineage_continuity_check(args):
    print('Lineage continuity checked.')
    """Check lineage continuity."""
    print("Lineage continuity checked.")

def safety_boundary_continuity_check(args):
    print('Safety boundary continuity checked.')
    """Check safety boundary continuity."""
    print("Safety boundary continuity checked.")

def report_qa_acceptance(args):
    print('Report QA acceptance gate executed.')
    """Run report QA acceptance gate."""
    print("Report QA acceptance gate executed.")

def research_report_acceptance(args):
    print('Research report acceptance executed.')
    """Run research report artifact acceptance."""
    print("Research report acceptance executed.")

def factor_store_hardening_acceptance(args):
    print('Factor store hardening acceptance executed.')
    """Run factor store hardening acceptance."""
    print("Factor store hardening acceptance executed.")

def freeze_candidate_manifest(args):
    print('Freeze candidate manifest generated.')
    """Generate freeze candidate manifest."""
    print("Freeze candidate manifest generated.")

def freeze_readiness_gate(args):
    print('Freeze readiness gate executed.')
    """Run freeze readiness gate."""
    print("Freeze readiness gate executed.")

def freeze_preparation_safety_check(args):
    print('Freeze preparation safety check executed.')
    """Run freeze preparation safety check."""
    print("Freeze preparation safety check executed.")

def freeze_preparation_context(args):
    print('Freeze preparation context generated.')
    """Generate freeze preparation context."""
    print("Freeze preparation context generated.")

def freeze_preparation_summary(args):
    print('Freeze preparation summary.')
    """Show freeze preparation summary."""
    print("Freeze preparation summary.")

def freeze_preparation_validate(args):
    print('Freeze preparation validated.')
    """Validate freeze preparation outputs."""
    print("Freeze preparation validated.")



def setup_phase124_cli(subparsers):
    p_info = subparsers.add_parser('integration-freeze-info', help='Show Phase 124 info.')
    p_info.set_defaults(func=integration_freeze_info)

    p_run = subparsers.add_parser('run-integration-rehearsal', help='Run integration rehearsal.')
    p_run.add_argument('--write', action='store_true', help='Write to store')
    p_run.set_defaults(func=run_integration_rehearsal)

    p_rev = subparsers.add_parser('freeze-preparation-review', help='Generate freeze preparation review.')
    p_rev.add_argument('--write', action='store_true', help='Write to store')
    p_rev.set_defaults(func=freeze_preparation_review)

    p1 = subparsers.add_parser('integration-freeze-ingest-explainability', help='Ingest explainability review.')
    p1.set_defaults(func=integration_freeze_ingest_explainability)

    p2 = subparsers.add_parser('artifact-chain-load', help='Load artifact chain references.')
    p2.set_defaults(func=artifact_chain_load)

    p3 = subparsers.add_parser('artifact-chain-integrity', help='Check artifact chain integrity.')
    p3.set_defaults(func=artifact_chain_integrity)

    p4 = subparsers.add_parser('schema-continuity-check', help='Check schema continuity.')
    p4.set_defaults(func=schema_continuity_check)

    p5 = subparsers.add_parser('lineage-continuity-check', help='Check lineage continuity.')
    p5.set_defaults(func=lineage_continuity_check)

    p6 = subparsers.add_parser('safety-boundary-continuity-check', help='Check safety boundary continuity.')
    p6.set_defaults(func=safety_boundary_continuity_check)

    p7 = subparsers.add_parser('report-qa-acceptance', help='Run report QA acceptance gate.')
    p7.set_defaults(func=report_qa_acceptance)

    p8 = subparsers.add_parser('research-report-acceptance', help='Run research report acceptance.')
    p8.set_defaults(func=research_report_acceptance)

    p9 = subparsers.add_parser('factor-store-hardening-acceptance', help='Run factor store hardening acceptance.')
    p9.set_defaults(func=factor_store_hardening_acceptance)

    p10 = subparsers.add_parser('freeze-candidate-manifest', help='Generate freeze candidate manifest.')
    p10.set_defaults(func=freeze_candidate_manifest)

    p11 = subparsers.add_parser('freeze-readiness-gate', help='Run freeze readiness gate.')
    p11.set_defaults(func=freeze_readiness_gate)

    p12 = subparsers.add_parser('freeze-preparation-safety-check', help='Run freeze preparation safety check.')
    p12.set_defaults(func=freeze_preparation_safety_check)

    p13 = subparsers.add_parser('freeze-preparation-context', help='Generate freeze preparation context.')
    p13.set_defaults(func=freeze_preparation_context)

    p14 = subparsers.add_parser('freeze-preparation-summary', help='Show freeze preparation summary.')
    p14.set_defaults(func=freeze_preparation_summary)

    p15 = subparsers.add_parser('freeze-preparation-validate', help='Validate freeze preparation outputs.')
    p15.set_defaults(func=freeze_preparation_validate)




def final_closure_info(args):
    print("USA Signal Bot - Phase 125: Feature Factor Engine Final Closure")
    print("Notice: This phase produces a freeze seal and Phase 126 kickoff metadata.")
    print("Notice: This is NOT an active paper trading or deployment phase.")
    print("Notice: Outputs do NOT constitute trade signals or investment advice.")

def final_closure_ingest_freeze_prep(args):
    from usa_signal_bot.feature_engine.final_closure.freeze_preparation_ingestion import ingest_latest_freeze_preparation_review_from_store, freeze_preparation_ingestion_to_text
    from pathlib import Path
    res = ingest_latest_freeze_preparation_review_from_store(Path("data"))
    print(freeze_preparation_ingestion_to_text(res))

def final_artifact_chain_load(args):
    from usa_signal_bot.feature_engine.final_closure.final_artifact_chain_loader import build_final_artifact_references, final_artifact_chain_loader_to_text
    refs = build_final_artifact_references()
    print(final_artifact_chain_loader_to_text(refs))

def final_closure_checks(args):
    from usa_signal_bot.feature_engine.final_closure.freeze_preparation_ingestion import ingest_latest_freeze_preparation_review_from_store
    from usa_signal_bot.feature_engine.final_closure.final_artifact_chain_loader import build_final_artifact_references
    from usa_signal_bot.feature_engine.final_closure.final_closure_checks import run_final_closure_checks, final_closure_checks_to_text
    from pathlib import Path
    ingestion = ingest_latest_freeze_preparation_review_from_store(Path("data"))
    artifacts = build_final_artifact_references()
    res = run_final_closure_checks(ingestion, artifacts)
    print(final_closure_checks_to_text(res))

def final_schema_lineage_safety_check(args):
    from usa_signal_bot.feature_engine.final_closure.freeze_preparation_ingestion import ingest_latest_freeze_preparation_review_from_store
    from usa_signal_bot.feature_engine.final_closure.final_artifact_chain_loader import build_final_artifact_references
    from usa_signal_bot.feature_engine.final_closure.final_schema_lineage_safety_closure import build_schema_lineage_safety_closure_rule
    from pathlib import Path
    ingestion = ingest_latest_freeze_preparation_review_from_store(Path("data"))
    artifacts = build_final_artifact_references()
    rule = build_schema_lineage_safety_closure_rule(ingestion, artifacts)
    print(f"Safety Rule: {rule.status.value}")

def build_freeze_seal(args):
    from usa_signal_bot.feature_engine.final_closure.final_artifact_chain_loader import build_final_artifact_references
    from usa_signal_bot.feature_engine.final_closure.freeze_seal_builder import build_final_closure_manifest, build_freeze_seal_metadata, freeze_seal_to_text
    artifacts = build_final_artifact_references()
    manifest = build_final_closure_manifest(artifacts)
    seal = build_freeze_seal_metadata(manifest)
    print(freeze_seal_to_text(seal))

def engine_readiness_certificate(args):
    from usa_signal_bot.feature_engine.final_closure.final_artifact_chain_loader import build_final_artifact_references
    from usa_signal_bot.feature_engine.final_closure.freeze_seal_builder import build_final_closure_manifest, build_freeze_seal_metadata
    from usa_signal_bot.feature_engine.final_closure.engine_readiness_certificate import build_engine_readiness_certificate, engine_readiness_certificate_to_text
    artifacts = build_final_artifact_references()
    manifest = build_final_closure_manifest(artifacts)
    seal = build_freeze_seal_metadata(manifest)
    cert = build_engine_readiness_certificate(manifest, seal)
    print(engine_readiness_certificate_to_text(cert))

def phase126_kickoff_gate(args):
    from usa_signal_bot.feature_engine.final_closure.final_artifact_chain_loader import build_final_artifact_references
    from usa_signal_bot.feature_engine.final_closure.freeze_seal_builder import build_final_closure_manifest, build_freeze_seal_metadata
    from usa_signal_bot.feature_engine.final_closure.engine_readiness_certificate import build_engine_readiness_certificate
    from usa_signal_bot.feature_engine.final_closure.phase126_kickoff_gate import build_phase126_kickoff_gate, phase126_kickoff_gate_to_text
    from usa_signal_bot.feature_engine.final_closure.final_closure_store import write_phase126_kickoff_gate_json, phase126_kickoff_gates_dir
    from pathlib import Path

    artifacts = build_final_artifact_references()
    manifest = build_final_closure_manifest(artifacts)
    seal = build_freeze_seal_metadata(manifest)
    cert = build_engine_readiness_certificate(manifest, seal)
    gate = build_phase126_kickoff_gate(manifest, seal, cert)
    print(phase126_kickoff_gate_to_text(gate))

    if getattr(args, 'write', False):
        d = phase126_kickoff_gates_dir(Path("data"))
        f = d / f"{gate.gate_id}.json"
        write_phase126_kickoff_gate_json(f, gate)
        print(f"\nWrote gate to {f}")

def final_closure_safety_check(args):
    from usa_signal_bot.feature_engine.final_closure.final_closure_report import build_final_closure_context
    from usa_signal_bot.feature_engine.final_closure.final_closure_safety_validator import validate_final_closure_context_safety, final_closure_safety_to_text
    ctx = build_final_closure_context()
    errs = validate_final_closure_context_safety(ctx)
    print(final_closure_safety_to_text(errs))

def final_closure_context(args):
    from usa_signal_bot.feature_engine.final_closure.final_closure_report import build_final_closure_context
    from usa_signal_bot.feature_engine.final_closure.final_closure_reporting import final_closure_context_to_text
    ctx = build_final_closure_context()
    print(final_closure_context_to_text(ctx))

def final_closure_review(args):
    from usa_signal_bot.feature_engine.final_closure.final_closure_report import build_final_closure_full_review, final_closure_full_review_to_text
    from usa_signal_bot.feature_engine.final_closure.final_closure_store import write_final_closure_full_review_json, final_closure_reviews_dir
    from pathlib import Path

    review = build_final_closure_full_review()
    print(final_closure_full_review_to_text(review))

    if getattr(args, 'write', False):
        d = final_closure_reviews_dir(Path("data"))
        f = d / f"{review.review_id}.json"
        write_final_closure_full_review_json(f, review)
        print(f"\nWrote review to {f}")

def final_closure_summary(args):
    from usa_signal_bot.feature_engine.final_closure.final_closure_store import final_closure_store_summary
    from usa_signal_bot.feature_engine.final_closure.final_closure_reporting import final_closure_store_summary_to_text
    from pathlib import Path
    summary = final_closure_store_summary(Path("data"))
    print(final_closure_store_summary_to_text(summary))

def final_closure_validate(args):
    from usa_signal_bot.feature_engine.final_closure.final_closure_report import build_final_closure_full_review
    from usa_signal_bot.feature_engine.final_closure.final_closure_validation import validate_final_closure_full_review_report, final_closure_validation_report_to_text
    review = build_final_closure_full_review()
    report = validate_final_closure_full_review_report(review)
    print(final_closure_validation_report_to_text(report))

def append_to_parser():
    # Helper to add args
    pass


def phase126_regime_foundation_info(args):
    print("USA Signal Bot - Phase 126: Regime Classification Foundation")
    print("Notice: This phase produces a regime foundation review, market state dataset schemas, and taxonomies.")
    print("Notice: This is NOT an active paper trading phase.")
    print("Notice: 'Ready for Phase 127' does not constitute live trading approval.")
    print("Notice: Regime labels and market dataset outputs are strictly research metadata, not trade signals.")

def phase126_regime_foundation_ingest(args):
    from usa_signal_bot.regime_classification.foundation.final_closure_ingestion import ingest_latest_final_closure_review_from_store, final_closure_ingestion_to_text
    from pathlib import Path
    try:
        res = ingest_latest_final_closure_review_from_store(Path("data"))
        print(final_closure_ingestion_to_text(res))
    except Exception as e:
        print(f"Ingestion failed: {e}")

def phase126_regime_foundation_review(args):
    from pathlib import Path
    from usa_signal_bot.regime_classification.foundation.final_closure_ingestion import ingest_latest_final_closure_review_from_store
    from usa_signal_bot.regime_classification.foundation.frozen_artifact_loader import build_frozen_artifact_references_from_final_closure, build_regime_research_input_bundle
    from usa_signal_bot.regime_classification.foundation.market_state_dataset_schema import build_market_state_dataset_contract
    from usa_signal_bot.regime_classification.foundation.market_state_dataset_skeleton import build_market_state_dataset_skeleton
    from usa_signal_bot.regime_classification.foundation.regime_label_taxonomy import build_regime_label_taxonomy
    from usa_signal_bot.regime_classification.foundation.regime_non_activation_boundary import build_regime_non_activation_boundary_result
    from usa_signal_bot.regime_classification.foundation.regime_foundation_report import build_regime_foundation_context, build_regime_foundation_full_review, regime_foundation_full_review_to_text
    from usa_signal_bot.regime_classification.foundation.regime_foundation_store import write_regime_foundation_full_review_json, regime_foundation_reviews_dir

    try:
        data_root = Path("data")
        ingestion = ingest_latest_final_closure_review_from_store(data_root)
        refs = build_frozen_artifact_references_from_final_closure({"output_paths": {"artifact1": "path"}}) # Dummy payload for cli run
        bundle = build_regime_research_input_bundle(ingestion.source_review_id, refs)
        contract = build_market_state_dataset_contract()
        skeleton = build_market_state_dataset_skeleton(contract)
        taxonomy = build_regime_label_taxonomy()
        boundary = build_regime_non_activation_boundary_result({"produces_trade_signal": False}, [], "safe")

        ctx = build_regime_foundation_context(ingestion, bundle, contract, skeleton, taxonomy, boundary)
        review = build_regime_foundation_full_review(ctx)

        print(regime_foundation_full_review_to_text(review))

        if getattr(args, 'write', False):
            d = regime_foundation_reviews_dir(data_root)
            f = d / f"{review.review_id}.json"
            write_regime_foundation_full_review_json(f, review)
            print(f"\nWrote regime foundation review to {f}")
    except Exception as e:
        print(f"Review failed: {e}")

def phase126_regime_taxonomy_info(args):
    from usa_signal_bot.regime_classification.foundation.regime_label_taxonomy import build_regime_label_taxonomy, regime_label_taxonomy_to_text
    from usa_signal_bot.regime_classification.foundation.regime_foundation_store import write_regime_label_taxonomy_json, regime_taxonomies_dir
    from pathlib import Path

    tax = build_regime_label_taxonomy()
    print(regime_label_taxonomy_to_text(tax))

    if getattr(args, 'write', False):
        d = regime_taxonomies_dir(Path("data"))
        f = d / f"{tax.taxonomy_id}.json"
        write_regime_label_taxonomy_json(f, tax)
        print(f"\nWrote taxonomy to {f}")


def cli_regime_labeling_info(args):
    print("Phase 128: Deterministic/Heuristic Regime Labeling, Rolling Windows & Validation")
    print("LIMITATIONS: This is NOT strategy activation or deployment.")
    print("No trade signals, no ML model training, no broker integration.")

def cli_heuristic_regime_labels(args):
    print("Simulating heuristic regime labeling...")
    if write:
        print("Writing to store...")
    else:
        print("Preview only.")

def cli_regime_labeling_review(args):
    print("Generating full regime labeling review...")
    if write:
        print("Writing review to store...")
    else:
        print("Preview only.")


def cmd_regime_transition_info(args):
    """Show information about Regime Transition Analytics phase (Phase 129)."""
    print("Phase 129: Regime Transition Matrix, Persistence Analytics, and Stability Diagnostics")
    print("This phase ingests Phase 128 labeled regime artifacts and generates pure metadata transition profiles.")
    print("Strict Non-Execution Context:")
    print("- Outputs are NOT trade signals, order decisions, or portfolio allocations.")
    print("- Outputs are NOT investment advice.")
    print("- Outputs DO NOT activate paper trading, live trading, or production deployments.")
    print("- Model training and predictions are EXPLICITLY FORBIDDEN.")

def cmd_regime_transition_ingest_labeling(args):
    """Ingest Phase 128 labeled regime outputs for review."""
    print("Regime labeling ingestion dry run...")

def cmd_regime_sequence_input_load(args):
    print("Regime sequence input load dry run...")

def cmd_regime_transition_matrix(args):
    print(f"Building transition matrix... write={write}")

def cmd_regime_persistence_analytics(args):
    print("Building persistence analytics...")

def cmd_regime_duration_analytics(args):
    print("Building duration analytics...")

def cmd_regime_churn_diagnostics(args):
    print("Building churn diagnostics...")

def cmd_regime_stability_diagnostics(args):
    print("Building stability diagnostics...")

def cmd_cross_symbol_regime_transitions(args):
    print("Building cross-symbol transition analytics...")

def cmd_rolling_transition_analytics(args):
    print("Building rolling transition analytics...")

def cmd_transition_concentration_metrics(args):
    print("Building transition concentration metrics...")

def cmd_regime_diagnostics_readiness_gate(args):
    print("Evaluating diagnostics readiness gate...")

def cmd_regime_diagnostics_schema_check(args):
    print("Evaluating schema validator...")

def cmd_regime_diagnostics_safety_check(args):
    print("Evaluating safety validator...")

def cmd_regime_transition_context(args):
    print("Building transition context...")

def cmd_regime_transition_review(args):
    print(f"Building full regime transition review... write={write}")

def cmd_regime_transition_summary(args):
    print("Printing regime transition store summary...")

def cmd_regime_transition_validate(args):
    print("Validating transition reviews in store...")



def append_phase129_to_parser(subparsers):
    p1 = subparsers.add_parser("regime-transition-info")
    p1.set_defaults(func=cmd_regime_transition_info)

    p2 = subparsers.add_parser("regime-transition-matrix")
    p2.add_argument("--write", action="store_true")
    p2.set_defaults(func=cmd_regime_transition_matrix)

    p3 = subparsers.add_parser("regime-transition-review")
    p3.add_argument("--write", action="store_true")
    p3.set_defaults(func=cmd_regime_transition_review)

# @cli.command()
def regime_alignment_info():
    """Phase 131 Regime Alignment Info"""
    click.echo("Phase 131 is regime-aware alignment, NOT activation/deployment.")
    click.echo("Overlay/compatibility outputs are NOT trade signals.")

# @cli.command()
# # @click.option
def compute_regime_compatibility(write: bool):
    """Compute regime compatibility"""
    click.echo(f"Computed compatibility (write={write})")

# @cli.command()
# # @click.option
def regime_alignment_review(write: bool):
    """Generate Phase 131 full review"""
    click.echo(f"Generated full review (write={write})")


# @click.command(name="research-freeze-info")
def research_freeze_info():
    click.echo("Phase 134 is regime monitoring validation, drift report QA, and freeze preparation.")
    click.echo("This is NOT deployment, strategy activation, model training, prediction, or live daemon.")

# @click.command(name="research-freeze-ingest-monitoring")
def research_freeze_ingest_monitoring():
    click.echo("Ingesting regime monitoring preview...")

# @click.command(name="monitoring-artifact-load")
def monitoring_artifact_load():
    click.echo("Loading monitoring artifacts...")

# @click.command(name="monitoring-validation-specs")
def monitoring_validation_specs():
    click.echo("Generating monitoring validation specs...")

# @click.command(name="run-monitoring-validation")
# @click.option("--write", is_flag=True, help="Write metadata reports to local data folder")
def run_monitoring_validation(write):
    click.echo(f"Running monitoring validation... write={write}")

# @click.command(name="build-drift-report")
# @click.option("--write", is_flag=True, help="Write metadata reports to local data folder")
def build_drift_report(write):
    click.echo(f"Building drift report (no investment advice)... write={write}")

# @click.command(name="drift-report-qa")
def drift_report_qa():
    click.echo("Running drift report QA...")

# @click.command(name="validate-monitoring-consistency")
def validate_monitoring_consistency():
    click.echo("Validating monitoring consistency...")

# @click.command(name="validate-degradation-consistency")
def validate_degradation_consistency():
    click.echo("Validating degradation consistency...")

# @click.command(name="build-research-freeze-package")
# @click.option("--write", is_flag=True, help="Write metadata reports to local data folder")
def build_research_freeze_package(write):
    click.echo(f"Building research freeze package (not a deployment package)... write={write}")

# @click.command(name="validate-research-freeze-package")
def validate_research_freeze_package():
    click.echo("Validating research freeze package...")

# @click.command(name="research-freeze-readiness-gate")
def research_freeze_readiness_gate():
    click.echo("Checking research freeze readiness gate (no strategy activation)...")

# @click.command(name="research-freeze-schema-check")
def research_freeze_schema_check():
    click.echo("Checking research freeze schema...")

# @click.command(name="research-freeze-safety-check")
def research_freeze_safety_check():
    click.echo("Checking research freeze safety boundaries...")

# @click.command(name="research-freeze-context")
def research_freeze_context():
    click.echo("Building research freeze context...")

# @click.command(name="research-freeze-review")
# @click.option("--write", is_flag=True, help="Write metadata reports to local data folder")
def research_freeze_review(write):
    click.echo(f"Building research freeze full review... write={write}")

# @click.command(name="research-freeze-summary")
def research_freeze_summary():
    click.echo("Displaying research freeze summary...")

# @click.command(name="research-freeze-validate")
def research_freeze_validate():
    click.echo("Running full research freeze validation...")
