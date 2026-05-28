with open("usa_signal_bot/app/cli.py", "r") as f:
    content = f.read()

# remove the broken part, search for "def final_closure_info(args):" and remove until end
idx = content.find("def final_closure_info(args):")
if idx != -1:
    content = content[:idx]

with open("usa_signal_bot/app/cli.py", "w") as f:
    f.write(content)
