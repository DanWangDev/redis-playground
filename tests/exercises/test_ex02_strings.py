"""Tests for Exercise 02: Strings."""

from redis_playground.exercises.ex02_strings import Ex02Strings


class TestEx02Strings:
    def test_incr_atomic_counter(self, fake_redis):
        exercise = Ex02Strings()
        results = exercise.execute(fake_redis)
        assert results[0] == 1, "First INCR should return 1"
        assert results[1] == 2, "Second INCR should return 2"

    def test_incrby_and_decr(self, fake_redis):
        exercise = Ex02Strings()
        results = exercise.execute(fake_redis)
        assert results[2] == 100, "INCRBY 100 should return 100"
        assert results[3] == 49, "DECR from 50 should return 49"

    def test_mset_and_mget(self, fake_redis):
        exercise = Ex02Strings()
        results = exercise.execute(fake_redis)
        assert results[4] == "Alice"
        assert results[5] == "alice@example.com"
        assert results[6] == "pro"
        assert results[7] is None, "Missing key should return None"

    def test_getrange_and_strlen(self, fake_redis):
        exercise = Ex02Strings()
        results = exercise.execute(fake_redis)
        assert results[8] == "Hello", "GETRANGE 0 4 should return 'Hello'"
        assert results[9] == 13, "STRLEN of 'Hello, World!' should be 13"

    def test_setrange_overwrites(self, fake_redis):
        exercise = Ex02Strings()
        results = exercise.execute(fake_redis)
        assert results[10] == "Hello, Redis!"

    def test_setnx_atomic(self, fake_redis):
        exercise = Ex02Strings()
        results = exercise.execute(fake_redis)
        assert results[11] == 1, "First SETNX should succeed"
        assert results[12] == 0, "Second SETNX on same key should fail"

    def test_append(self, fake_redis):
        exercise = Ex02Strings()
        results = exercise.execute(fake_redis)
        assert results[13] > 0, "APPEND should return new length"
        assert "retry failed" in results[14], "Appended text should be in the value"
