"""Exercise 11: Lua Scripting — atomic server-side scripts with EVAL/EVALSHA."""

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner


INVENTORY_CHECK_LUA = """
local key = KEYS[1]
local requested = tonumber(ARGV[1])
local current = tonumber(redis.call('GET', key) or '0')
if current >= requested then
    redis.call('DECRBY', key, requested)
    return current - requested
else
    return -1
end
"""


class Ex11LuaScripting(ExerciseRunner):
    def __init__(self):
        super().__init__("11-lua-scripting", "Lua Scripting")

    def run(self, client: redis.Redis) -> dict:
        results = {}

        self.log.section("Step 1: EVAL — Execute a Lua Script")
        self.log.concept("EVAL sends a Lua script to Redis for atomic execution.")
        simple_lua = "return 'Hello from Lua, ' .. KEYS[1] .. '!'"
        result = client.eval(simple_lua, 1, "Redis")
        self.log.command("EVAL \"return 'Hello from Lua, ' .. KEYS[1] .. '!'\" 1 Redis")
        self.log.output(f"→ {result}")
        results["eval_result"] = result

        self.log.section("Step 2: SCRIPT LOAD + EVALSHA")
        self.log.concept(
            "SCRIPT LOAD caches a script. EVALSHA executes by SHA hash (saves bandwidth)."
        )
        sha = client.script_load(INVENTORY_CHECK_LUA)
        self.log.command("SCRIPT LOAD (inventory check script)")
        self.log.output(f"SHA: {sha[:16]}...")
        results["sha"] = sha

        scripts_exist = client.script_exists(sha)
        self.log.command(f"SCRIPT EXISTS {sha[:8]}...")
        self.log.output(f"→ {scripts_exist}")
        results["script_exists"] = scripts_exist

        self.log.section("Step 3: Atomic Inventory Deduction")
        self.log.concept(
            "Lua script atomically checks inventory and deducts if sufficient."
        )
        client.set("inventory:widget", "100")
        self.log.command("SET inventory:widget 100")

        self.log.command("EVALSHA (deduct 30 from inventory:widget)")
        remaining = client.evalsha(sha, 1, "inventory:widget", "30")
        self.log.output(f"After deduct 30: {remaining}")
        results["after_deduct_30"] = remaining

        self.log.command("EVALSHA (deduct 80 — insufficient!)")
        failed = client.evalsha(sha, 1, "inventory:widget", "80")
        self.log.output(f"Deduct 80 result: {failed} (-1 = insufficient)")
        results["insufficient"] = failed

        final_stock = client.get("inventory:widget")
        self.log.output(f"Final stock: {final_stock} (should be 70)")
        results["final_stock"] = final_stock

        self.log.section("Step 4: EVALSHA Fallback Pattern")
        self.log.concept(
            "If EVALSHA fails with NOSCRIPT, fall back to EVAL and re-cache."
        )
        try:
            client.evalsha("nonexistent_sha", 0)
        except redis.exceptions.NoScriptError:
            self.log.warn("EVALSHA failed with NOSCRIPT — would fall back to EVAL")
            results["noscript_handled"] = True
        else:
            results["noscript_handled"] = False

        self.log.separator()
        self.log.success(
            f"Lua: EVAL={result!r}, inventory: 100→{final_stock}, SHA cached"
        )
        return results
