"""Tests for Exercise 21: Sharded Pub/Sub (integration — Redis 7.0+ required)."""

import pytest

from redis_playground.exercises.ex21_sharded_pub_sub import Ex21ShardedPubSub


class TestEx21ShardedPubSub:
    @pytest.mark.integration
    def test_spublish_without_subscribers(self, real_redis):
        results = Ex21ShardedPubSub().execute(real_redis)
        assert "spublish_no_sub" in results

    @pytest.mark.integration
    def test_sharded_available(self, real_redis):
        results = Ex21ShardedPubSub().execute(real_redis)
        assert results["sharded_available"] is True

    @pytest.mark.integration
    def test_message_delivery_ran(self, real_redis):
        results = Ex21ShardedPubSub().execute(real_redis)
        if results["sharded_available"]:
            assert "message_count" in results

    @pytest.mark.integration
    def test_classic_vs_sharded_ran(self, real_redis):
        results = Ex21ShardedPubSub().execute(real_redis)
        if results["sharded_available"]:
            assert "classic_received" in results
            assert "sharded_received" in results
