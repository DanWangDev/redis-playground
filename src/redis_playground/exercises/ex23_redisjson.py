"""Exercise 23: RedisJSON — native JSON document storage (Redis Stack)."""

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner


class Ex23RedisJSON(ExerciseRunner):
    def __init__(self):
        super().__init__("23-redisjson", "RedisJSON")

    def run(self, client: redis.Redis) -> dict:
        results = {}

        self.log.section("Step 1: JSON.SET — Store a Document")
        self.log.concept("JSON.SET stores a JSON document at a key with a JSONPath.")
        self.log.concept("Requires Redis Stack — may not be available in plain Redis or older fakeredis.")
        try:
            client.execute_command(
                "JSON.SET", "user:1", "$",
                '{"name":"Alice","age":28,"plan":"pro","tags":["redis","python"]}'
            )
            self.log.command('JSON.SET user:1 $ \'{"name":"Alice","age":28,...}\'')
            self.log.success("Document stored with RedisJSON")
        except redis.exceptions.ResponseError as e:
            self.log.warn(f"JSON.SET not available: {e}")
            self.log.concept("Run with Docker `redis/redis-stack:latest` for RedisJSON support.")
            results["json_available"] = False
            self.log.separator()
            self.log.success("RedisJSON requires Redis Stack — exercise complete (conceptual)")
            return results

        results["json_available"] = True

        self.log.section("Step 2: JSON.GET — Read Paths")
        full = client.execute_command("JSON.GET", "user:1", "$")
        self.log.command("JSON.GET user:1 $")
        self.log.output(f"Full document: {full}")
        results["full"] = full

        name = client.execute_command("JSON.GET", "user:1", "$.name")
        self.log.command("JSON.GET user:1 $.name")
        self.log.output(f"Name: {name}")
        results["name"] = name

        self.log.section("Step 3: JSON.NUMINCRBY — Atomic Numeric Update")
        new_age = client.execute_command("JSON.NUMINCRBY", "user:1", "$.age", "1")
        self.log.command("JSON.NUMINCRBY user:1 $.age 1")
        self.log.output(f"Age is now: {new_age}")
        results["new_age"] = new_age

        self.log.section("Step 4: JSON.ARRAPPEND — Modify Arrays")
        arr_len = client.execute_command("JSON.ARRAPPEND", "user:1", "$.tags", '"docker"', '"lua"')
        self.log.command('JSON.ARRAPPEND user:1 $.tags "docker" "lua"')
        self.log.output(f"Array length now: {arr_len}")
        results["arr_len"] = arr_len

        tags = client.execute_command("JSON.GET", "user:1", "$.tags")
        self.log.output(f"Tags: {tags}")
        results["tags"] = tags

        self.log.section("Step 5: JSON.OBJKEYS and JSON.DEL")
        keys = client.execute_command("JSON.OBJKEYS", "user:1", "$")
        self.log.command("JSON.OBJKEYS user:1 $")
        self.log.output(f"Top-level keys: {keys}")
        results["obj_keys"] = keys

        deleted = client.execute_command("JSON.DEL", "user:1", "$.plan")
        self.log.command("JSON.DEL user:1 $.plan")
        self.log.output(f"Deleted: {deleted}")
        results["deleted"] = deleted

        self.log.separator()
        self.log.success(f"RedisJSON: name={name}, age→{new_age}, tags={arr_len}")
        return results
