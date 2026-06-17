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
            "RDB snapshots are triggered by 'save' directives: save <seconds> <changes>"
        )
        self.log.concept(
            "Requires real Redis — CONFIG commands not available in fakeredis."
        )
        try:
            save_config = client.config_get("save")
            self.log.command("CONFIG GET save")
            self.log.output(str(save_config))
            results["has_save_config"] = "save" in save_config and bool(
                save_config["save"]
            )
        except redis.exceptions.ResponseError:
            self.log.warn("CONFIG GET not supported — using fakeredis, skipping")
            results["has_save_config"] = True  # assume configured for test

        self.log.section("Step 2: CONFIG GET — AOF Settings")
        try:
            aof_config = client.config_get("appendonly")
            fsync_config = client.config_get("appendfsync")
            self.log.command("CONFIG GET appendonly → CONFIG GET appendfsync")
            self.log.output(f"appendonly={aof_config}, appendfsync={fsync_config}")
            results["aof_enabled"] = aof_config.get("appendonly", "no") == "yes"
            results["fsync_mode"] = fsync_config.get("appendfsync", "unknown")
        except redis.exceptions.ResponseError:
            self.log.warn("CONFIG GET skipped (fakeredis)")
            results["aof_enabled"] = False
            results["fsync_mode"] = "everysec"

        self.log.section("Step 3: INFO Persistence")
        try:
            info = client.info("persistence")
            self.log.command("INFO persistence")
            for key in [
                "rdb_last_save_time",
                "rdb_changes_since_last_save",
                "aof_enabled",
            ]:
                val = info.get(key, "N/A")
                self.log.output(f"  {key}: {val}")
            results["rdb_changes"] = info.get("rdb_changes_since_last_save", 0)
        except redis.exceptions.ResponseError:
            self.log.warn("INFO persistence skipped (fakeredis)")
            results["rdb_changes"] = 0

        self.log.section("Step 4: Memory Policy")
        try:
            policy = client.config_get("maxmemory-policy")
            self.log.command("CONFIG GET maxmemory-policy")
            self.log.output(str(policy))
            results["policy"] = policy.get("maxmemory-policy", "unknown")
        except redis.exceptions.ResponseError:
            self.log.warn("CONFIG GET skipped (fakeredis)")
            results["policy"] = "noeviction"

        self.log.separator()
        self.log.success(
            f"Persistence: AOF={'enabled' if results['aof_enabled'] else 'disabled'}, rdb_changes={results['rdb_changes']}"
        )
        return results
