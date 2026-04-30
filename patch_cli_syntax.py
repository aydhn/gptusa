file_path = "usa_signal_bot/app/cli.py"
with open(file_path, "r") as f:
    content = f.read()

# There is a missing block for exceptions before `elif cmd == "active-universe-info":` which caused SyntaxError
content = content.replace("def main() -> int:", "def main() -> int:")
# Let's fix the syntax error directly by running syntax check
