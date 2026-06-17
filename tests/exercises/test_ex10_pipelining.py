"""Tests for Exercise 10: Pipelining."""

import pytest

from redis_playground.exercises.ex10_pipelining import Ex10Pipelining


class TestEx10Pipelining:
    def test_pipeline_speedup(self, fake_redis):
        """Pipelining should be faster than sequential commands."""
        exercise = Ex10Pipelining()
        results = exercise.execute(fake_redis)
        assert results[0] > 0, "Sequential time should be positive"
        assert results[1] >= 1.0, "Pipeline should be at least as fast (speedup >= 1.0)"

    def test_pipeline_not_atomic(self, fake_redis):
        """Pipelined commands can interleave with other clients."""
        exercise = Ex10Pipelining()
        results = exercise.execute(fake_redis)
        assert results[2] == "3", (
            "Counter should be 3 (pipeline A incr + manual incr + pipeline B incr)"
        )

    def test_pipeline_batch_reads(self, fake_redis):
        """Pipeline can batch read operations efficiently."""
        exercise = Ex10Pipelining()
        results = exercise.execute(fake_redis)
        assert results[3] == 10, "Should read 10 user names via pipeline"
