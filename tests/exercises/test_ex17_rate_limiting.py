"""Tests for Exercise 17: Rate Limiting."""

from redis_playground.exercises.ex17_rate_limiting import Ex17RateLimiting


class TestEx17RateLimiting:
    def test_fixed_window(self, fake_redis):
        results = Ex17RateLimiting().execute(fake_redis)
        assert results["fixed_window_count"] == 1

    def test_sliding_window(self, fake_redis):
        results = Ex17RateLimiting().execute(fake_redis)
        assert results["sliding_window_count"] > 0

    def test_token_bucket(self, fake_redis):
        results = Ex17RateLimiting().execute(fake_redis)
        assert results["token_bucket_allowed"] is True
        assert results["token_bucket_remaining"] >= 0

    def test_drain_tokens(self, fake_redis):
        results = Ex17RateLimiting().execute(fake_redis)
        assert results["drain_allowed"] is True
