"""Tests for Exercise 02: Strings."""

import pytest

from redis_playground.exercises.ex02_strings import Ex02Strings
from tests.helpers.assertions import assert_value_equal


class TestEx02Strings:
    def test_incr_atomic_counter(self, fake_redis):
        """INCR creates key at 0 then increments to 1."""
        exercise = Ex02Strings()
        results = exercise.execute(fake_redis)
        assert results[0] == 1, "First INCR should return 1"
        assert results[1] == 2, "Second INCR should return 2"

    def test_incrby_and_decr(self, fake_redis):
        """INCRBY increments by custom amount, DECR subtracts 1."""
        exercise = Ex02Strings()
        results = exercise.execute(fake_redis)
        assert results[2] == 100, "INCRBY 100 should return 100"
        assert results[3] == 49, "DECR from 50 should return 49"

    def test_mset_and_mget(self, fake_redis):
        """MGET returns values in order, None for missing keys."""
        exercise = Ex02Strings()
        results = exercise.execute(fake_redis)
        assert results[4] == "Alice"
        assert results[5] == "alice@example.com"
        assert results[6] == "pro"
        assert results[7] is None, "Missing key should return None"

    def test_getrange_and_strlen(self, fake_redis):
        """GETRANGE extracts substring, STRLEN returns character count."""
        exercise = Ex02Strings()
        results = exercise.execute(fake_redis)
        assert results[8] == "Hello", "GETRANGE 0 4 should return 'Hello'"
        assert results[9] == 13, "STRLEN of 'Hello, World!' should be 13"

    def test_setrange_overwrites(self, fake_redis):
        """SETRANGE overwrites characters at an offset."""
        exercise = Ex02Strings()
        results = exercise.execute(fake_redis)
        assert results[10] == "Hello, Redis!", "SETRANGE should overwrite 'World' with 'Redis'"

    def test_setnx_atomic(self, fake_redis):
        """SETNX returns 1 on first call, 0 if key already exists."""
        exercise = Ex02Strings()
        results = exercise.execute(fake_redis)
        assert results[11] == 1, "First SETNX should succeed (return 1)"
        assert results[12] == 0, "Second SETNX on same key should fail (return 0)"

    def test_append(self, fake_redis):
        """APPEND adds to end of string, returns new length."""
        exercise = Ex02Strings()
        results = exercise.execute(fake_redis)
        assert results[13] > 0, "APPEND should return new length"
        assert "retry failed" in results[14], "Appended text should be in the value"
