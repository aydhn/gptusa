with open('usa_signal_bot/core/config_schema.py', 'r') as f:
    lines = f.readlines()

# Find the validate method inside Config
validate_idx = -1
for i, line in enumerate(lines):
    if "def validate(self) -> None:" in line:
        validate_idx = i
        break

if validate_idx != -1:
    lines.insert(validate_idx, "    feature_engine_foundation: FeatureEngineFoundationConfig = field(default_factory=FeatureEngineFoundationConfig)\n")
    lines.insert(validate_idx, "    phase116_feature_policy: Phase116FeaturePolicyConfig = field(default_factory=Phase116FeaturePolicyConfig)\n")
    lines.insert(validate_idx, "    phase116_feature_scope: Phase116FeatureScopeConfig = field(default_factory=Phase116FeatureScopeConfig)\n")
    lines.insert(validate_idx, "    phase116_notifications: Phase116NotificationsConfig = field(default_factory=Phase116NotificationsConfig)\n")

# Need to fix the data_provider_abstraction indent issues as well
# Check for "    data_provider_abstraction:" but indented too far
for i, line in enumerate(lines):
    if line.startswith("        data_provider_abstraction: DataProviderAbstractionConfig"):
        lines[i] = "    data_provider_abstraction: DataProviderAbstractionConfig = field(default_factory=DataProviderAbstractionConfig)\n"

with open('usa_signal_bot/core/config_schema.py', 'w') as f:
    f.writelines(lines)
