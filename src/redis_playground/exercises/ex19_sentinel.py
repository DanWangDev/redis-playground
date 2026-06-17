"""Exercise 19: Redis Sentinel — high availability, failover, discovery (real Redis + Sentinel required)."""

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner


class Ex19Sentinel(ExerciseRunner):
    def __init__(self):
        super().__init__("19-sentinel", "Sentinel")

    def run(self, client: redis.Redis) -> dict:
        results = {}

        self.log.section("Step 1: Sentinel Discovery")
        self.log.concept(
            "Sentinel tracks the current master — clients ask Sentinel, not a fixed IP."
        )
        self.log.concept(
            "Requires a real Redis + Sentinel setup (Docker Compose with sentinel profile)."
        )

        try:
            master_info = client.execute_command(
                "SENTINEL", "get-master-addr-by-name", "mymaster"
            )
            self.log.command("SENTINEL get-master-addr-by-name mymaster")
            self.log.output(f"Current master: {master_info}")
            results["master_addr"] = master_info
        except Exception as e:
            self.log.warn(f"SENTINEL not available: {e}")
            self.log.concept(
                "Run with `docker compose -f docker-compose.yml -f docker-compose.sentinel.yml up -d`"
            )
            results["master_addr"] = None

        self.log.section("Step 2: Sentinel Replicas Discovery")
        try:
            replicas = client.execute_command("SENTINEL", "replicas", "mymaster")
            self.log.command("SENTINEL replicas mymaster")
            replica_names = (
                [r.get("name", "unknown") for r in replicas] if replicas else []
            )
            self.log.output(f"Replicas: {replica_names}")
            results["replica_count"] = len(replicas) if replicas else 0
        except Exception:
            self.log.warn(
                "SENTINEL replicas not available (requires real Redis + Sentinel)"
            )
            results["replica_count"] = 0

        self.log.section("Step 3: INFO Replication Status")
        self.log.concept(
            "INFO replication shows whether this instance is master or replica."
        )
        try:
            info = client.info("replication")
            role = info.get("role", "unknown")
            connected = info.get("connected_slaves", 0)
            self.log.command("INFO replication")
            self.log.output(f"Role: {role}, Connected replicas: {connected}")
            results["role"] = role
            results["connected_replicas"] = connected
        except Exception:
            self.log.warn("INFO replication skipped")
            results["role"] = "unknown"

        self.log.separator()
        self.log.success(
            f"Sentinel: role={results['role']}, replicas={results.get('replica_count', 0)}"
        )
        return results
