import sys
import re

def patch_cli():
    file_path = "usa_signal_bot/app/cli.py"
    with open(file_path, "r") as f:
        content = f.read()

    # We need to import our setup function
    if "from usa_signal_bot.regime_classification.final_closure import setup_phase135_cli" not in content:
        content = content.replace(
            "import argparse\n",
            "import argparse\nfrom usa_signal_bot.regime_classification.final_closure import setup_phase135_cli\n"
        )

    # We need to call our setup function
    if "setup_phase135_cli(subparsers)" not in content:
        # Find where setup functions are called and add ours
        content = re.sub(
            r"(setup_phase[0-9]+.*?\(subparsers\)\n)+",
            r"\g<0>    setup_phase135_cli(subparsers)\n",
            content,
            count=1
        )

        # If the regex didn't work (maybe no setup_phase functions yet), just put it before the return
        if "setup_phase135_cli(subparsers)" not in content:
             content = content.replace(
                "return parser",
                "setup_phase135_cli(subparsers)\n    return parser"
             )

    with open(file_path, "w") as f:
        f.write(content)

if __name__ == "__main__":
    patch_cli()
