"""Exercise 09: Transactions — MULTI/EXEC, WATCH optimistic locking, DISCARD."""

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner


class Ex09Transactions(ExerciseRunner):
    def __init__(self):
        super().__init__("09-transactions", "Transactions")

    def run(self, client: redis.Redis) -> list:
        results = {}

        self.log.section("Step 1: MULTI/EXEC — Atomic Batch")
        self.log.concept("Commands between MULTI and EXEC execute atomically.")
        pipe = client.pipeline(transaction=True)
        pipe.set("account:a", 100)
        pipe.set("account:b", 200)
        pipe.incrby("account:a", 50)
        pipe.decrby("account:b", 50)
        self.log.command(
            "MULTI → SET a=100, SET b=200, INCRBY a 50, DECRBY b 50 → EXEC"
        )
        tx_result = pipe.execute()
        self.log.output(f"Result: {tx_result}")
        a_bal = client.get("account:a")
        b_bal = client.get("account:b")
        self.log.output(f"account:a={a_bal}, account:b={b_bal}")
        results["tx_result"] = tx_result
        results["a_balance"] = a_bal
        results["b_balance"] = b_bal

        self.log.section("Step 2: DISCARD — Cancel Transaction")
        pipe2 = client.pipeline(transaction=True)
        pipe2.set("will_be_discarded", "should not exist")
        pipe2.discard()
        self.log.command("MULTI → SET → DISCARD")
        try:
            pipe2.execute()
        except Exception:
            pass
        exists = client.exists("will_be_discarded")
        self.log.output(f"EXISTS will_be_discarded → {exists}")
        results["discarded_exists"] = exists

        self.log.section("Step 3: WATCH — Optimistic Locking")
        client.set("account:c", 500)
        pipe3 = client.pipeline(transaction=True)
        pipe3.watch("account:c")
        current_val = int(client.get("account:c"))
        self.log.command(f"WATCH account:c → GET → {current_val}")

        # Another client modifies the key
        client.set("account:c", 999)
        self.log.warn("Another client changed account:c to 999!")

        pipe3.multi()
        pipe3.set("account:c", current_val - 100)
        try:
            watch_result = pipe3.execute()
        except redis.exceptions.WatchError:
            watch_result = None
        self.log.command(f"MULTI → SET account:c {current_val - 100} → EXEC")
        self.log.output(f"EXEC result: {watch_result} (None = aborted!)")
        final_val = client.get("account:c")
        self.log.output(f"Final value: {final_val} (should be 999)")
        results["watch_result"] = watch_result
        results["final_value"] = final_val

        self.log.separator()
        self.log.success(
            f"Tx: transfer={'OK' if tx_result else 'FAIL'}, WATCH aborted={watch_result is None}"
        )
        return results
