"""Tests for Exercise 06: Sorted Sets."""

from redis_playground.exercises.ex06_sorted_sets import Ex06SortedSets


class TestEx06SortedSets:
    def test_zadd_and_zcard(self, fake_redis):
        results = Ex06SortedSets().execute(fake_redis)
        assert results[0] == 10

    def test_zrevrange_top_players(self, fake_redis):
        results = Ex06SortedSets().execute(fake_redis)
        assert results[1][0][0] == "player:dave"
        assert results[1][0][1] == 10100.0

    def test_zrank_and_zscore(self, fake_redis):
        results = Ex06SortedSets().execute(fake_redis)
        assert results[2] >= 0
        assert results[4] == 6700.0

    def test_zincrby_updates_score(self, fake_redis):
        results = Ex06SortedSets().execute(fake_redis)
        assert results[5] == 7200.0

    def test_zcount_range(self, fake_redis):
        results = Ex06SortedSets().execute(fake_redis)
        assert results[6] >= 0
        assert results[7] >= 0

    def test_zrem_removes_member(self, fake_redis):
        results = Ex06SortedSets().execute(fake_redis)
        assert results[9] == 1
        assert results[10] is None
