"""Tests for Exercise 20: Cluster (integration — real Redis Cluster required)."""

import pytest

from redis_playground.exercises.ex20_cluster import Ex20Cluster


class TestEx20Cluster:
    @pytest.mark.integration
    def test_keyslot(self, real_redis):
        results = Ex20Cluster().execute(real_redis)
        assert "slot_user" in results

    @pytest.mark.integration
    def test_hash_tag_co_location(self, real_redis):
        results = Ex20Cluster().execute(real_redis)
        if results["slot_user"] is not None:
            assert results["same_slot"] is True

    @pytest.mark.integration
    def test_get_set(self, real_redis):
        results = Ex20Cluster().execute(real_redis)
        assert "get_result" in results
