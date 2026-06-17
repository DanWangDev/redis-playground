# Exercise 17: Rate Limiting

## What You'll Learn
- Fixed window counter with `INCR` + `EXPIRE`
- Sliding window log with sorted sets (`ZADD` + `ZREMRANGEBYSCORE`)
- Token bucket with Lua scripting
- Compare accuracy vs memory trade-offs

## Why This Matters
Rate limiting protects APIs from abuse. Redis provides the atomic primitives needed for accurate, distributed rate limiting. Each strategy has different trade-offs: fixed window is simplest but has boundary burst issues; sliding window is most accurate; token bucket provides smooth traffic shaping.

## Core Concepts
- **Fixed window**: `INCR key` + `EXPIRE key window_seconds`. Simple but allows 2× bursts at boundaries.
- **Sliding window**: Sorted set keyed by timestamp. `ZREMRANGEBYSCORE` cleans old entries. Most accurate, more memory.
- **Token bucket**: Lua script checks bucket level, refills tokens, and allows/rejects. Smooth rate limiting.

## Key Gotchas
- Fixed window has boundary burst problem — 100 req/min can burst to 200 at minute boundary.
- Sliding window memory grows with request rate — clean up old entries.
- Token bucket needs Lua for atomicity — check-then-decrement must be atomic.
