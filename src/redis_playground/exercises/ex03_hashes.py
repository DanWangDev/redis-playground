"""Exercise 03: Hashes — object storage, field ops, atomic increments."""

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
        client.hset(
            "user:1",
            mapping={
                "name": "Alice",
                "email": "alice@example.com",
                "age": "28",
                "plan": "pro",
            },
        )
        self.log.command(
            'HSET user:1 name "Alice" email "alice@example.com" age 28 plan "pro"'
        )
        count = client.hlen("user:1")
        self.log.command("HLEN user:1")
        self.log.output(f"→ {count} fields")
        results.append(count)

        # ── Step 2: Retrieve fields ────────────────────────────
        self.log.section("Step 2: Retrieve Fields")
        name = client.hget("user:1", "name")
        fields = client.hmget("user:1", ["name", "email", "plan"])
        everything = client.hgetall("user:1")
        self.log.command("HGET user:1 name → HMGET → HGETALL")
        self.log.output(f"name={name!r}, multi={fields}, all={len(everything)} fields")
        results.extend([name, *fields, len(everything)])

        # ── Step 3: Atomic field increments ────────────────────
        self.log.section("Step 3: Atomic Field Increments")
        new_age = client.hincrby("user:1", "age", 1)
        login_count = client.hincrby("user:1", "login_count", 1)
        self.log.command("HINCRBY user:1 age 1 → HINCRBY user:1 login_count 1")
        self.log.output(f"age={new_age}, login_count={login_count}")
        results.extend([new_age, login_count])

        # ── Step 4: Field existence ────────────────────────────
        self.log.section("Step 4: Field Existence")
        has_email = client.hexists("user:1", "email")
        has_phone = client.hexists("user:1", "phone")
        self.log.command("HEXISTS user:1 email → HEXISTS user:1 phone")
        self.log.output(f"email={has_email}, phone={has_phone}")
        keys = client.hkeys("user:1")
        vals = client.hvals("user:1")
        results.extend([has_email, has_phone, len(keys), len(vals)])

        # ── Step 5: Delete a field ─────────────────────────────
        self.log.section("Step 5: Delete a Field")
        deleted = client.hdel("user:1", "plan")
        exists_after = client.hexists("user:1", "plan")
        self.log.command("HDEL user:1 plan")
        self.log.output(f"Deleted {deleted}, exists after: {exists_after}")
        results.extend([deleted, exists_after])

        # ── Step 6: Multiple users ─────────────────────────────
        self.log.section("Step 6: Seed and Query Multiple Users")
        seed_users(client)
        total = len(client.keys("user:*"))
        self.log.command("KEYS user:*")
        self.log.output(f"Found {total} user profiles")
        results.append(total)

        self.log.separator()
        self.log.success(
            f"Hash ops: {results[0]} fields, name={results[1]!r}, "
            f"age={results[6]}, users={results[13]}"
        )
        return results
