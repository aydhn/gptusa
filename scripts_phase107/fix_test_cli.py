print("Fixing test cli sys exit mock")
import re

with open("tests/test_cli_phase107.py", "r") as f:
    content = f.read()

content = content.replace("main()", """try:
            main()
        except SystemExit as e:
            assert e.code == 0
""")

with open("tests/test_cli_phase107.py", "w") as f:
    f.write(content)
