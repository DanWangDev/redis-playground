"""Tests for Exercise 08: Streams."""

from redis_playground.exercises.ex08_streams import Ex08Streams


class TestEx08Streams:
    def test_xadd_and_xlen(self, fake_redis):
        results = Ex08Streams().execute(fake_redis)
        assert results[2] == 2

    def test_xread_returns_entries(self, fake_redis):
        results = Ex08Streams().execute(fake_redis)
        assert results[3] == 2

    def test_xrange_returns_entries(self, fake_redis):
        results = Ex08Streams().execute(fake_redis)
        assert results[4] == 2

    def test_consumer_group(self, fake_redis):
        results = Ex08Streams().execute(fake_redis)
        assert results[5] == "mygroup"

    def test_xreadgroup_and_xack(self, fake_redis):
        results = Ex08Streams().execute(fake_redis)
        assert results[6] > 0
        assert results[8] == 0
