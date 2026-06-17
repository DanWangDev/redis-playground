"""Tests for Exercise 13: Bitmaps & HyperLogLog."""

from redis_playground.exercises.ex13_bitmaps_hll import Ex13BitmapsHLL


class TestEx13BitmapsHLL:
    def test_bitcount(self, fake_redis):
        results = Ex13BitmapsHLL().execute(fake_redis)
        assert results["day0_bitcount"] == 2
        assert results["day1_bitcount"] == 2

    def test_getbit(self, fake_redis):
        results = Ex13BitmapsHLL().execute(fake_redis)
        assert results["user7_both_days"] == 1

    def test_bitop_and(self, fake_redis):
        results = Ex13BitmapsHLL().execute(fake_redis)
        assert results["both_days"] == 1

    def test_pfcount(self, fake_redis):
        results = Ex13BitmapsHLL().execute(fake_redis)
        assert results["page_a"] == 3
        assert results["page_b"] == 3

    def test_pfmerge(self, fake_redis):
        results = Ex13BitmapsHLL().execute(fake_redis)
        assert results["total_unique"] == 4
