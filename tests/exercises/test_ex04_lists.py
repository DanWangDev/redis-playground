"""Tests for Exercise 04: Lists."""

from redis_playground.exercises.ex04_lists import Ex04Lists


class TestEx04Lists:
    def test_queue_fifo(self, fake_redis):
        """LPOP after RPUSH returns first-in element."""
        exercise = Ex04Lists()
        results = exercise.execute(fake_redis)
        assert results[0] == "task-1", "First LPOP should return 'task-1' (FIFO)"

    def test_stack_lifo(self, fake_redis):
        """LPOP after LPUSH returns last-pushed element."""
        exercise = Ex04Lists()
        results = exercise.execute(fake_redis)
        assert results[1] == "page-3", "LPOP should return 'page-3' (LIFO)"

    def test_lrange_all(self, fake_redis):
        """LRANGE 0 -1 returns all elements."""
        exercise = Ex04Lists()
        results = exercise.execute(fake_redis)
        assert results[2] == 5, "Should have 5 fruits"

    def test_lrange_slicing(self, fake_redis):
        """LRANGE with indices slices the list."""
        exercise = Ex04Lists()
        results = exercise.execute(fake_redis)
        assert results[3] == ["apple", "banana"], "LRANGE 0 1 should return first two"
        assert results[4] == ["date", "elderberry"], (
            "LRANGE -2 -1 should return last two"
        )

    def test_ltrim_cap(self, fake_redis):
        """LTRIM caps list to specified range."""
        exercise = Ex04Lists()
        results = exercise.execute(fake_redis)
        assert results[5] == 5, "After LTRIM 0 4, list should have 5 elements"

    def test_llen(self, fake_redis):
        """LLEN returns the correct element count."""
        exercise = Ex04Lists()
        results = exercise.execute(fake_redis)
        assert results[6] == 5, "LLEN should return 5"
