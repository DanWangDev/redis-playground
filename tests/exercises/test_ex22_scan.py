"""Tests for Exercise 22: SCAN."""

from redis_playground.exercises.ex22_scan import Ex22Scan


class TestEx22Scan:
    def test_scan_finds_all_keys(self, fake_redis):
        results = Ex22Scan().execute(fake_redis)
        assert results["scan_total"] == 50
        assert results["scan_iterations"] > 1

    def test_hscan_iterates_fields(self, fake_redis):
        results = Ex22Scan().execute(fake_redis)
        assert results["hscan_total"] == 20  # 20 field names

    def test_sscan_iterates_members(self, fake_redis):
        results = Ex22Scan().execute(fake_redis)
        assert results["sscan_total"] == 15

    def test_zscan_iterates_with_scores(self, fake_redis):
        results = Ex22Scan().execute(fake_redis)
        assert results["zscan_total"] == 10  # 10 member-score tuples
