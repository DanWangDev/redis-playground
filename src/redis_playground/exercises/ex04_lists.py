"""Exercise 04: Lists.

Explore Redis list operations: queue (LPUSH+RPOP), stack (LPUSH+LPOP),
range inspection (LRANGE), capped collections (LTRIM),
blocking pops (BLPOP), and length (LLEN).
"""

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner


class Ex04Lists(ExerciseRunner):
    def __init__(self):
        super().__init__("04-lists", "Lists")

    def run(self, client: redis.Redis) -> list:
        results = []

        # ── Step 1: Queue pattern (FIFO) ───────────────────────
        self.log.section("Step 1: Queue (FIFO) — LPUSH + RPOP")
        self.log.concept(
            "A queue is First-In-First-Out: LPUSH adds to head, RPOP removes from tail."
        )
        self.log.concept("This is the classic task queue / message queue pattern.")

        client.rpush("queue:tasks", "task-1", "task-2", "task-3")
        self.log.command('RPUSH queue:tasks "task-1" "task-2" "task-3"')

        task = client.lpop("queue:tasks")
        self.log.command("LPOP queue:tasks")
        self.log.output(f"→ {task} (first in, first out)")
        results.append(task)

        # ── Step 2: Stack pattern (LIFO) ───────────────────────
        self.log.section("Step 2: Stack (LIFO) — LPUSH + LPOP")
        self.log.concept(
            "A stack is Last-In-First-Out: LPUSH adds to head, LPOP removes from head."
        )
        self.log.concept(
            "Useful for browser history, undo systems, expression evaluation."
        )

        client.lpush("stack:history", "page-1", "page-2", "page-3")
        self.log.command('LPUSH stack:history "page-1" "page-2" "page-3"')

        page = client.lpop("stack:history")
        self.log.command("LPOP stack:history")
        self.log.output(f"→ {page} (last in, first out)")
        results.append(page)

        # ── Step 3: Range inspection ───────────────────────────
        self.log.section("Step 3: LRANGE — Inspect List Contents")
        self.log.concept(
            "LRANGE start stop returns elements in the range (both inclusive)."
        )
        self.log.concept(
            "Use 0 -1 to get all elements. Negative indices count from the end."
        )

        client.delete("stack:history")
        client.rpush("fruits", "apple", "banana", "cherry", "date", "elderberry")
        self.log.command('RPUSH fruits "apple" "banana" "cherry" "date" "elderberry"')

        all_fruits = client.lrange("fruits", 0, -1)
        self.log.command("LRANGE fruits 0 -1")
        self.log.output(str(all_fruits))
        results.append(len(all_fruits))

        first_two = client.lrange("fruits", 0, 1)
        self.log.command("LRANGE fruits 0 1")
        self.log.output(str(first_two))

        last_two = client.lrange("fruits", -2, -1)
        self.log.command("LRANGE fruits -2 -1")
        self.log.output(str(last_two))
        results.extend([first_two, last_two])

        # ── Step 4: Capped collection ──────────────────────────
        self.log.section("Step 4: LTRIM — Capped Collection")
        self.log.concept("LTRIM keeps only a range of elements, discarding the rest.")
        self.log.concept(
            "Useful for activity feeds where you only need the most recent N items."
        )

        client.delete("activity")
        for i in range(1, 12):
            client.lpush("activity", f"event-{i}")
        self.log.command("LPUSH activity event-1 ... event-11")
        self.log.output(f"List now has {client.llen('activity')} events")

        client.ltrim("activity", 0, 4)
        self.log.command("LTRIM activity 0 4")
        recent = client.lrange("activity", 0, -1)
        self.log.output(f"After LTRIM, only newest 5: {recent}")
        results.append(client.llen("activity"))

        # ── Step 5: LLEN — Count elements ─────────────────────
        self.log.section("Step 5: LLEN — Element Count")
        length = client.llen("fruits")
        self.log.command("LLEN fruits")
        self.log.output(f"→ {length} fruits")
        results.append(length)

        # ── Summary ─────────────────────────────────────────────
        self.log.separator()
        self.log.success(
            f"List operations: queue pop={results[0]!r}, stack pop={results[1]!r}, "
            f"total fruits={results[2]}, trimmed count={results[5]}, fruit count={results[6]}"
        )
        return results
