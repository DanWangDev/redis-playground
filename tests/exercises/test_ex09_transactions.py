"""Tests for Exercise 09: Transactions."""

from redis_playground.exercises.ex09_transactions import Ex09Transactions


class TestEx09Transactions:
    def test_multi_exec_atomic(self, fake_redis):
        results = Ex09Transactions().execute(fake_redis)
        assert results["tx_result"] == [True, True, 150, 150]
        assert results["a_balance"] == "150"
        assert results["b_balance"] == "150"

    def test_discard_aborts(self, fake_redis):
        results = Ex09Transactions().execute(fake_redis)
        assert results["discarded_exists"] == 0

    def test_watch_detects_change(self, fake_redis):
        results = Ex09Transactions().execute(fake_redis)
        assert results["watch_result"] is None
        assert results["final_value"] == "999"
