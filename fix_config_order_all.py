with open('usa_signal_bot/core/config_schema.py', 'r') as f:
    content = f.read()

# Let's completely separate `class Config:` and all following lines and put them at the VERY end.
lines = content.split('\n')
config_start = -1
for i, line in enumerate(lines):
    if line.startswith('class Config:'):
        config_start = i
        break

if config_start != -1:
    config_body = lines[config_start:]
    classes_before = lines[:config_start]

    # But wait, there might be dataclasses defined INSIDE config_body due to previous bad appends.
    # We need to pull out any class definitions that start with @dataclass and class XXXConfig

    new_config_body = []
    pulled_classes = []

    in_pulled_class = False

    i = 0
    while i < len(config_body):
        line = config_body[i]

        # If we hit a dataclass definition that is NOT indented (so not inside Config)
        if line.startswith('@dataclass') and i + 1 < len(config_body) and config_body[i+1].startswith('class '):
            in_pulled_class = True
            pulled_classes.append(line)
            i += 1
            pulled_classes.append(config_body[i])
            i += 1
            continue

        if in_pulled_class:
            # Continue adding to pulled_classes until we hit a non-indented line that isn't empty and isn't another @dataclass
            if line.strip() == '':
                pulled_classes.append(line)
            elif line.startswith('    '):
                pulled_classes.append(line)
            else:
                in_pulled_class = False
                new_config_body.append(line)
        else:
            new_config_body.append(line)

        i += 1

    final_lines = classes_before + pulled_classes + new_config_body
    with open('usa_signal_bot/core/config_schema.py', 'w') as f:
        f.write('\n'.join(final_lines))
