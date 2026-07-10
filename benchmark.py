import time
import random
from datetime import datetime, timedelta

# Define the two versions of the function logic

def current_logic(rows, start_date=None, end_date=None):
    actual_set = {
        d_val[:10]
        for r in rows
        if isinstance(d_val := (r.get("date") or r.get("timestamp") or ""), str)
        and len(d_val) >= 10
    }

    if not actual_set and not start_date and not end_date:
        return []

    start = start_date or (min(actual_set) if actual_set else "")
    end = end_date or (max(actual_set) if actual_set else "")
    return actual_set

def optimized_logic(rows, start_date=None, end_date=None):
    actual_set = {
        d_val[:10]
        for r in rows
        if isinstance(d_val := (r.get("date") or r.get("timestamp") or ""), str)
        and len(d_val) >= 10
    }

    if not actual_set and not start_date and not end_date:
        return []

    start = start_date or (min(actual_set) if actual_set else "")
    end = end_date or (max(actual_set) if actual_set else "")
    return actual_set


# Generate some test data
base_date = datetime(2020, 1, 1)
test_rows = []
for i in range(100000):
    dt = base_date + timedelta(days=i)
    # Mix formats to simulate realistic data
    fmt = "%Y-%m-%d" if random.random() > 0.5 else "%Y-%m-%dT%H:%M:%S"
    date_str = dt.strftime(fmt)
    if random.random() > 0.5:
        test_rows.append({"date": date_str})
    else:
        test_rows.append({"timestamp": date_str})

# Add some bad data
for _ in range(5000):
    test_rows.append({"date": None})
    test_rows.append({"timestamp": 1234567890})
    test_rows.append({})

# Warm up
current_logic(test_rows[:1000])
optimized_logic(test_rows[:1000])

# Benchmark current
start = time.perf_counter()
for _ in range(10):
    current_logic(test_rows)
end = time.perf_counter()
current_time = end - start

# Benchmark optimized
start = time.perf_counter()
for _ in range(10):
    optimized_logic(test_rows)
end = time.perf_counter()
optimized_time = end - start

print(f"Current logic time: {current_time:.4f}s")
print(f"Optimized logic time: {optimized_time:.4f}s")
if current_time > 0:
    print(f"Improvement: {(current_time - optimized_time) / current_time * 100:.2f}%")
