"""Tests for Exercise 01: Basic Commands."""

from redis_playground.exercises.ex01_basic_commands import Ex01BasicCommands


class TestEx01BasicCommands:
    def test_ping_returns_true(self, fake_redis):
        """PING should return True."""
        exercise = Ex01BasicCommands()
        results = exercise.execute(fake_redis)
        assert results[0] is True

    def test_set_and_get(self, fake_redis):
        """SET stores a value, GET retrieves it, GET missing key returns None."""
        exercise = Ex01BasicCommands()
        results = exercise.execute(fake_redis)
        assert results[1] == "Alice", "GET name should return 'Alice'"
        assert results[2] is None, "GET on non-existent key should return None"

    def test_exists(self, fake_redis):
        """EXISTS returns correct count for single and multiple key checks."""
        exercise = Ex01BasicCommands()
        results = exercise.execute(fake_redis)
        assert results[3] == 1, "EXISTS city should return 1"
        assert results[4] == 2, "EXISTS city language no_such_key should return 2"

    def test_expire_and_ttl(self, fake_redis):
        """EXPIRE sets TTL, TTL returns remaining seconds."""
        exercise = Ex01BasicCommands()
        results = exercise.execute(fake_redis)
        assert results[5] > 0, "TTL on expiring key should be > 0"
        assert results[6] == -1, "TTL on persistent key should be -1"

    def test_delete_key(self, fake_redis):
        """DEL removes a key, EXISTS and TTL confirm it's gone."""
        exercise = Ex01BasicCommands()
        results = exercise.execute(fake_redis)
        assert results[7] == 1, "DEL should return 1 (one key deleted)"
        assert results[8] == 0, "EXISTS after DEL should return 0"
        assert results[9] == -2, "TTL after DEL should return -2"

    def test_keys_and_type(self, fake_redis):
        """KEYS returns all keys; TYPE returns correct type."""
        exercise = Ex01BasicCommands()
        results = exercise.execute(fake_redis)
        assert results[10] > 0, "KEYS * should find at least one key"
        assert fake_redis.type("name") == "string"
        assert fake_redis.type("language") == "string"
