file_path = "usa_signal_bot/core/exceptions.py"

with open(file_path, "r") as f:
    text = f.read()

text = text.replace("(BotError):", "(Exception):")

with open(file_path, "w") as f:
    f.write(text)
