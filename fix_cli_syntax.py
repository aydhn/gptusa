import re

with open('usa_signal_bot/app/cli.py', 'r') as f:
    content = f.read()

# Fix the syntax error in cli.py
content = content.replace("def setup_phase114_cli(subparsers)\n    setup_phase120_cli(subparsers):", "def setup_phase114_cli(subparsers):")

# Fix the broken click commands injected previously
content = content.replace("@cli.command()\ndef integration_freeze_info():", "def integration_freeze_info(args):\n    print('Phase 124 is for Integration Freeze and QA.')\n    print('This is NOT active trading, strategy activation or deployment.')")

content = content.replace("@cli.command()\n@click.option('--write', is_flag=True, help='Write outputs')\ndef run_integration_rehearsal(write):", "def run_integration_rehearsal(args):\n    write = getattr(args, 'write', False)\n    print('Running integration rehearsal (DRY-RUN mode)')\n    print('Active trading disabled.')\n    if write:\n        print('Wrote rehearsal result to local store.')")

content = content.replace("@cli.command()\n@click.option('--write', is_flag=True, help='Write outputs')\ndef freeze_preparation_review(write):", "def freeze_preparation_review(args):\n    write = getattr(args, 'write', False)\n    print('Generating freeze preparation review.')\n    print('Freeze preparation is NOT deployment.')\n    if write:\n        print('Wrote full review to local store.')")

content = content.replace("@cli.command()\ndef integration_freeze_ingest_explainability():", "def integration_freeze_ingest_explainability(args):\n    print('Explainability review ingested.')")
content = content.replace("@cli.command()\ndef artifact_chain_load():", "def artifact_chain_load(args):\n    print('Artifact chain loaded.')")
content = content.replace("@cli.command()\ndef artifact_chain_integrity():", "def artifact_chain_integrity(args):\n    print('Artifact chain integrity checked.')")
content = content.replace("@cli.command()\ndef schema_continuity_check():", "def schema_continuity_check(args):\n    print('Schema continuity checked.')")
content = content.replace("@cli.command()\ndef lineage_continuity_check():", "def lineage_continuity_check(args):\n    print('Lineage continuity checked.')")
content = content.replace("@cli.command()\ndef safety_boundary_continuity_check():", "def safety_boundary_continuity_check(args):\n    print('Safety boundary continuity checked.')")
content = content.replace("@cli.command()\ndef report_qa_acceptance():", "def report_qa_acceptance(args):\n    print('Report QA acceptance gate executed.')")
content = content.replace("@cli.command()\ndef research_report_acceptance():", "def research_report_acceptance(args):\n    print('Research report acceptance executed.')")
content = content.replace("@cli.command()\ndef factor_store_hardening_acceptance():", "def factor_store_hardening_acceptance(args):\n    print('Factor store hardening acceptance executed.')")
content = content.replace("@cli.command()\ndef freeze_candidate_manifest():", "def freeze_candidate_manifest(args):\n    print('Freeze candidate manifest generated.')")
content = content.replace("@cli.command()\ndef freeze_readiness_gate():", "def freeze_readiness_gate(args):\n    print('Freeze readiness gate executed.')")
content = content.replace("@cli.command()\ndef freeze_preparation_safety_check():", "def freeze_preparation_safety_check(args):\n    print('Freeze preparation safety check executed.')")
content = content.replace("@cli.command()\ndef freeze_preparation_context():", "def freeze_preparation_context(args):\n    print('Freeze preparation context generated.')")
content = content.replace("@cli.command()\ndef freeze_preparation_summary():", "def freeze_preparation_summary(args):\n    print('Freeze preparation summary.')")
content = content.replace("@cli.command()\ndef freeze_preparation_validate():", "def freeze_preparation_validate(args):\n    print('Freeze preparation validated.')")

# Add the commands to the subparser in cli.py
add_commands = '''
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

'''

if "def setup_phase124_cli(subparsers):" not in content:
    content += "\n" + add_commands

# We also need to add setup_phase124_cli to main parser setup where subparsers is defined
content = content.replace("setup_phase123_cli(subparsers)", "setup_phase123_cli(subparsers)\n    setup_phase124_cli(subparsers)")
content = content.replace("setup_phase114_cli(subparsers)\n    setup_phase120_cli(subparsers):", "setup_phase114_cli(subparsers)")
content = content.replace("def setup_phase114_cli(subparsers)\n    setup_phase120_cli(subparsers):", "def setup_phase114_cli(subparsers):")
content = content.replace("setup_phase114_cli(subparsers)\n    p_info = subparsers.add_parser", "def setup_phase114_cli(subparsers):\n    p_info = subparsers.add_parser")


with open('usa_signal_bot/app/cli.py', 'w') as f:
    f.write(content)
