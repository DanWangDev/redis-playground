"""Tests for Exercise 07: Pub/Sub."""

from redis_playground.exercises.ex07_pub_sub import Ex07PubSub


class TestEx07PubSub:
    def test_publish_without_subscriber_returns_zero(self, fake_redis):
        """PUBLISH returns 0 when no subscribers are listening."""
        exercise = Ex07PubSub()
        results = exercise.execute(fake_redis)
        assert results[0] == 0, "No subscribers, so PUBLISH should return 0"

    def test_subscribe_receives_messages(self, fake_redis):
        """Subscriber receives messages published after subscribing."""
        exercise = Ex07PubSub()
        results = exercise.execute(fake_redis)
        assert results[1] >= 1, "Subscriber should receive at least 1 message"

    def test_pattern_subscription(self, fake_redis):
        """Pattern subscription matches multiple channels."""
        exercise = Ex07PubSub()
        results = exercise.execute(fake_redis)
        assert results[2] == 2, (
            "PSUBSCRIBE 'notifications:*' should match both email and sms channels"
        )
