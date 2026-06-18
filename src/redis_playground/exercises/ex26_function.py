"""Exercise 26: FUNCTION — Redis 7 durable server-side functions."""

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner

INVENTORY_LIB = """
#!lua name=mylib
redis.register_function('checkout', function(keys, args)
    local key = keys[1]
    local requested = tonumber(args[1])
    local current = tonumber(redis.call('GET', key) or '0')
    if current >= requested then
        redis.call('DECRBY', key, requested)
        return current - requested
    else
        return -1
    end
end)
"""


class Ex26Function(ExerciseRunner):
    def __init__(self):
        super().__init__("26-function", "FUNCTION")

    def run(self, client: redis.Redis) -> dict:
        results = {}

        self.log.section("Step 1: FUNCTION LOAD — Load a Library")
        self.log.concept(
            "Functions are durable — they survive restarts, unlike EVAL scripts."
        )
        self.log.concept(
            "Requires Redis 7.0+ — may not be available in older versions."
        )
        try:
            client.execute_command("FUNCTION", "LOAD", "REPLACE", INVENTORY_LIB)
            self.log.command("FUNCTION LOAD REPLACE (inventory library)")
            self.log.success("Library loaded: mylib")
        except redis.exceptions.ResponseError as e:
            self.log.warn(f"FUNCTION LOAD not available: {e}")
            self.log.concept(
                "Run with Redis 7.0+ to try durable server-side functions."
            )
            results["func_available"] = False
            self.log.separator()
            self.log.success("FUNCTION requires Redis 7.0+")
            return results

        results["func_available"] = True

        self.log.section("Step 2: FUNCTION LIST — List Libraries")
        func_list = client.execute_command("FUNCTION", "LIST")
        self.log.command("FUNCTION LIST")
        lib_name = func_list[0][1] if func_list else "unknown"
        self.log.output(f"Loaded library: {lib_name}")
        results["lib_name"] = lib_name

        self.log.section("Step 3: FCALL — Call a Function")
        self.log.concept(
            "FCALL calls a registered function by name — no SHA hash needed."
        )
        client.set("inventory:widget", "100")
        self.log.command("SET inventory:widget 100")

        remaining = client.execute_command(
            "FCALL", "checkout", "1", "inventory:widget", "30"
        )
        self.log.command("FCALL checkout 1 inventory:widget 30")
        self.log.output(f"Remaining after checkout: {remaining}")
        results["after_checkout"] = remaining

        failed = client.execute_command(
            "FCALL", "checkout", "1", "inventory:widget", "80"
        )
        self.log.command("FCALL checkout 1 inventory:widget 80")
        self.log.output(f"Insufficient stock: {failed} (-1 = rejected)")
        results["insufficient"] = failed

        self.log.section("Step 4: FUNCTION DELETE")
        client.execute_command("FUNCTION", "DELETE", "mylib")
        self.log.command("FUNCTION DELETE mylib")
        self.log.success("Library deleted")
        results["deleted"] = True

        self.log.separator()
        self.log.success(f"FUNCTION: {lib_name} loaded, checkout OK, deleted")
        return results
