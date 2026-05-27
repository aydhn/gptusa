import pandas as pd

series = pd.Series([1] * 20 + [1000])
mean = series.mean()
std = series.std()
print("mean:", mean)
print("std:", std)
z = (series - mean).abs() / std
print("max z:", z.max())

def fix_test():
    with open("tests/test_phase121.py", "r") as f:
        content = f.read()

    # The max possible z-score for a sample size of N is roughly sqrt(N-1)
    # For N=10, max z is around 3. For N=21, max z is around 4.47.

    content = content.replace("df = pd.DataFrame({\"f1\": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1000]})", "df = pd.DataFrame({\"f1\": [1]*20 + [1000]})")

    with open("tests/test_phase121.py", "w") as f:
        f.write(content)

fix_test()
