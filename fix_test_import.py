import re

with open('tests/test_all_models.py', 'r') as f:
    content = f.read()

# Make sure we import our new models to test them in test_all_models.py if needed.
# Let's just create a new test explicitly for Phase 116 Models.
