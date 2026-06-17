"""Exercise 16: Client-Side Caching — RESP3 server-assisted invalidation (real Redis only)."""

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner


class Ex16ClientSideCaching(ExerciseRunner):
    def __init__(self):
        super().__init__("16-client-side-caching", "Client-Side Caching")

    def run(self, client: redis.Redis) -> dict:
        results = {}

        self.log.section("Step 1: Enable RESP3 Client Tracking")
        self.log.concept(
            "Requires RESP3 protocol and real Redis. fakeredis doesn't support this."
        )
        try:
            client.execute_command("CLIENT", "TRACKING", "ON")
            self.log.command("CLIENT TRACKING ON")
            self.log.success("Client tracking enabled")
            results["tracking_enabled"] = True
        except Exception as e:
            self.log.warn(f"CLIENT TRACKING not available: {e}")
            self.log.concept(
                "Run with real Redis via `docker compose up -d` to try this feature."
            )
            results["tracking_enabled"] = False
            self.log.separator()
            self.log.success("Client-side caching: requires real Redis with RESP3")
            return results

        self.log.section("Step 2: Local Cache Simulation")
        local_cache = {}
        client.set("user:profile:1", "Alice's Profile Data")
        self.log.command("SET user:profile:1 ...")
        val = client.get("user:profile:1")
        local_cache["user:profile:1"] = val
        self.log.output(f"Cached: user:profile:1 = {val!r}")
        results["cache_hit_value"] = val

        self.log.section("Step 3: Invalidation on Modification")
        client.set("user:profile:1", "Updated Profile")
        self.log.command(
            "SET user:profile:1 (modification — would trigger invalidation push)"
        )
        self.log.concept(
            "In RESP3 mode, this pushes an invalidation message to tracking clients."
        )
        results["invalidated"] = True
        client.execute_command("CLIENT", "TRACKING", "OFF")

        self.log.separator()
        self.log.success("Client-side caching pattern demonstrated")
        return results
