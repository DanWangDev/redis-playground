"""Exercise 17: Rate Limiting — fixed window, sliding window, token bucket."""

import time
import redis

from redis_playground.shared.exercise_runner import ExerciseRunner

TOKEN_BUCKET_LUA = """
local key = KEYS[1]
local capacity = tonumber(ARGV[1])
local rate = tonumber(ARGV[2])
local now = tonumber(ARGV[3])
local requested = tonumber(ARGV[4])

local bucket = redis.call('HMGET', key, 'tokens', 'last_refill')
local tokens = tonumber(bucket[1]) or capacity
local last_refill = tonumber(bucket[2]) or now

local elapsed = now - last_refill
local refill = math.floor(elapsed * rate)
tokens = math.min(capacity, tokens + refill)

local allowed = 0
if tokens >= requested then
    tokens = tokens - requested
    allowed = 1
end

redis.call('HMSET', key, 'tokens', tokens, 'last_refill', now)
redis.call('EXPIRE', key, 60)
return {allowed, tokens}
"""


class Ex17RateLimiting(ExerciseRunner):
    def __init__(self):
        super().__init__("17-rate-limiting", "Rate Limiting")

    def run(self, client: redis.Redis) -> dict:
        results = {}

        self.log.section("Step 1: Fixed Window Counter")
        self.log.concept(
            "Simplest rate limiter: INCR counter, EXPIRE to reset after window."
        )
        key = "ratelimit:fixed:user:1"
        client.delete(key)
        count = client.incr(key)
        client.expire(key, 60)
        self.log.command("INCR ratelimit:fixed:user:1 → EXPIRE 60")
        self.log.output(f"Request count: {count}/100 allowed in this window")
        results["fixed_window_count"] = count

        self.log.section("Step 2: Sliding Window with Sorted Sets")
        self.log.concept(
            "Store each request timestamp as a sorted set member. Clean old entries."
        )
        now_ms = int(time.time() * 1000)
        window_ms = 60000  # 1 minute window
        zkey = "ratelimit:sliding:user:1"
        client.delete(zkey)
        # Simulate requests at different times
        for i in range(5):
            client.zadd(
                zkey, {f"req:{now_ms - 50000 + i * 1000}": now_ms - 50000 + i * 1000}
            )
        cutoff = now_ms - window_ms
        client.zremrangebyscore(zkey, 0, cutoff)
        count = client.zcard(zkey)
        self.log.command("ZADD (5 timestamps) → ZREMRANGEBYSCORE → ZCARD")
        self.log.output(f"Requests in last {window_ms}ms: {count}")
        results["sliding_window_count"] = count

        self.log.section("Step 3: Token Bucket with Lua")
        self.log.concept(
            "Token bucket provides smooth rate limiting. Lua script makes it atomic."
        )
        tkey = "ratelimit:bucket:user:1"
        client.delete(tkey)
        sha = client.script_load(TOKEN_BUCKET_LUA)
        # 10 tokens capacity, 1 token/sec refill, request 1 token
        result = client.evalsha(sha, 1, tkey, "10", "1", str(now_ms // 1000), "1")
        self.log.command("EVALSHA token_bucket (capacity=10, rate=1/s, request=1)")
        self.log.output(f"Allowed={result[0]}, Tokens left={result[1]}")
        results["token_bucket_allowed"] = result[0] == 1
        results["token_bucket_remaining"] = result[1]

        # Drain remaining tokens
        result2 = client.evalsha(sha, 1, tkey, "10", "1", str(now_ms // 1000 + 1), "9")
        self.log.command("Request 9 more tokens")
        self.log.output(f"Allowed={result2[0]}, Tokens left={result2[1]}")
        results["drain_allowed"] = result2[0] == 1

        self.log.separator()
        self.log.success(
            f"Rate limiting: fixed={count}, sliding={results['sliding_window_count']}, token_bucket OK"
        )
        return results
