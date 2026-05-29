import glob

for test_file in glob.glob("tests/test_*.py"):
    with open(test_file, 'r') as f:
        text = f.read()

    if 'import pandas as pd' not in text and 'pd.' in text:
        text = 'import pandas as pd\n' + text
        with open(test_file, 'w') as f:
            f.write(text)
    elif 'try:\n    import pandas as pd\nexcept ImportError:\n    pass' in text:
        text = text.replace('try:\n    import pandas as pd\nexcept ImportError:\n    pass', 'import pandas as pd')
        with open(test_file, 'w') as f:
            f.write(text)

