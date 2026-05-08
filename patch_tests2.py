from pathlib import Path

# Fix test live language
f_path = Path("tests/test_release_validation.py")
content = f_path.read_text()
content = content.replace('res2.warnings[0]', 'res2.errors[0]')
f_path.write_text(content)
