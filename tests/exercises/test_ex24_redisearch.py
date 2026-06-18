"""Tests for Exercise 24: RediSearch (integration — Redis Stack required)."""

import pytest

from redis_playground.exercises.ex24_redisearch import Ex24RediSearch


class TestEx24RediSearch:
    @pytest.mark.integration
    def test_search_available(self, real_redis):
        results = Ex24RediSearch().execute(real_redis)
        assert results["search_available"] is True

    @pytest.mark.integration
    def test_text_search(self, real_redis):
        results = Ex24RediSearch().execute(real_redis)
        if results["search_available"]:
            assert results["text_search"] >= 2

    @pytest.mark.integration
    def test_price_filter(self, real_redis):
        results = Ex24RediSearch().execute(real_redis)
        if results["search_available"]:
            assert results["price_filter"] >= 1

    @pytest.mark.integration
    def test_tag_filter(self, real_redis):
        results = Ex24RediSearch().execute(real_redis)
        if results["search_available"]:
            assert results["tag_filter"] >= 1
