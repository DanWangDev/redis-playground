"""Tests for Exercise 25: RedisTimeSeries (integration — Redis Stack required)."""

import pytest

from redis_playground.exercises.ex25_redistimeseries import Ex25RedisTimeSeries


class TestEx25RedisTimeSeries:
    @pytest.mark.integration
    def test_ts_available(self, real_redis):
        results = Ex25RedisTimeSeries().execute(real_redis)
        assert results["ts_available"] is True

    @pytest.mark.integration
    def test_points_added(self, real_redis):
        results = Ex25RedisTimeSeries().execute(real_redis)
        if results["ts_available"]:
            assert results["points_added"] == 4

    @pytest.mark.integration
    def test_range_query(self, real_redis):
        results = Ex25RedisTimeSeries().execute(real_redis)
        if results["ts_available"]:
            assert results["range_count"] == 4

    @pytest.mark.integration
    def test_aggregation(self, real_redis):
        results = Ex25RedisTimeSeries().execute(real_redis)
        if results["ts_available"]:
            assert results["agg_buckets"] >= 1
