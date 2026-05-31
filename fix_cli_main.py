file_path = "usa_signal_bot/app/cli.py"
with open(file_path, "r") as f:
    content = f.read()

if "setup_phase135_cli(subparsers)" not in content.split("def main()")[1]:
    content = content.replace(
        "def main():\n    parser = argparse.ArgumentParser()\n    subparsers = parser.add_subparsers(dest='command')\n",
        "def main():\n    parser = argparse.ArgumentParser()\n    subparsers = parser.add_subparsers(dest='command')\n    setup_phase135_cli(subparsers)\n"
    )

with open(file_path, "w") as f:
    f.write(content)
