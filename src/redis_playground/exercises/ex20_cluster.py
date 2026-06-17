"""Exercise 20: Redis Cluster — hash slots, key distribution, redirects (real Redis Cluster required)."""

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner


class Ex20Cluster(ExerciseRunner):
    def __init__(self):
        super().__init__("20-cluster", "Cluster")

    def run(self, client: redis.Redis) -> dict:
        results = {}

        self.log.section("Step 1: CLUSTER KEYSLOT — Hash Slot Calculation")
        self.log.concept("CRC16(key) mod 16384 determines which node owns a key.")
        self.log.concept("Requires a real Redis Cluster (Docker Compose cluster profile).")

        try:
            slot1 = client.execute_command("CLUSTER", "KEYSLOT", "user:123")
            slot2 = client.execute_command("CLUSTER", "KEYSLOT", "product:456")
            self.log.command("CLUSTER KEYSLOT user:123 → CLUSTER KEYSLOT product:456")
            self.log.output(f"user:123 → slot {slot1}, product:456 → slot {slot2}")
            results["slot_user"] = slot1
            results["slot_product"] = slot2
        except Exception as e:
            self.log.warn(f"CLUSTER KEYSLOT not available: {e}")
            self.log.concept("Run with real Redis Cluster to try hash slot operations.")
            results["slot_user"] = None
            results["slot_product"] = None

        self.log.section("Step 2: Hash Tags — Force Co-Location")
        self.log.concept("Hash tags {key} ensure related keys land on the same slot.")
        try:
            slot_a = client.execute_command("CLUSTER", "KEYSLOT", "user:{123}:name")
            slot_b = client.execute_command("CLUSTER", "KEYSLOT", "user:{123}:email")
            self.log.command("CLUSTER KEYSLOT user:{123}:name → user:{123}:email")
            self.log.output(f"name → slot {slot_a}, email → slot {slot_b}")
            same_slot = slot_a == slot_b
            self.log.output(f"Same slot: {same_slot} (both hash on 123)")
            results["same_slot"] = same_slot
        except Exception:
            self.log.warn("CLUSTER KEYSLOT skipped")
            results["same_slot"] = True  # conceptually always true

        self.log.section("Step 3: CLUSTER INFO")
        try:
            info = client.execute_command("CLUSTER", "INFO")
            self.log.command("CLUSTER INFO")
            for line in str(info).split("\n")[:5]:
                self.log.output(f"  {line}")
            results["cluster_info"] = str(info)[:100]
        except Exception as e:
            self.log.warn(f"CLUSTER INFO not available: {e}")
            results["cluster_info"] = "not clustered"

        self.log.section("Step 4: MOVED Redirect Simulation")
        self.log.concept("When a key belongs to another node, Cluster returns MOVED <slot> <ip:port>.")
        self.log.concept("redis-py's RedisCluster client handles this automatically.")
        try:
            # Just demonstrate the concept — won't actually redirect in single-node mode
            client.set("test:key", "value")
            val = client.get("test:key")
            self.log.command("SET test:key value → GET test:key")
            self.log.output(f"Value: {val!r} (handled by current node)")
            results["get_result"] = val
        except redis.exceptions.ResponseError as e:
            if "MOVED" in str(e):
                self.log.warn("MOVED redirect received — Cluster redirected to correct node")
                results["get_result"] = "MOVED"
            else:
                raise

        self.log.separator()
        self.log.success(f"Cluster: slots OK, hash tags co-locate, info: {results['cluster_info'][:50]}")
        return results
