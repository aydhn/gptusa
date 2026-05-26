with open('usa_signal_bot/core/config_schema.py', 'r') as f:
    content = f.read()

# I see what I did: I appended classes to the end of the file, AFTER `class Config:`.
# We need to move the new classes BEFORE `class Config:`.

# 1. Strip the classes from the end.
# We will use regex to find class Config: and split the file.
parts = content.split('class Config:')
part1 = parts[0]
part2 = parts[1]

# In part2, we added the Phase 116 classes at the end. We will extract them and put them at the end of part1.
# The added classes start with `@dataclass\nclass FeatureEngineFoundationConfig:`
marker = "@dataclass\nclass FeatureEngineFoundationConfig:"

if marker in part2:
    sub_parts = part2.split(marker)
    part2_pure = sub_parts[0]
    appended_classes = marker + sub_parts[1]

    new_content = part1 + appended_classes + "\n\nclass Config:" + part2_pure

    with open('usa_signal_bot/core/config_schema.py', 'w') as f:
        f.write(new_content)
else:
    print("Classes not found in part 2")
