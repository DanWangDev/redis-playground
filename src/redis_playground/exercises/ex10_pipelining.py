"""Exercise 10: Pipelining — RTT reduction, performance comparison, non-atomic demo."""

import time

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner


class Ex10Pipelining(ExerciseRunner):
    def __init__(self):
        super().__init__("10-pipelining", "Pipelining")

    def run(self, client: redis.Redis) -> dict:
        results = {}
        N = 100

        self.log.section("Step 1: Sequential Commands (N RTTs)")
        self.log.concept(
            "Each SET requires a separate round-trip. N commands = N×RTT overhead."
        )
        start = time.perf_counter()
        for i in range(N):
            client.set(f"seq:{i}", f"value-{i}")
        seq_time = time.perf_counter() - start
        self.log.command(f"SET seq:0..seq:{N - 1} (sequential)")
        self.log.output(f"Time: {seq_time:.4f}s ({seq_time / N * 1000:.2f}ms per SET)")
        for i in range(N):
            client.delete(f"seq:{i}")
        results["seq_time"] = seq_time

        self.log.section("Step 2: Pipelined Commands (1 RTT)")
        self.log.concept(
            "Pipeline sends all commands at once, reads all replies at once."
        )
        start = time.perf_counter()
        pipe = client.pipeline(transaction=False)
        for i in range(N):
            pipe.set(f"pipe:{i}", f"value-{i}")
        pipe.execute()
        pipe_time = time.perf_counter() - start
        self.log.command(f"pipeline SET pipe:0..pipe:{N - 1}")
        self.log.output(
            f"Time: {pipe_time:.4f}s ({pipe_time / N * 1000:.2f}ms per SET)"
        )
        speedup = seq_time / pipe_time if pipe_time > 0 else float("inf")
        self.log.success(f"Speedup: {speedup:.1f}x")
        for i in range(N):
            client.delete(f"pipe:{i}")
        results["pipe_time"] = pipe_time
        results["speedup"] = speedup

        self.log.section("Step 3: Pipelines Are NOT Atomic")
        self.log.concept(
            "Unlike MULTI/EXEC, other commands can interleave between pipeline commands."
        )
        client.set("counter", "0")
        pipe1 = client.pipeline(transaction=False)
        pipe1.get("counter")
        pipe1.incr("counter")
        pipe1.execute()

        client.incr("counter")  # interleaves!

        pipe2 = client.pipeline(transaction=False)
        pipe2.get("counter")
        pipe2.incr("counter")
        pipe2.execute()

        final = client.get("counter")
        self.log.command("Pipeline A incr → manual incr → Pipeline B incr")
        self.log.output(f"Final counter: {final} (3 = interleaved, not atomic)")
        results["counter"] = final

        self.log.section("Step 4: Pipeline for Batch Reads")
        client.mset({f"user:{i}:name": f"user-{i}" for i in range(10)})
        pipe = client.pipeline(transaction=False)
        for i in range(10):
            pipe.get(f"user:{i}:name")
        names = pipe.execute()
        self.log.command("Pipeline: GET user:0:name ... user:9:name")
        self.log.output(f"Results: {names[:5]}... (10 total)")
        results["batch_reads"] = len(names)

        self.log.separator()
        self.log.success(
            f"Pipelining: seq={seq_time:.4f}s, pipeline={pipe_time:.4f}s, speedup={speedup:.1f}x"
        )
        return results
