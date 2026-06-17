# Exercise 16: Client-Side Caching

## What You'll Learn
- Enable server-assisted client caching with `CLIENT TRACKING ON`
- Understand RESP3 push-based invalidation
- Implement a two-tier cache pattern (local + Redis)

## Why This Matters
Client-side caching reduces network round-trips for hot keys. Redis tracks which keys each client reads and pushes invalidation notices when those keys change — the client can then invalidate its local cache without polling. This is a "server-assisted" pattern, unique to Redis RESP3.

## Core Concepts
- **RESP3 protocol**: Required for push messages. `redis.Redis(protocol=3)`
- **CLIENT TRACKING ON**: Enables key tracking for the connection
- **Invalidation push**: When a tracked key is modified, Redis pushes an `invalidate` message
- **Two-tier cache**: Local in-memory cache (fast) + Redis (shared, consistent)

## Key Gotchas
- Requires RESP3 protocol (redis-py: `protocol=3`)
- Client must handle invalidation messages in a separate listener
- Only works with real Redis — fakeredis doesn't support this
- Broadcasting mode (`BCAST`) invalidates keys for ALL tracking clients
