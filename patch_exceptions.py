file_path = "usa_signal_bot/core/exceptions.py"

with open(file_path, "r") as f:
    text = f.read()

# Replace USA_SignalBotError with USA_SignalBotError if it doesn't exist, wait, the error is about BotError
text = text.replace("class RegimeMonitoringError(BotError):", "class RegimeMonitoringError(Exception):")
text = text.replace("class RegimeResearchFreezeError(USA_SignalBotError):", "class RegimeResearchFreezeError(Exception):")

with open(file_path, "w") as f:
    f.write(text)
