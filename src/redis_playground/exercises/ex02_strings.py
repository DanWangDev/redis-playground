"""Exercise 02: Strings — counters, bulk ops, slicing, SETNX, APPEND."""

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner


class Ex02Strings(ExerciseRunner):
    def __init__(self):
        super().__init__("02-strings", "Strings")

    def run(self, client: redis.Redis) -> list:
        results = []

        # ── Step 1: Atomic counters ────────────────────────────
        self.log.section("Step 1: Atomic Counters")
        self.log.concept("INCR atomically increments a counter. No race conditions.")
        self.log.concept(
            "If the key doesn't exist, INCR creates it as 0 then increments to 1."
        )

        views = client.incr("article:42:views")
        self.log.command("INCR article:42:views")
        self.log.output(f"→ {views}")
        views2 = client.incr("article:42:views")
        self.log.command("INCR article:42:views (again)")
        self.log.output(f"→ {views2}")
        results.extend([views, views2])

        score = client.incrby("game:score", 100)
        self.log.command("INCRBY game:score 100")
        self.log.output(f"→ {score}")
        results.append(score)

        client.set("inventory:item:1", "50")
        remaining = client.decr("inventory:item:1")
        self.log.command("DECR inventory:item:1")
        self.log.output(f"→ {remaining}")
        results.append(remaining)

        # ── Step 2: Bulk MSET and MGET ─────────────────────────
        self.log.section("Step 2: Bulk MSET and MGET")
        client.mset(
            {
                "user:1:name": "Alice",
                "user:1:email": "alice@example.com",
                "user:1:plan": "pro",
            }
        )
        self.log.command(
            'MSET user:1:name "Alice" user:1:email "alice@example.com" user:1:plan "pro"'
        )
        values = client.mget(
            ["user:1:name", "user:1:email", "user:1:plan", "user:1:missing"]
        )
        self.log.command("MGET user:1:name user:1:email user:1:plan user:1:missing")
        self.log.output(str(values))
        results.extend(values)

        # ── Step 3: String slicing ─────────────────────────────
        self.log.section("Step 3: String Slicing")
        client.set("greeting", "Hello, World!")
        sub = client.getrange("greeting", 0, 4)
        self.log.command("GETRANGE greeting 0 4")
        self.log.output(f'→ "{sub}"')
        results.append(sub)

        length = client.strlen("greeting")
        self.log.command("STRLEN greeting")
        self.log.output(f"→ {length}")
        results.append(length)

        client.setrange("greeting", 7, "Redis")
        updated = client.get("greeting")
        self.log.command('SETRANGE greeting 7 "Redis"')
        self.log.output(f'→ "{updated}"')
        results.append(updated)

        # ── Step 4: SETNX ──────────────────────────────────────
        self.log.section("Step 4: SETNX — Atomic Set-If-Not-Exists")
        nx1 = client.setnx("lock:resource", "owner-1")
        nx2 = client.setnx("lock:resource", "owner-2")
        self.log.command('SETNX lock:resource "owner-1" → SETNX "owner-2"')
        self.log.output(f"→ {nx1} (acquired), {nx2} (already held)")
        results.extend([nx1, nx2])

        # ── Step 5: APPEND ─────────────────────────────────────
        self.log.section("Step 5: APPEND")
        client.set("log", "ERROR: connection lost\n")
        new_len = client.append("log", "ERROR: retry failed\n")
        self.log.command('APPEND log "ERROR: retry failed\\n"')
        self.log.output(f"New length: {new_len}")
        results.append(new_len)
        results.append(client.get("log"))

        self.log.separator()
        self.log.success(
            f"String ops: INCR={results[0]}→{results[1]}, INCRBY={results[2]}, "
            f"DECR={results[3]}, MGET={results[4:8]}, GETRANGE={results[8]!r}, "
            f"STRLEN={results[9]}, SETRANGE={results[10]!r}, "
            f"SETNX={results[11]}/{results[12]}"
        )
        return results
