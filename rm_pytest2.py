import glob

files = glob.glob("tests/test_markdown_behavior_report_renderer.py") + \
        glob.glob("tests/test_json_behavior_report_renderer.py") + \
        glob.glob("tests/test_text_behavior_report_renderer.py")

for f in files:
    with open(f, "r") as file:
        content = file.read()
    content = content.replace("import pytest\n", "")
    with open(f, "w") as file:
        file.write(content)
