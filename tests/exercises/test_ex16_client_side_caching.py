"""Tests for Exercise 16: Client-Side Caching (integration — real Redis + RESP3 required)."""

import pytest

from redis_playground.exercises.ex16_client_side_caching import Ex16ClientSideCaching


class TestEx16ClientSideCaching:
    @pytest.mark.integration
    def test_tracking_enabled(self, real_redis):
        results = Ex16ClientSideCaching().execute(real_redis)
        assert results["tracking_enabled"] is True

    @pytest.mark.integration
    def test_cache_read(self, real_redis):
        results = Ex16ClientSideCaching().execute(real_redis)
        if results["tracking_enabled"]:
            assert results["cache_hit_value"] is not None
