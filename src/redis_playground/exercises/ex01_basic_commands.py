"""Exercise 01: Basic Commands.

Connect to Redis, explore fundamental CRUD operations:
PING, SET, GET, DEL, EXISTS, EXPIRE, TTL, KEYS, TYPE.
"""

import time

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner


class Ex01BasicCommands(ExerciseRunner):
    def __init__(self):
        super().__init__("01-basic-commands", "Basic Commands")

    def run(self, client: redis.Redis) -> list:
        results = []

        # ── Step 1: Connect and PING ────────────────────────────
        self.log.section("Step 1: Connect to Redis")
        self.log.concept("PING is the simplest Redis command — it returns PONG.")
        self.log.concept("If PING works, your connection is alive.")

        response = client.ping()
        self.log.command("PING")
        self.log.output(str(response))
        self.step_pause.pause("Verify PING returned True")
        results.append(response)

        # ── Step 2: SET and GET ─────────────────────────────────
        self.log.section("Step 2: SET and GET")
        self.log.concept("SET stores a string value under a key.")
        self.log.concept("GET retrieves the value. Returns None if the key doesn't exist.")

        client.set("name", "Alice")
        self.log.command('SET name "Alice"')
        self.log.output("OK")

        value = client.get("name")
        self.log.command("GET name")
        self.log.output(str(value))
        results.append(value)

        # GET on a non-existent key
        missing = client.get("no_such_key")
        self.log.command("GET no_such_key")
        self.log.output(str(missing))
        self.log.concept("GET returns None for keys that don't exist — no error.")
        results.append(missing)

        # ── Step 3: Multiple keys and EXISTS ────────────────────
        self.log.section("Step 3: Multiple Keys and EXISTS")
        self.log.concept("EXISTS checks whether one or more keys exist.")
        self.log.concept("It returns the count of keys that exist.")

        client.set("city", "San Francisco")
        client.set("language", "Python")
        self.log.command('SET city "San Francisco"')
        self.log.command('SET language "Python"')

        count1 = client.exists("city")
        self.log.command("EXISTS city")
        self.log.output(f"Returns {count1} (1 = exists)")

        count2 = client.exists("city", "language", "no_such_key")
        self.log.command("EXISTS city language no_such_key")
        self.log.output(f"Returns {count2} (2 of the 3 keys exist)")
        results.extend([count1, count2])

        # ── Step 4: Key expiration and TTL ─────────────────────
        self.log.section("Step 4: Key Expiration")
        self.log.concept("EXPIRE sets a time-to-live in seconds on a key.")
        self.log.concept("TTL returns remaining seconds: positive = expiring, -1 = persistent, -2 = gone.")

        client.set("temp", "I will disappear")
        client.expire("temp", 10)
        self.log.command('SET temp "I will disappear"')
        self.log.command("EXPIRE temp 10")

        ttl1 = client.ttl("temp")
        self.log.command("TTL temp")
        self.log.output(f"Returns ~10 seconds: {ttl1}")
        self.log.concept(f"TTL returned {ttl1} — the key will expire in about 10 seconds.")

        # TTL on a persistent key (no expiry)
        ttl2 = client.ttl("name")
        self.log.command("TTL name")
        self.log.output(f"Returns {ttl2} (-1 = no expiry, persistent)")
        self.log.concept("TTL returns -1 when a key has no expiry set.")

        results.extend([ttl1, ttl2])

        # ── Step 5: Delete a key ────────────────────────────────
        self.log.section("Step 5: Delete a Key")
        self.log.concept("DEL removes keys and returns the count of keys deleted.")
        self.log.concept("After deletion, EXISTS returns 0 and TTL returns -2.")

        deleted = client.delete("city")
        self.log.command("DEL city")
        self.log.output(f"Deleted {deleted} key(s)")

        exists_after = client.exists("city")
        ttl_after = client.ttl("city")
        self.log.command("EXISTS city")
        self.log.output(f"Returns {exists_after} (0 = gone)")
        self.log.command("TTL city")
        self.log.output(f"Returns {ttl_after} (-2 = key doesn't exist)")
        results.extend([deleted, exists_after, ttl_after])

        # ── Step 6: KEYS and TYPE ───────────────────────────────
        self.log.section("Step 6: KEYS and TYPE")
        self.log.warn("KEYS scans the entire keyspace — O(N). Never use in production!")

        all_keys = client.keys("*")
        self.log.command("KEYS *")
        self.log.output(f"Found {len(all_keys)} keys: {sorted(all_keys)}")

        # Check types
        for key in sorted(all_keys):
            ktype = client.type(key)
            self.log.command(f"TYPE {key}")
            self.log.output(f"→ {ktype}")
        results.append(len(all_keys))

        # ── Summary ─────────────────────────────────────────────
        self.log.separator()
        self.log.success(
            f"Completed basic Redis CRUD: "
            f"PING={results[0]}, "
            f"GET name={results[1]!r}, "
            f"GET missing={results[2]!r}, "
            f"EXISTS city={results[3]}, "
            f"EXISTS multi={results[4]}, "
            f"TTL temp={results[5]}, "
            f"TTL persistent={results[6]}, "
            f"DEL count={results[7]}, "
            f"EXISTS after={results[8]}, "
            f"TTL after={results[9]}, "
            f"total keys={results[10]}"
        )

        return results
