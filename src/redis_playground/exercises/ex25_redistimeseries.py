"""Exercise 25: RedisTimeSeries — time-series data with automatic downsampling (Redis Stack)."""

import time
import redis

from redis_playground.shared.exercise_runner import ExerciseRunner


class Ex25RedisTimeSeries(ExerciseRunner):
    def __init__(self):
        super().__init__("25-redistimeseries", "RedisTimeSeries")

    def run(self, client: redis.Redis) -> dict:
        results = {}

        self.log.section("Step 1: TS.CREATE — Create a Time-Series")
        self.log.concept("TS.CREATE defines a time-series key with retention and labels.")
        self.log.concept("Requires Redis Stack — may not be available in plain Redis.")
        try:
            try:
                client.execute_command("TS.DEL", "ts:sensor:1")
            except redis.exceptions.ResponseError:
                pass
            client.execute_command("TS.CREATE", "ts:sensor:1", "RETENTION", "86400000")
            self.log.command("TS.CREATE ts:sensor:1 RETENTION 86400000 (24h)")
            self.log.success("Time-series created")
        except redis.exceptions.ResponseError as e:
            self.log.warn(f"TS.CREATE not available: {e}")
            results["ts_available"] = False
            self.log.separator()
            self.log.success("RedisTimeSeries requires Redis Stack")
            return results

        results["ts_available"] = True

        self.log.section("Step 2: TS.ADD — Add Data Points")
        now = int(time.time() * 1000)
        client.execute_command("TS.ADD", "ts:sensor:1", str(now), "23.5")
        client.execute_command("TS.ADD", "ts:sensor:1", str(now + 60000), "24.1")
        client.execute_command("TS.ADD", "ts:sensor:1", str(now + 120000), "25.0")
        client.execute_command("TS.ADD", "ts:sensor:1", str(now + 180000), "24.8")
        self.log.command("TS.ADD ts:sensor:1 (4 data points)")
        results["points_added"] = 4

        self.log.section("Step 3: TS.RANGE — Query Range")
        data = client.execute_command("TS.RANGE", "ts:sensor:1", str(now), str(now + 200000))
        self.log.command("TS.RANGE ts:sensor:1 (full range)")
        for dp in data:
            self.log.output(f"  ts={dp[0]}, val={dp[1]}")
        results["range_count"] = len(data)

        self.log.section("Step 4: Aggregated Query")
        agg = client.execute_command(
            "TS.RANGE", "ts:sensor:1", str(now), str(now + 200000),
            "AGGREGATION", "avg", "120000"
        )
        self.log.command("TS.RANGE ts:sensor:1 ... AGGREGATION avg 120000")
        self.log.output(f"Aggregated buckets: {len(agg)}")
        for bucket in agg:
            self.log.output(f"  ts={bucket[0]}, avg={bucket[1]}")
        results["agg_buckets"] = len(agg)

        client.execute_command("TS.DEL", "ts:sensor:1")

        self.log.separator()
        self.log.success(f"RedisTimeSeries: {results['range_count']} points, {results['agg_buckets']} buckets")
        return results
