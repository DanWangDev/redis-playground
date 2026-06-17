"""Tests for Exercise 09: Transactions."""

import pytest

from redis_playground.exercises.ex09_transactions import Ex09Transactions


class TestEx09Transactions:
    def test_multi_exec_atomic_transfer(self, fake_redis):
        """MULTI/EXEC executes commands atomically."""
        exercise = Ex09Transactions()
        results = exercise.execute(fake_redis)
        assert results[0] == [True, True, 150, 150], "Transaction should execute all commands"
        assert results[1] == "150", "account:a should be 150"
        assert results[2] == "150", "account:b should be 150"

    def test_discard_aborts_transaction(self, fake_redis):
        """DISCARD prevents queued commands from executing."""
        exercise = Ex09Transactions()
        results = exercise.execute(fake_redis)
        assert results[3] == 0, "Discarded key should not exist"

    def test_watch_detects_modification(self, fake_redis):
        """WATCH detects when another client modifies the key."""
        exercise = Ex09Transactions()
        results = exercise.execute(fake_redis)
        assert results[4] is None, "EXEC should return None when WATCHed key changed"
        assert results[5] == "999", "Final value should be the other client's value (999)"
