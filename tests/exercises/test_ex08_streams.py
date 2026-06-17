"""Tests for Exercise 08: Streams."""

from redis_playground.exercises.ex08_streams import Ex08Streams


class TestEx08Streams:
    def test_xadd_and_xlen(self, fake_redis):
        """XADD adds entries, XLEN returns stream length."""
        exercise = Ex08Streams()
        results = exercise.execute(fake_redis)
        assert results[2] == 2, "Stream should have 2 entries"
        assert "-" in results[0], "Entry ID should contain a timestamp"

    def test_xread_returns_entries(self, fake_redis):
        """XREAD from 0 returns all entries."""
        exercise = Ex08Streams()
        results = exercise.execute(fake_redis)
        assert results[3] == 2, "XREAD from 0 should return 2 entries"

    def test_xrange_returns_entries(self, fake_redis):
        """XRANGE returns entries in a range."""
        exercise = Ex08Streams()
        results = exercise.execute(fake_redis)
        assert results[4] == 2, "XRANGE - + should return all entries"

    def test_consumer_group(self, fake_redis):
        """XGROUP CREATE creates a consumer group."""
        exercise = Ex08Streams()
        results = exercise.execute(fake_redis)
        assert results[5] == "mygroup", "Consumer group should be created"

    def test_xreadgroup_and_xack(self, fake_redis):
        """XREADGROUP delivers messages, XACK removes them from pending."""
        exercise = Ex08Streams()
        results = exercise.execute(fake_redis)
        assert results[6] > 0, "XREADGROUP should deliver messages"
        assert results[8] == 0, "After ACK, pending count should be 0"
