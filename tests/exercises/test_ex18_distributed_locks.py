"""Tests for Exercise 18: Distributed Locks."""

from redis_playground.exercises.ex18_distributed_locks import Ex18DistributedLocks


class TestEx18DistributedLocks:
    def test_acquire_lock(self, fake_redis):
        results = Ex18DistributedLocks().execute(fake_redis)
        assert results["acquired"] is True
        assert results["token"] is not None

    def test_contention_fails(self, fake_redis):
        results = Ex18DistributedLocks().execute(fake_redis)
        assert not results["second_acquired"]

    def test_safe_release(self, fake_redis):
        results = Ex18DistributedLocks().execute(fake_redis)
        assert results["wrong_release_result"] == 0
        assert results["lock_still_held"] == 1
        assert results["correct_release"] == 1
        assert results["lock_freed"] is True

    def test_fencing_token(self, fake_redis):
        results = Ex18DistributedLocks().execute(fake_redis)
        assert results["fencing_token"] == 42
