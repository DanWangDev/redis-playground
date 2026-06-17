"""Tests for Exercise 14: Keyspace Notifications."""

from redis_playground.exercises.ex14_keyspace_notifications import (
    Ex14KeyspaceNotifications,
)


class TestEx14KeyspaceNotifications:
    def test_config_set(self, fake_redis):
        results = Ex14KeyspaceNotifications().execute(fake_redis)
        assert results["config_set"] is True

    def test_events_captured(self, fake_redis):
        results = Ex14KeyspaceNotifications().execute(fake_redis)
        assert results["event_count"] >= 2
