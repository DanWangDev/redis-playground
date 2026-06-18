"""Tests for Exercise 26: FUNCTION (integration — Redis 7.0+ required)."""

import pytest

from redis_playground.exercises.ex26_function import Ex26Function


class TestEx26Function:
    @pytest.mark.integration
    def test_func_available(self, real_redis):
        results = Ex26Function().execute(real_redis)
        assert results["func_available"] is True

    @pytest.mark.integration
    def test_library_loaded(self, real_redis):
        results = Ex26Function().execute(real_redis)
        if results["func_available"]:
            assert results["lib_name"] == "mylib"

    @pytest.mark.integration
    def test_fcall_checkout(self, real_redis):
        results = Ex26Function().execute(real_redis)
        if results["func_available"]:
            assert results["after_checkout"] == 70

    @pytest.mark.integration
    def test_insufficient_rejected(self, real_redis):
        results = Ex26Function().execute(real_redis)
        if results["func_available"]:
            assert results["insufficient"] == -1
