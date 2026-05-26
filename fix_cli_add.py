with open('usa_signal_bot/app/cli.py', 'r') as f:
    content = f.read()

# We need to make sure phase116_add_commands is actually defined before main() is called.
# And inside main(), it calls phase116_add_commands(subparsers).

if "def phase116_add_commands(subparsers):" in content:
    print("Found definition.")
else:
    print("Definition NOT found!")
