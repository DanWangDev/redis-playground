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
            "Client-side caching requires RESP3 protocol and CLIENT TRACKING ON."
        )
        self.log.concept(
            "This feature requires a real Redis server — fakeredis doesn't support it."
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
        self.log.concept(
            "A local dict simulates the client-side cache. Redis tracks reads."
        )
        local_cache = {}
        client.set("user:profile:1", "Alice's Profile Data")
        self.log.command('SET user:profile:1 "Alice\'s Profile Data"')

        # Read and cache locally
        val = client.get("user:profile:1")
        local_cache["user:profile:1"] = val
        self.log.command("GET user:profile:1 → cached locally")
        self.log.output(f"Cached: user:profile:1 = {val!r}")
        results["cache_hit_value"] = val

        self.log.section("Step 3: Invalidation on Modification")
        self.log.concept(
            "When another client modifies the key, Redis pushes an invalidation message."
        )
        client.set("user:profile:1", "Updated Profile")
        self.log.command('SET user:profile:1 "Updated Profile" (modification)')
        self.log.concept(
            "In a real RESP3 setup, this would push an invalidation message to our listener."
        )
        self.log.output("Local cache should now be invalidated (stale)")
        results["invalidated"] = True

        client.execute_command("CLIENT", "TRACKING", "OFF")
        results["tracking_disabled"] = True

        self.log.separator()
        self.log.success("Client-side caching pattern demonstrated (conceptual)")
        return results
