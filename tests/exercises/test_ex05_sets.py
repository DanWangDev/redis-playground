"""Tests for Exercise 05: Sets."""

import pytest

from redis_playground.exercises.ex05_sets import Ex05Sets
from tests.helpers.assertions import assert_set_member, assert_set_size


class TestEx05Sets:
    def test_sadd_adds_members(self, fake_redis):
        """SADD adds unique members, duplicates are ignored."""
        exercise = Ex05Sets()
        results = exercise.execute(fake_redis)
        assert results[0] == 4, "First SADD should add 4 members"
        assert results[1] == 0, "Duplicate SADD should add 0 members"

    def test_sismember(self, fake_redis):
        """SISMEMBER correctly identifies membership."""
        exercise = Ex05Sets()
        results = exercise.execute(fake_redis)
        assert results[2] == 1, "cache should be a member"
        assert results[3] == 0, "sql should not be a member"

    def test_sinter_common_tags(self, fake_redis):
        """SINTER returns common elements (redis is the only shared tag between article:1 and article:2)."""
        exercise = Ex05Sets()
        results = exercise.execute(fake_redis)
        assert "redis" in results[4], "redis should be in intersection"
        assert len(results[4]) == 1, "Only 'redis' is shared between article:1 and article:2"

    def test_sunion_all_tags(self, fake_redis):
        """SUNION returns all distinct elements."""
        exercise = Ex05Sets()
        results = exercise.execute(fake_redis)
        assert len(results[5]) > 0, "SUNION should return tags"

    def test_sdiff_exclusive_tags(self, fake_redis):
        """SDIFF returns elements only in first set."""
        exercise = Ex05Sets()
        results = exercise.execute(fake_redis)
        assert "performance" in results[6], "SDIFF should find performance tag"

    def test_scard_and_srandmember(self, fake_redis):
        """SCARD returns size, SRANDMEMBER returns random elements."""
        exercise = Ex05Sets()
        results = exercise.execute(fake_redis)
        assert results[7] == 4, "article:1 should have 4 tags"
        assert len(results[8]) == 2, "SRANDMEMBER with count 2 should return 2 elements"

    def test_srem(self, fake_redis):
        """SREM removes members and returns count."""
        exercise = Ex05Sets()
        results = exercise.execute(fake_redis)
        assert results[9] == 1, "SREM should remove 1 member"
        assert results[10] == 0, "Removed member should not exist"
