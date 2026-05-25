import os
import sys

def check_files():
    found = False
    for root, dirs, files in os.walk("usa_signal_bot"):
        for f in files:
            if "phase113" in f:
                print(f"Found: {os.path.join(root, f)}")
                found = True
    if not found:
        print("No Phase 113 files found.")
check_files()
