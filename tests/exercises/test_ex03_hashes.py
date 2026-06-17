"""Tests for Exercise 03: Hashes."""

from redis_playground.exercises.ex03_hashes import Ex03Hashes


class TestEx03Hashes:
    def test_hset_and_hlen(self, fake_redis):
        exercise = Ex03Hashes()
        results = exercise.execute(fake_redis)
        assert results[0] == 4, "User should have 4 fields initially"

    def test_hget_and_hmget(self, fake_redis):
        exercise = Ex03Hashes()
        results = exercise.execute(fake_redis)
        assert results[1] == "Alice"
        assert results[2] == "Alice"
        assert results[3] == "alice@example.com"
        assert results[4] == "pro"

    def test_hincrby_atomic(self, fake_redis):
        exercise = Ex03Hashes()
        results = exercise.execute(fake_redis)
        assert results[6] == 29, "Age should increment from 28 to 29"
        assert results[7] == 1, "New login_count should start at 1"

    def test_hexists(self, fake_redis):
        exercise = Ex03Hashes()
        results = exercise.execute(fake_redis)
        assert results[8] == 1, "email field should exist"
        assert results[9] == 0, "phone field should not exist"

    def test_hkeys_hvals(self, fake_redis):
        exercise = Ex03Hashes()
        results = exercise.execute(fake_redis)
        assert results[10] > 0
        assert results[11] == results[10]

    def test_hdel_removes_field(self, fake_redis):
        exercise = Ex03Hashes()
        results = exercise.execute(fake_redis)
        assert results[12] == 1, "HDEL should delete 1 field"
        assert results[13] == 0, "HEXISTS after HDEL should return 0"
