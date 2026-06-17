"""Tests for Exercise 07: Pub/Sub."""

from redis_playground.exercises.ex07_pub_sub import Ex07PubSub


class TestEx07PubSub:
    def test_publish_without_subscriber(self, fake_redis):
        results = Ex07PubSub().execute(fake_redis)
        assert results[0] == 0

    def test_subscribe_receives_messages(self, fake_redis):
        results = Ex07PubSub().execute(fake_redis)
        assert results[1] >= 1

    def test_pattern_subscription(self, fake_redis):
        results = Ex07PubSub().execute(fake_redis)
        assert results[2] == 2
