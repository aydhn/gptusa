import re
with open('usa_signal_bot/core/config_schema.py', 'r') as f:
    content = f.read()

# Remove the previously appended CalibrationDiagnosticsConfig
content = re.sub(
    r'\n    calibration_diagnostics: CalibrationDiagnosticsConfig = field\(default_factory=CalibrationDiagnosticsConfig\)',
    '',
    content
)

# And use 'CalibrationDiagnosticsConfig' as forward reference
content = re.sub(
    r'(class Config:.*?)(\n\n|$)',
    r"\1\n    calibration_diagnostics: 'CalibrationDiagnosticsConfig' = field(default_factory=dict)\2",
    content,
    flags=re.DOTALL
)

with open('usa_signal_bot/core/config_schema.py', 'w') as f:
    f.write(content)
