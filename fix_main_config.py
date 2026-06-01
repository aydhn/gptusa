import re
with open('usa_signal_bot/core/config_schema.py', 'r') as f:
    content = f.read()

if "calibration_diagnostics: CalibrationDiagnosticsConfig" not in content:
    # Find class Config: and add it
    content = re.sub(
        r'(class Config:.*?)(\n\n|$)',
        r'\1\n    calibration_diagnostics: CalibrationDiagnosticsConfig = field(default_factory=CalibrationDiagnosticsConfig)\2',
        content,
        flags=re.DOTALL
    )
    with open('usa_signal_bot/core/config_schema.py', 'w') as f:
        f.write(content)
