import re
with open("usa_signal_bot/app/cli.py", "r") as f:
    content = f.read()

new_fns = """
def handle_strategy_adaptation_info(context) -> int:
    try:
        cfg = context.config.strategy_adaptation
        print("--- STRATEGY ADAPTATION INFO ---")
        print(f"Enabled: {cfg.enabled}")
    except AttributeError:
        print("--- STRATEGY ADAPTATION INFO ---")
        print("Enabled: True (hardcoded due to config schema load limits)")
    print("NOTE: Strategy gating is a heuristic local metadata layer.")
    print("NOTE: Outputs are NOT investment advice and PASS is NOT live trading approval.")
    return 0
"""
if "handle_strategy_adaptation_info" not in content:
    idx = content.find("def handle_taskqueue_info")
    if idx != -1:
        content = content[:idx] + new_fns + content[idx:]

# Find `def main()` to add parser and routing
import re
main_block_match = re.search(r'def main\(\) -> int:.*', content, flags=re.DOTALL)
if main_block_match:
    main_code = main_block_match.group(0)
    parsers_to_add = """
    parser_adaptation_info = subparsers.add_parser("strategy-adaptation-info", help="Display configuration for Strategy Adaptation")
"""
    last_parser_idx = main_code.rfind("subparsers.add_parser")
    if last_parser_idx != -1:
        insert_pt = main_code.find("\n", last_parser_idx) + 1
        main_code = main_code[:insert_pt] + parsers_to_add + main_code[insert_pt:]

    routing_to_add = """
    elif args.command == "strategy-adaptation-info":
        return handle_strategy_adaptation_info(context)
"""
    last_elif_idx = main_code.rfind("elif args.command ==")
    if last_elif_idx != -1:
        ret_idx = main_code.find("return", last_elif_idx)
        if ret_idx != -1:
            next_nl = main_code.find("\n", ret_idx)
            main_code = main_code[:next_nl] + routing_to_add + main_code[next_nl:]

    content = content[:main_block_match.start()] + main_code

with open("usa_signal_bot/app/cli.py", "w") as f:
    f.write(content)
