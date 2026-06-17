"""Tests for Exercise 04: Lists."""

from redis_playground.exercises.ex04_lists import Ex04Lists


class TestEx04Lists:
    def test_queue_fifo(self, fake_redis):
        exercise = Ex04Lists()
        results = exercise.execute(fake_redis)
        assert results[0] == "task-1", "LPOP should return first-in element"

    def test_stack_lifo(self, fake_redis):
        exercise = Ex04Lists()
        results = exercise.execute(fake_redis)
        assert results[1] == "page-3", "LPOP should return last-pushed element"

    def test_lrange_all(self, fake_redis):
        exercise = Ex04Lists()
        results = exercise.execute(fake_redis)
        assert results[2] == 5, "Should have 5 fruits"

    def test_lrange_slicing(self, fake_redis):
        exercise = Ex04Lists()
        results = exercise.execute(fake_redis)
        assert results[3] == ["apple", "banana"]
        assert results[4] == ["date", "elderberry"]

    def test_ltrim_cap(self, fake_redis):
        exercise = Ex04Lists()
        results = exercise.execute(fake_redis)
        assert results[5] == 5, "After LTRIM 0 4, list should have 5 elements"

    def test_llen(self, fake_redis):
        exercise = Ex04Lists()
        results = exercise.execute(fake_redis)
        assert results[6] == 5, "LLEN should return 5"
