import re
with open('usa_signal_bot/core/config_schema.py', 'r') as f:
    content = f.read()

if "calibration_diagnostics: CalibrationDiagnosticsConfig" not in content:
    # Find the end of AppConfig fields and insert
    match = re.search(r'(class AppConfig:.*?)(?=\n@dataclass|\nclass|\Z)', content, re.DOTALL)
    if match:
        appconfig_content = match.group(1)
        if "    calibration_diagnostics: CalibrationDiagnosticsConfig" not in appconfig_content:
            new_appconfig = appconfig_content + "    calibration_diagnostics: CalibrationDiagnosticsConfig = field(default_factory=CalibrationDiagnosticsConfig)\n"
            content = content.replace(appconfig_content, new_appconfig)
            with open('usa_signal_bot/core/config_schema.py', 'w') as f:
                f.write(content)
