"""Exercise 22: SCAN — cursor-based safe iteration for large datasets."""

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner


class Ex22Scan(ExerciseRunner):
    def __init__(self):
        super().__init__("22-scan", "SCAN")

    def run(self, client: redis.Redis) -> dict:
        results = {}

        self.log.section("Step 1: KEYS vs SCAN — Why SCAN Matters")
        self.log.concept(
            "KEYS * blocks the server. SCAN iterates in small batches — production-safe."
        )
        self.log.concept("We'll seed 50 keys and compare both approaches.")

        # Seed keys
        for i in range(50):
            client.set(f"item:{i:03d}", f"value-{i}")
        self.log.command("SET item:000..item:049 (50 keys seeded)")

        self.log.section("Step 2: SCAN — Iterate All Keys")
        cursor = 0
        all_keys = []
        iterations = 0
        while True:
            cursor, batch = client.scan(cursor, match="item:*", count=10)
            all_keys.extend(batch)
            iterations += 1
            if cursor == 0:
                break
        self.log.command("SCAN 0 MATCH item:* COUNT 10 (looped until cursor=0)")
        self.log.output(f"Found {len(all_keys)} keys in {iterations} SCAN iterations")
        results["scan_total"] = len(all_keys)
        results["scan_iterations"] = iterations

        self.log.section("Step 3: HSCAN — Iterate Hash Fields")
        client.hset("hash:big", mapping={f"field:{i}": str(i) for i in range(20)})
        self.log.command("HSET hash:big (20 fields)")
        cursor = 0
        hash_fields = []
        while True:
            cursor, batch = client.hscan("hash:big", cursor, count=5)
            hash_fields.extend(batch)
            if cursor == 0:
                break
        self.log.command("HSCAN hash:big 0 COUNT 5 (looped)")
        self.log.output(f"Found {len(hash_fields)} field-value pairs")
        results["hscan_total"] = len(hash_fields)

        self.log.section("Step 4: SSCAN — Iterate Set Members")
        client.sadd("set:big", *[f"member:{i}" for i in range(15)])
        self.log.command("SADD set:big (15 members)")
        cursor = 0
        set_members = []
        while True:
            cursor, batch = client.sscan("set:big", cursor, count=5)
            set_members.extend(batch)
            if cursor == 0:
                break
        self.log.command("SSCAN set:big 0 COUNT 5 (looped)")
        self.log.output(f"Found {len(set_members)} members")
        results["sscan_total"] = len(set_members)

        self.log.section("Step 5: ZSCAN — Iterate Sorted Set with Scores")
        pairs = {f"item:{i}": float(i) for i in range(10)}
        client.zadd("zset:big", pairs)
        self.log.command("ZADD zset:big (10 members)")
        cursor = 0
        zset_results = []
        while True:
            cursor, batch = client.zscan("zset:big", cursor, count=3)
            zset_results.extend(batch)
            if cursor == 0:
                break
        self.log.command("ZSCAN zset:big 0 COUNT 3 (looped)")
        self.log.output(f"Found {len(zset_results)} member-score pairs")
        results["zscan_total"] = len(zset_results)

        self.log.separator()
        self.log.success(
            f"SCAN: {results['scan_total']} keys in {iterations} iters, "
            f"HSCAN={results['hscan_total']}, SSCAN={results['sscan_total']}, ZSCAN={results['zscan_total']}"
        )
        return results
