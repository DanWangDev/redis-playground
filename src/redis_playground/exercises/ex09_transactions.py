"""Exercise 09: Transactions.

Explore Redis transactions: MULTI/EXEC for atomic command batching,
WATCH for optimistic locking, and DISCARD for cancellation.
"""

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner


class Ex09Transactions(ExerciseRunner):
    def __init__(self):
        super().__init__("09-transactions", "Transactions")

    def run(self, client: redis.Redis) -> list:
        results = []

        # ── Step 1: MULTI/EXEC — Atomic batch ──────────────────
        self.log.section("Step 1: MULTI/EXEC — Atomic Command Batch")
        self.log.concept(
            "Commands between MULTI and EXEC are queued, then executed atomically."
        )
        self.log.concept(
            "No other client can see intermediate state between the commands."
        )

        pipeline = client.pipeline(transaction=True)
        pipeline.set("account:a", 100)
        pipeline.set("account:b", 200)
        pipeline.incrby("account:a", 50)
        pipeline.decrby("account:b", 50)
        self.log.command("MULTI")
        self.log.command("SET account:a 100")
        self.log.command("SET account:b 200")
        self.log.command("INCRBY account:a 50")
        self.log.command("DECRBY account:b 50")
        self.log.command("EXEC")

        result = pipeline.execute()
        self.log.output(f"Transaction result: {result}")
        self.log.concept(
            "account:a = 150, account:b = 150 — transfer complete, atomically."
        )

        a_balance = client.get("account:a")
        b_balance = client.get("account:b")
        self.log.command("GET account:a")
        self.log.output(f"→ {a_balance}")
        self.log.command("GET account:b")
        self.log.output(f"→ {b_balance}")
        results.extend([result, a_balance, b_balance])

        # ── Step 2: DISCARD — Cancel a transaction ─────────────
        self.log.section("Step 2: DISCARD — Cancel a Transaction")
        self.log.concept(
            "DISCARD aborts the transaction — queued commands are never executed."
        )

        pipeline = client.pipeline(transaction=True)
        pipeline.set("will_be_discarded", "should not exist")
        pipeline.discard()
        self.log.command("MULTI")
        self.log.command('SET will_be_discarded "should not exist"')
        self.log.command("DISCARD")

        # Try to execute — should error since we already discarded
        try:
            pipeline.execute()
        except Exception:
            pass

        exists = client.exists("will_be_discarded")
        self.log.command("EXISTS will_be_discarded")
        self.log.output(f"→ {exists} (0 = never created)")
        results.append(exists)

        # ── Step 3: WATCH — Optimistic locking ─────────────────
        self.log.section("Step 3: WATCH — Optimistic Locking")
        self.log.concept(
            "WATCH monitors a key. If the key changes before EXEC, the transaction aborts."
        )
        self.log.concept(
            "This implements optimistic concurrency control — try, check, retry if needed."
        )

        # Set up account
        client.set("account:c", 500)
        self.log.command("SET account:c 500")

        # Create two connections: one for the "other client", one for our transaction
        other = client  # same client for simplicity in fakeredis

        # Phase 1: WATCH and read
        pipeline = client.pipeline(transaction=True)
        pipeline.watch("account:c")
        current_val = int(client.get("account:c"))
        self.log.command("WATCH account:c")
        self.log.command("GET account:c")
        self.log.output(f"Current value: {current_val}")

        # Phase 2: Another client modifies the watched key
        other.set("account:c", 999)
        self.log.warn("Another client changed account:c to 999!")
        self.log.output(f"account:c is now: {other.get('account:c')}")

        # Phase 3: Try to execute transaction — should abort
        pipeline.multi()
        pipeline.set("account:c", current_val - 100)
        try:
            exec_result = pipeline.execute()
        except redis.exceptions.WatchError:
            exec_result = None  # WATCH detected change — transaction aborted
        self.log.command(f"MULTI → SET account:c {current_val - 100} → EXEC")
        self.log.output(f"EXEC result: {exec_result} (None = aborted!)")
        self.log.concept(
            "The WATCH detected the change — transaction aborted to prevent lost update."
        )

        final_val = client.get("account:c")
        self.log.output(
            f"Final value: {final_val} (should be 999, not {current_val - 100})"
        )
        results.extend([exec_result, final_val])

        # ── Summary ─────────────────────────────────────────────
        self.log.separator()
        self.log.success(
            f"Transactions: transfer result={results[0]}, "
            f"balances={results[1]}/{results[2]}, "
            f"discarded={results[3]}, "
            f"WATCH abort={results[4]}, final={results[5]}"
        )
        return results
