"""Tests for Exercise 11: Lua Scripting."""

from redis_playground.exercises.ex11_lua_scripting import Ex11LuaScripting


class TestEx11LuaScripting:
    def test_eval_simple(self, fake_redis):
        results = Ex11LuaScripting().execute(fake_redis)
        assert "Hello from Lua, Redis!" in results["eval_result"]

    def test_script_load_and_exists(self, fake_redis):
        results = Ex11LuaScripting().execute(fake_redis)
        assert len(results["sha"]) == 40
        assert results["script_exists"] == [True]

    def test_atomic_inventory(self, fake_redis):
        results = Ex11LuaScripting().execute(fake_redis)
        assert results["after_deduct_30"] == 70
        assert results["insufficient"] == -1
        assert results["final_stock"] == "70"

    def test_noscript_handled(self, fake_redis):
        results = Ex11LuaScripting().execute(fake_redis)
        assert results["noscript_handled"] is True
