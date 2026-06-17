"""Tests for Exercise 19: Sentinel (integration — real Redis + Sentinel required)."""

import pytest

from redis_playground.exercises.ex19_sentinel import Ex19Sentinel


class TestEx19Sentinel:
    @pytest.mark.integration
    def test_master_discovery(self, real_redis):
        results = Ex19Sentinel().execute(real_redis)
        assert "master_addr" in results

    @pytest.mark.integration
    def test_role(self, real_redis):
        results = Ex19Sentinel().execute(real_redis)
        assert results["role"] in ("master", "slave", "unknown")
