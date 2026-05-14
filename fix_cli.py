import re

file_cli = "usa_signal_bot/app/cli.py"

with open(file_cli, 'r') as f:
    content = f.read()

# I will use a different anchor, perhaps `_add_transaction_cost_parsers` is not called, or called differently. Let's add it right before `args = parser.parse_args()`
content = re.sub(r'(\s*args = parser\.parse_args\(\))', r'\n    setup_cost_robustness_parsers(subparsers)\1', content)

with open(file_cli, 'w') as f:
    f.write(content)
