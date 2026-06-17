"""Tests for Exercise 03: Hashes."""

import pytest

from redis_playground.exercises.ex03_hashes import Ex03Hashes
from tests.helpers.assertions import assert_hash_field, assert_key_exists


class TestEx03Hashes:
    def test_hset_and_hlen(self, fake_redis):
        """HSET stores fields, HLEN returns field count."""
        exercise = Ex03Hashes()
        results = exercise.execute(fake_redis)
        assert results[0] == 4, "User hash should have 4 fields initially"

    def test_hget_and_hmget(self, fake_redis):
        """HGET returns single field, HMGET returns multiple."""
        exercise = Ex03Hashes()
        results = exercise.execute(fake_redis)
        assert results[1] == "Alice", "HGET name should return 'Alice'"
        assert results[2] == "Alice"
        assert results[3] == "alice@example.com"
        assert results[4] == "pro"

    def test_hincrby_atomic(self, fake_redis):
        """HINCRBY atomically increments numeric fields."""
        exercise = Ex03Hashes()
        results = exercise.execute(fake_redis)
        assert results[6] == 29, "Age should increment from 28 to 29"
        assert results[7] == 1, "New login_count should start at 1"

    def test_hexists(self, fake_redis):
        """HEXISTS returns 1 for existing field, 0 for missing."""
        exercise = Ex03Hashes()
        results = exercise.execute(fake_redis)
        assert results[8] == 1, "email field should exist"
        assert results[9] == 0, "phone field should not exist"

    def test_hkeys_hvals(self, fake_redis):
        """HKEYS and HVALS return field names and values."""
        exercise = Ex03Hashes()
        results = exercise.execute(fake_redis)
        assert results[10] > 0, "HKEYS should return field names"
        assert results[11] == results[10], "HVALS count should match HKEYS count"

    def test_hdel_removes_field(self, fake_redis):
        """HDEL removes a field, HEXISTS returns 0 after deletion."""
        exercise = Ex03Hashes()
        results = exercise.execute(fake_redis)
        assert results[12] == 1, "HDEL should delete 1 field"
        assert results[13] == 0, "HEXISTS after HDEL should return 0"
