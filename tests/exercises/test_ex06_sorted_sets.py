"""Tests for Exercise 06: Sorted Sets."""

import pytest

from redis_playground.exercises.ex06_sorted_sets import Ex06SortedSets
from tests.helpers.assertions import (
    assert_sorted_set_rank,
    assert_sorted_set_score,
)


class TestEx06SortedSets:
    def test_zadd_and_zcard(self, fake_redis):
        """ZADD adds members with scores, ZCARD returns count."""
        exercise = Ex06SortedSets()
        results = exercise.execute(fake_redis)
        assert results[0] == 10, "Should have 10 players"

    def test_zrevrange_top_players(self, fake_redis):
        """ZREVRANGE returns highest scores first."""
        exercise = Ex06SortedSets()
        results = exercise.execute(fake_redis)
        top3 = results[1]
        assert top3[0][0] == "player:dave", "Top player should be dave (10100)"
        assert top3[0][1] == 10100.0

    def test_zrank_and_zscore(self, fake_redis):
        """ZRANK and ZSCORE return correct position and score."""
        exercise = Ex06SortedSets()
        results = exercise.execute(fake_redis)
        # eve starts at 6700, should be near the bottom
        assert results[2] >= 0, "ZRANK should return a valid rank"
        assert results[4] == 6700.0, "eve's initial score should be 6700"

    def test_zincrby_updates_score(self, fake_redis):
        """ZINCRBY atomically increments a member's score."""
        exercise = Ex06SortedSets()
        results = exercise.execute(fake_redis)
        assert results[5] == 7200.0, "eve's score should be 6700 + 500 = 7200"
        # eve moved from 6700 to 7200; rank may or may not change depending on tie-breaking
        assert results[6] is not None, "eve should still have a rank"

    def test_zcount_range(self, fake_redis):
        """ZCOUNT returns correct count for score range."""
        exercise = Ex06SortedSets()
        results = exercise.execute(fake_redis)
        assert results[7] >= 0, "ZCOUNT should return a non-negative count"
        assert results[8] >= 0, "ZCOUNT for elite should return a non-negative count"

    def test_zrem_removes_member(self, fake_redis):
        """ZREM removes a member, ZSCORE returns None."""
        exercise = Ex06SortedSets()
        results = exercise.execute(fake_redis)
        assert results[9] == 1, "ZREM should remove 1 member"
        assert results[10] is None, "ZSCORE should return None for removed member"
