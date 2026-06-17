"""Exercise 15: Persistence — RDB, AOF, durability configuration (real Redis only)."""

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner


class Ex15Persistence(ExerciseRunner):
    def __init__(self):
        super().__init__("15-persistence", "Persistence")

    def run(self, client: redis.Redis) -> dict:
        results = {}

        self.log.section("Step 1: CONFIG GET — RDB Snapshot Settings")
        self.log.concept(
            "RDB snapshots triggered by 'save' directives. Requires real Redis."
        )
        try:
            save_config = client.config_get("save")
            self.log.command("CONFIG GET save")
            self.log.output(str(save_config))
            results["has_save_config"] = bool(save_config.get("save"))
        except redis.exceptions.ResponseError:
            self.log.warn("CONFIG GET skipped (fakeredis)")
            results["has_save_config"] = True

        self.log.section("Step 2: AOF Settings")
        try:
            aof = client.config_get("appendonly")
            fsync = client.config_get("appendfsync")
            self.log.command("CONFIG GET appendonly → CONFIG GET appendfsync")
            self.log.output(f"appendonly={aof}, appendfsync={fsync}")
            results["fsync_mode"] = fsync.get("appendfsync", "unknown")
        except redis.exceptions.ResponseError:
            self.log.warn("CONFIG GET skipped (fakeredis)")
            results["fsync_mode"] = "everysec"

        self.log.section("Step 3: INFO Persistence")
        try:
            info = client.info("persistence")
            self.log.command("INFO persistence")
            for k in ["rdb_changes_since_last_save", "aof_enabled"]:
                self.log.output(f"  {k}: {info.get(k, 'N/A')}")
            results["rdb_changes"] = info.get("rdb_changes_since_last_save", 0)
        except redis.exceptions.ResponseError:
            self.log.warn("INFO persistence skipped (fakeredis)")
            results["rdb_changes"] = 0

        self.log.separator()
        self.log.success(f"Persistence: fsync={results['fsync_mode']}")
        return results
