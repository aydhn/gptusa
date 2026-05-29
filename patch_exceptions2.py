import re

with open("usa_signal_bot/core/exceptions.py", "r") as f:
    content = f.read()

# Replace RegimeLabelingError(USAError) with RegimeLabelingError(Exception)
# if USAError is not found or use a proper base class. I'll check if USASignalBotError exists.
if "class USASignalBotError(" in content:
    content = content.replace("RegimeLabelingError(USAError)", "RegimeLabelingError(USASignalBotError)")
else:
    content = content.replace("RegimeLabelingError(USAError)", "RegimeLabelingError(Exception)")

with open("usa_signal_bot/core/exceptions.py", "w") as f:
    f.write(content)
