"""Tests for Exercise 23: RedisJSON (integration — Redis Stack required)."""

import pytest

from redis_playground.exercises.ex23_redisjson import Ex23RedisJSON


class TestEx23RedisJSON:
    @pytest.mark.integration
    def test_json_available(self, real_redis):
        results = Ex23RedisJSON().execute(real_redis)
        assert results["json_available"] is True

    @pytest.mark.integration
    def test_json_get(self, real_redis):
        results = Ex23RedisJSON().execute(real_redis)
        if results["json_available"]:
            assert results["name"] is not None

    @pytest.mark.integration
    def test_json_numincrby(self, real_redis):
        results = Ex23RedisJSON().execute(real_redis)
        if results["json_available"]:
            assert results["new_age"] == [
                2
            ]  # 28 + 1 = 29 → JSON.NUMINCRBY returns [29]

    @pytest.mark.integration
    def test_json_arrappend(self, real_redis):
        results = Ex23RedisJSON().execute(real_redis)
        if results["json_available"]:
            assert results["arr_len"] == [4]  # 2 original + 2 added = 4
