import os
import sys

# Add root folder to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set VERCEL environment variable to simulate Vercel deployment
os.environ["VERCEL"] = "1"

from app import resolve_path, load_config

print("=== VERIFYING VERCEL PATH RESOLUTION ===")
print("Simulating Vercel environment (VERCEL=1)")

# Test 1: Writing path
write_path_config = resolve_path("config.json", write=True)
print("1. Write Path config.json (expected: /tmp/config.json):", write_path_config)
assert os.path.normpath(write_path_config) == os.path.normpath("/tmp/config.json"), f"Unexpected write path: {write_path_config}"

# Test 2: Reading path before sync (when file does not exist in /tmp)
read_path_initial = resolve_path("config.json", write=False)
expected_initial = os.path.join(os.getcwd(), "config.json")
print("2. Read Path config.json (before sync/exists, expected: project root config.json):", read_path_initial)
assert os.path.normpath(read_path_initial) == os.path.normpath(expected_initial), f"Unexpected initial read path: {read_path_initial}"

# Test 3: Reading path after sync (when file exists in /tmp)
# Create a dummy file in /tmp to simulate sync/upload
os.makedirs("/tmp", exist_ok=True)
dummy_file = os.path.join("/tmp", "config.json")
with open(dummy_file, "w") as f:
    f.write("{}")

read_path_after = resolve_path("config.json", write=False)
print("3. Read Path config.json (after sync/exists, expected: /tmp/config.json):", read_path_after)
assert os.path.normpath(read_path_after) == os.path.normpath("/tmp/config.json"), f"Unexpected read path after: {read_path_after}"

# Cleanup dummy file
try:
    os.remove(dummy_file)
except Exception as e:
    pass

print("=== VERIFICATION PASSED SUCCESSFULLY ===")
