import random
import os

os.makedirs("shards", exist_ok=True)

valid_domains = ["gmail.com", "yahoo.com", "hotmail.com"]
names = ["Alice Smith", "Bob Lee", "Carla Diaz", "Dev Patel", "Evan Cho"]

for shard_idx in range(8):
    random.seed(shard_idx)
    rows = [["email", "name"]]
    n_rows = 50
    for i in range(n_rows):
        name = random.choice(names)
        r = random.random()
        if r < 0.15: # set email missing
            email = ""
        elif r < 0.30: # @ missing, domain missing, @@
            email = random.choice(["not-an-email", "bad@", "@nodomain.com", "user@@x.com"])
        else:
            email = f"user{i}@{random.choice(valid_domains)}"
        rows.append([email, name])

    with open(f"shards/signup_shard_{shard_idx}.csv", "w") as f:
        for row in rows:
            f.write(",".join(row) + "\n")
    print(f"shard {shard_idx}: wrote {n_rows} rows")