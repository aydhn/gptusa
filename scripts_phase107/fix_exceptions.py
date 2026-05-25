with open("usa_signal_bot/core/exceptions.py", "r") as f:
    lines = f.readlines()

# check if CoreError is defined, if not, find the base error
has_core_error = False
for line in lines:
    if "class CoreError" in line:
        has_core_error = True
        break

print(f"Has CoreError: {has_core_error}")
if not has_core_error:
    # Just replace CoreError with Exception
    new_lines = []
    for line in lines:
        if "DataProviderRuntimeError(CoreError)" in line:
            new_lines.append("class DataProviderRuntimeError(Exception):\n")
        else:
            new_lines.append(line)

    with open("usa_signal_bot/core/exceptions.py", "w") as f:
        f.writelines(new_lines)
