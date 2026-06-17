"""Tests for Exercise 15: Persistence (integration — real Redis required)."""

import pytest

from redis_playground.exercises.ex15_persistence import Ex15Persistence


class TestEx15Persistence:
    @pytest.mark.integration
    def test_config_get_save(self, real_redis):
        results = Ex15Persistence().execute(real_redis)
        assert "has_save_config" in results

    @pytest.mark.integration
    def test_aof_config(self, real_redis):
        results = Ex15Persistence().execute(real_redis)
        assert "fsync_mode" in results

    @pytest.mark.integration
    def test_info_persistence(self, real_redis):
        results = Ex15Persistence().execute(real_redis)
        assert results["rdb_changes"] >= 0

    @pytest.mark.integration
    def test_maxmemory_policy(self, real_redis):
        results = Ex15Persistence().execute(real_redis)
        assert results["policy"] is not None
