import os
import re
import csv
import time

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$") # validating email

# indexed jobs auto inject this env var
shard_idx = os.environ["JOB_COMPLETION_INDEX"]
node_name = os.environ.get("NODE_NAME", "unknown")
pod_name = os.environ.get("POD_NAME", "unknown")
shard_path = f"/data/signup_shard_{shard_idx}.csv"

invalid_count = 0
total = 0
# validating for a given shard
with open(shard_path, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        total += 1
        email = row.get("email", "").strip()
        name = row.get("name", "").strip()
        if not email or not name or not EMAIL_RE.match(email):
            invalid_count += 1

print(f"shard_index={shard_idx} pod={pod_name} node={node_name} " f"total={total} invalid={invalid_count}")
time.sleep(10) # to observe pods parallelism