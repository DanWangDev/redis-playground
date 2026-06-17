"""Exercise 10: Pipelining.

Explore Redis pipelining: batching commands to reduce round-trips,
performance comparison vs sequential, and non-atomic behavior.
"""

import time

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner


class Ex10Pipelining(ExerciseRunner):
    def __init__(self):
        super().__init__("10-pipelining", "Pipelining")

    def run(self, client: redis.Redis) -> list:
        results = []

        # ── Step 1: Sequential commands (1 RTT each) ────────────
        self.log.section("Step 1: Sequential Commands (1 RTT each)")
        self.log.concept("Each SET requires a separate network round-trip.")
        self.log.concept("For N commands: N × RTT latency overhead.")

        ITERATIONS = 100

        start = time.perf_counter()
        for i in range(ITERATIONS):
            client.set(f"seq:{i}", f"value-{i}")
        seq_time = time.perf_counter() - start

        self.log.command(f"SET seq:0..seq:{ITERATIONS - 1} (sequentially)")
        self.log.output(
            f"Time: {seq_time:.4f}s ({seq_time / ITERATIONS * 1000:.2f}ms per SET)"
        )
        results.append(seq_time)

        # Clean up
        for i in range(ITERATIONS):
            client.delete(f"seq:{i}")

        self.step_pause.pause()

        # ── Step 2: Pipelined commands (1 RTT total) ────────────
        self.log.section("Step 2: Pipelined Commands (1 RTT total)")
        self.log.concept(
            "Pipeline sends all commands at once, reads all replies at once."
        )
        self.log.concept(
            "N commands → 1 RTT. Speedup is ~N× for network-bound workloads."
        )

        start = time.perf_counter()
        pipe = client.pipeline(transaction=False)
        for i in range(ITERATIONS):
            pipe.set(f"pipe:{i}", f"value-{i}")
        pipe.execute()
        pipe_time = time.perf_counter() - start

        self.log.command(f"pipeline SET pipe:0..pipe:{ITERATIONS - 1}")
        self.log.output(
            f"Time: {pipe_time:.4f}s ({pipe_time / ITERATIONS * 1000:.2f}ms per SET)"
        )

        speedup = seq_time / pipe_time if pipe_time > 0 else float("inf")
        self.log.success(f"Pipeline speedup: {speedup:.1f}x faster!")
        results.append(speedup)

        # Clean up
        for i in range(ITERATIONS):
            client.delete(f"pipe:{i}")

        self.step_pause.pause()

        # ── Step 3: Pipelining is NOT atomic ────────────────────
        self.log.section("Step 3: Pipelines Are NOT Atomic")
        self.log.concept("Unlike MULTI/EXEC, pipelined commands are NOT isolated.")
        self.log.concept(
            "Other clients' commands can interleave between pipelined commands."
        )

        pipe = client.pipeline(transaction=False)
        pipe.set("counter", "0")
        pipe.execute()

        # Simulate: two clients both read counter in a pipeline
        pipe1 = client.pipeline(transaction=False)
        pipe1.get("counter")
        pipe1.incr("counter")
        results1 = pipe1.execute()

        self.log.command("Pipeline A: GET counter → INCR counter")
        self.log.output(f"Results: {results1}")

        # Another increment happens between pipelines (or in parallel)
        client.incr("counter")
        self.log.command("(Another client INCRs counter concurrently)")

        pipe2 = client.pipeline(transaction=False)
        pipe2.get("counter")
        pipe2.incr("counter")
        results2 = pipe2.execute()

        self.log.command("Pipeline B: GET counter → INCR counter")
        self.log.output(f"Results: {results2}")

        final = client.get("counter")
        self.log.output(f"Final counter: {final}")
        self.log.concept(
            "Counter is 3 — both pipelines and the manual increment ran, interleaved."
        )
        results.append(final)

        # ── Step 4: Pipeline for reads too ──────────────────────
        self.log.section("Step 4: Pipeline for Batch Reads")
        self.log.concept(
            "Pipelines work for reads too — batch multiple GETs into one RTT."
        )

        client.mset({f"user:{i}:name": f"user-{i}" for i in range(10)})

        pipe = client.pipeline(transaction=False)
        for i in range(10):
            pipe.get(f"user:{i}:name")
        names = pipe.execute()

        self.log.command("Pipeline: GET user:0:name ... user:9:name")
        self.log.output(f"Results: {names[:5]}... (10 total)")
        results.append(len(names))

        # ── Summary ─────────────────────────────────────────────
        self.log.separator()
        self.log.success(
            f"Pipelining: sequential={results[0]:.4f}s, "
            f"speedup={results[1]:.1f}x, "
            f"counter (non-atomic)={results[2]}, "
            f"batch reads={results[3]} items"
        )
        return results
