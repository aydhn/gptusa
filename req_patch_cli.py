with open("usa_signal_bot/app/cli.py", "r") as f:
    content = f.read()

cli_add = """
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
"""

import re

# Add parsers
subparsers_add = """
    p130_info = subparsers.add_parser("market-behavior-info", help="Phase 130 Market Behavior Info")
    p130_info.set_defaults(func=phase130_market_behavior_info)

    p130_ingest = subparsers.add_parser("market-behavior-ingest-transition", help="Phase 130 Ingest Transition")
    p130_ingest.set_defaults(func=phase130_market_behavior_ingest_transition)

    p130_load = subparsers.add_parser("diagnostics-artifact-load", help="Phase 130 Load Artifacts")
    p130_load.set_defaults(func=phase130_diagnostics_artifact_load)

    p130_specs = subparsers.add_parser("market-behavior-profile-specs", help="Phase 130 Profile Specs")
    p130_specs.set_defaults(func=phase130_market_behavior_profile_specs)

    p130_profiles = subparsers.add_parser("build-market-behavior-profiles", help="Phase 130 Build Profiles")
    p130_profiles.add_argument("--write", action="store_true")
    p130_profiles.set_defaults(func=phase130_build_market_behavior_profiles)

    p130_summaries = subparsers.add_parser("build-regime-behavior-summaries", help="Phase 130 Build Summaries")
    p130_summaries.add_argument("--write", action="store_true")
    p130_summaries.set_defaults(func=phase130_build_regime_behavior_summaries)

    p130_intps = subparsers.add_parser("build-diagnostics-interpretations", help="Phase 130 Build Interpretations")
    p130_intps.add_argument("--write", action="store_true")
    p130_intps.set_defaults(func=phase130_build_diagnostics_interpretations)

    p130_cross = subparsers.add_parser("build-cross-symbol-behavior-profile", help="Phase 130 Build Cross-Symbol Profile")
    p130_cross.set_defaults(func=phase130_build_cross_symbol_behavior_profile)

    p130_report = subparsers.add_parser("build-behavior-report", help="Phase 130 Build Behavior Report")
    p130_report.add_argument("--write", action="store_true")
    p130_report.set_defaults(func=phase130_build_behavior_report)

    p130_rend_md = subparsers.add_parser("render-behavior-report-markdown", help="Phase 130 Render MD")
    p130_rend_md.add_argument("--write", action="store_true")
    p130_rend_md.set_defaults(func=phase130_render_behavior_report_markdown)

    p130_rend_json = subparsers.add_parser("render-behavior-report-json", help="Phase 130 Render JSON")
    p130_rend_json.add_argument("--write", action="store_true")
    p130_rend_json.set_defaults(func=phase130_render_behavior_report_json)

    p130_rend_txt = subparsers.add_parser("render-behavior-report-text", help="Phase 130 Render TEXT")
    p130_rend_txt.add_argument("--write", action="store_true")
    p130_rend_txt.set_defaults(func=phase130_render_behavior_report_text)

    p130_qa = subparsers.add_parser("behavior-report-qa", help="Phase 130 Run QA")
    p130_qa.set_defaults(func=phase130_behavior_report_qa)

    p130_gate = subparsers.add_parser("market-behavior-readiness-gate", help="Phase 130 Run Readiness Gate")
    p130_gate.set_defaults(func=phase130_market_behavior_readiness_gate)

    p130_safe = subparsers.add_parser("market-behavior-safety-check", help="Phase 130 Safety Check")
    p130_safe.set_defaults(func=phase130_market_behavior_safety_check)

    p130_ctx = subparsers.add_parser("market-behavior-context", help="Phase 130 Context")
    p130_ctx.set_defaults(func=phase130_market_behavior_context)

    p130_review = subparsers.add_parser("market-behavior-review", help="Phase 130 Build Review")
    p130_review.add_argument("--write", action="store_true")
    p130_review.set_defaults(func=phase130_market_behavior_review)

    p130_summary = subparsers.add_parser("market-behavior-summary", help="Phase 130 Store Summary")
    p130_summary.set_defaults(func=phase130_market_behavior_summary)

    p130_val = subparsers.add_parser("market-behavior-validate", help="Phase 130 Validate Payload")
    p130_val.set_defaults(func=phase130_market_behavior_validate)
"""

if "def phase130_market_behavior_info" not in content:
    # insert functions before main
    content = content.replace("def main():", cli_add + "\ndef main():")

    # insert subparsers
    content = content.replace("return parser", subparsers_add + "\n    return parser")

    with open("usa_signal_bot/app/cli.py", "w") as f:
        f.write(content)

print("Updated cli.py")
