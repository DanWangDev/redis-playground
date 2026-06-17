"""Exercise 03: Hashes.

Store and manipulate objects as Redis hashes:
HSET, HGET, HGETALL, HMGET, HINCRBY, HDEL, HEXISTS, HLEN, HKEYS, HVALS.
"""

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner
from redis_playground.shared.data_factory import seed_users


class Ex03Hashes(ExerciseRunner):
    def __init__(self):
        super().__init__("03-hashes", "Hashes")

    def run(self, client: redis.Redis) -> list:
        results = []

        # ── Step 1: Create objects with HSET ───────────────────
        self.log.section("Step 1: Store Objects with HSET")
        self.log.concept("Hashes store objects as field-value pairs — like a Python dict in Redis.")
        self.log.concept("HSET with 'mapping' parameter sets multiple fields in one command.")

        client.hset("user:1", mapping={"name": "Alice", "email": "alice@example.com", "age": "28", "plan": "pro"})
        self.log.command('HSET user:1 name "Alice" email "alice@example.com" age 28 plan "pro"')
        self.log.success("User profile stored as hash")

        count = client.hlen("user:1")
        self.log.command("HLEN user:1")
        self.log.output(f"→ {count} fields")
        results.append(count)

        # ── Step 2: Retrieve fields ────────────────────────────
        self.log.section("Step 2: Retrieve Fields")
        self.log.concept("HGET gets a single field. HMGET gets multiple. HGETALL gets everything.")

        name = client.hget("user:1", "name")
        self.log.command("HGET user:1 name")
        self.log.output(f'→ "{name}"')
        results.append(name)

        fields = client.hmget("user:1", ["name", "email", "plan"])
        self.log.command("HMGET user:1 name email plan")
        self.log.output(str(fields))
        results.extend(fields)

        everything = client.hgetall("user:1")
        self.log.command("HGETALL user:1")
        self.log.output(str(everything))
        results.append(len(everything))

        # ── Step 3: Atomic field increments ────────────────────
        self.log.section("Step 3: Atomic Field Increments")
        self.log.concept("HINCRBY atomically increments a numeric hash field.")
        self.log.concept("No read-then-write race — the increment is atomic.")

        new_age = client.hincrby("user:1", "age", 1)
        self.log.command("HINCRBY user:1 age 1")
        self.log.output(f"Age is now: {new_age}")
        results.append(new_age)

        self.log.concept("You can also add a counter field that didn't exist before:")
        login_count = client.hincrby("user:1", "login_count", 1)
        self.log.command("HINCRBY user:1 login_count 1")
        self.log.output(f"Login count: {login_count}")
        results.append(login_count)

        # ── Step 4: Check field existence ──────────────────────
        self.log.section("Step 4: Field Existence and Metadata")
        self.log.concept("HEXISTS checks if a specific field exists in the hash.")

        has_email = client.hexists("user:1", "email")
        has_phone = client.hexists("user:1", "phone")
        self.log.command("HEXISTS user:1 email")
        self.log.output(f"→ {has_email}")
        self.log.command("HEXISTS user:1 phone")
        self.log.output(f"→ {has_phone}")
        results.extend([has_email, has_phone])

        # List all fields and values
        keys = client.hkeys("user:1")
        vals = client.hvals("user:1")
        self.log.command("HKEYS user:1")
        self.log.output(str(keys))
        self.log.command("HVALS user:1")
        self.log.output(str(vals))
        results.extend([len(keys), len(vals)])

        # ── Step 5: Delete a field ─────────────────────────────
        self.log.section("Step 5: Delete a Field")
        self.log.concept("HDEL removes one or more fields from a hash.")
        self.log.concept("If all fields are removed, the hash key itself is deleted.")

        deleted = client.hdel("user:1", "plan")
        self.log.command("HDEL user:1 plan")
        self.log.output(f"→ Deleted {deleted} field(s)")

        exists_after = client.hexists("user:1", "plan")
        self.log.command("HEXISTS user:1 plan")
        self.log.output(f"→ {exists_after} (0 = gone)")
        results.extend([deleted, exists_after])

        # ── Step 6: Seed and query multiple users ──────────────
        self.log.section("Step 6: Working with Multiple User Profiles")
        seed_users(client)
        total_users = len(client.keys("user:*"))
        self.log.command("KEYS user:*")
        self.log.output(f"Found {total_users} user profiles")
        results.append(total_users)

        # ── Summary ─────────────────────────────────────────────
        self.log.separator()
        self.log.success(f"Hash operations complete: {len(client.hgetall('user:1'))} fields remaining on user:1")
        return results
