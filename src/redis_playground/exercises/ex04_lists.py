"""Exercise 04: Lists — queue, stack, range, capped collections."""

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner


class Ex04Lists(ExerciseRunner):
    def __init__(self):
        super().__init__("04-lists", "Lists")

    def run(self, client: redis.Redis) -> list:
        results = []

        # ── Step 1: Queue (FIFO) ───────────────────────────────
        self.log.section("Step 1: Queue (FIFO) — RPUSH + LPOP")
        self.log.concept(
            "RPUSH adds to tail, LPOP removes from head — First In, First Out."
        )

        client.rpush("queue:tasks", "task-1", "task-2", "task-3")
        self.log.command('RPUSH queue:tasks "task-1" "task-2" "task-3"')
        task = client.lpop("queue:tasks")
        self.log.command("LPOP queue:tasks")
        self.log.output(f"→ {task} (first in, first out)")
        results.append(task)

        # ── Step 2: Stack (LIFO) ───────────────────────────────
        self.log.section("Step 2: Stack (LIFO) — LPUSH + LPOP")
        self.log.concept(
            "LPUSH adds to head, LPOP removes from head — Last In, First Out."
        )

        client.lpush("stack:history", "page-1", "page-2", "page-3")
        self.log.command('LPUSH stack:history "page-1" "page-2" "page-3"')
        page = client.lpop("stack:history")
        self.log.command("LPOP stack:history")
        self.log.output(f"→ {page} (last in, first out)")
        results.append(page)

        # ── Step 3: LRANGE — inspect contents ──────────────────
        self.log.section("Step 3: LRANGE — Inspect List Contents")
        client.delete("fruits")
        client.rpush("fruits", "apple", "banana", "cherry", "date", "elderberry")
        self.log.command('RPUSH fruits "apple" "banana" "cherry" "date" "elderberry"')

        all_fruits = client.lrange("fruits", 0, -1)
        first_two = client.lrange("fruits", 0, 1)
        last_two = client.lrange("fruits", -2, -1)
        self.log.command("LRANGE fruits 0 -1 → LRANGE 0 1 → LRANGE -2 -1")
        self.log.output(f"all={all_fruits}, first2={first_two}, last2={last_two}")
        results.extend([len(all_fruits), first_two, last_two])

        # ── Step 4: LTRIM — capped collection ──────────────────
        self.log.section("Step 4: LTRIM — Capped Collection")
        client.delete("activity")
        for i in range(1, 12):
            client.lpush("activity", f"event-{i}")
        self.log.command("LPUSH activity event-1 ... event-11")
        self.log.output(f"Before trim: {client.llen('activity')} events")

        client.ltrim("activity", 0, 4)
        recent = client.lrange("activity", 0, -1)
        self.log.command("LTRIM activity 0 4")
        self.log.output(f"After trim: {recent}")
        results.append(client.llen("activity"))

        # ── Step 5: LLEN ───────────────────────────────────────
        self.log.section("Step 5: LLEN — Count Elements")
        length = client.llen("fruits")
        self.log.command("LLEN fruits")
        self.log.output(f"→ {length}")
        results.append(length)

        self.log.separator()
        self.log.success(
            f"List ops: queue={results[0]!r}, stack={results[1]!r}, "
            f"fruits={results[2]}, trimmed={results[5]}, len={results[6]}"
        )
        return results
