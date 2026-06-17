"""Tests for Exercise 10: Pipelining."""

from redis_playground.exercises.ex10_pipelining import Ex10Pipelining


class TestEx10Pipelining:
    def test_pipeline_speedup(self, fake_redis):
        results = Ex10Pipelining().execute(fake_redis)
        assert results["seq_time"] > 0
        assert results["speedup"] > 0.5

    def test_pipeline_not_atomic(self, fake_redis):
        results = Ex10Pipelining().execute(fake_redis)
        assert results["counter"] == "3"

    def test_batch_reads(self, fake_redis):
        results = Ex10Pipelining().execute(fake_redis)
        assert results["batch_reads"] == 10
