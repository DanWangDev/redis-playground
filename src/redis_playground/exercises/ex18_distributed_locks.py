"""Exercise 18: Distributed Locks — SET NX PX, safe release, fencing tokens."""

import uuid
import redis

from redis_playground.shared.exercise_runner import ExerciseRunner

SAFE_RELEASE_LUA = """
if redis.call('GET', KEYS[1]) == ARGV[1] then
    return redis.call('DEL', KEYS[1])
else
    return 0
end
"""


class Ex18DistributedLocks(ExerciseRunner):
    def __init__(self):
        super().__init__("18-distributed-locks", "Distributed Locks")

    def run(self, client: redis.Redis) -> dict:
        results = {}

        self.log.section("Step 1: Acquire Lock with SET NX PX")
        self.log.concept("SET key value NX PX 30000: set only if Not eXists, with 30s eXpiration.")
        token = str(uuid.uuid4())[:8]
        acquired = client.set("lock:resource", token, nx=True, px=30000)
        self.log.command(f'SET lock:resource "{token}" NX PX 30000')
        self.log.output(f"Lock acquired: {acquired} (token={token})")
        results["acquired"] = acquired
        results["token"] = token

        self.log.section("Step 2: Contention — Second Lock Attempt Fails")
        self.log.concept("A second client tries to acquire the same lock — NX prevents it.")
        other_token = "other-" + str(uuid.uuid4())[:4]
        second_acquired = client.set("lock:resource", other_token, nx=True, px=30000)
        self.log.command(f'SET lock:resource "{other_token}" NX PX 30000')
        self.log.output(f"Second attempt: {second_acquired} (0 = lock held by another)")
        results["second_acquired"] = second_acquired

        self.log.section("Step 3: Safe Release with Lua")
        self.log.concept("A Lua script checks the token before deleting — prevents releasing others' locks.")
        sha = client.script_load(SAFE_RELEASE_LUA)
        # Wrong token attempt
        wrong_release = client.evalsha(sha, 1, "lock:resource", "wrong-token")
        self.log.command('EVALSHA safe_release (wrong token)')
        self.log.output(f"Wrong token release: {wrong_release} (0 = not released)")

        # Correct token release
        lock_still_held = client.exists("lock:resource")
        self.log.output(f"Lock still held: {lock_still_held}")
        results["wrong_release_result"] = wrong_release
        results["lock_still_held"] = lock_still_held

        correct_release = client.evalsha(sha, 1, "lock:resource", token)
        self.log.command(f'EVALSHA safe_release (correct token "{token}")')
        self.log.output(f"Correct token release: {correct_release} (1 = released)")
        results["correct_release"] = correct_release

        lock_exists = client.exists("lock:resource")
        self.log.output(f"Lock exists now: {lock_exists} (0 = free)")
        results["lock_freed"] = lock_exists == 0

        self.log.section("Step 4: Fencing Token Pattern")
        self.log.concept("Fencing tokens (monotonic IDs) prevent lock-starvation from paused processes.")
        fence_token = 42
        client.set("lock:resource", str(fence_token), nx=True, px=30000)
        current_fence = int(client.get("lock:resource") or 0)
        self.log.command(f"Lock acquired with fencing token: {fence_token}")
        self.log.output(f"Current fence: {current_fence} — storage checks {fence_token} >= {current_fence}")
        results["fencing_token"] = fence_token

        client.delete("lock:resource")

        self.log.separator()
        self.log.success(f"Distributed locks: SET NX PX OK, safe release OK, fencing token={fence_token}")
        return results
