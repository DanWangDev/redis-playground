# Exercise 16: Client-Side Caching

## What You'll Learn
- Enable server-assisted client caching with `CLIENT TRACKING ON`
- Understand RESP3 push-based invalidation
- Implement a two-tier cache pattern

## Why This Matters
Client-side caching reduces network round-trips for hot keys. Redis tracks which keys each client reads and pushes invalidation notices — no polling needed.

## Core Concepts
- **RESP3 protocol**: Required for push messages (`redis.Redis(protocol=3)`)
- **CLIENT TRACKING ON**: Enables key tracking for the connection
- **Invalidation push**: When a tracked key is modified, Redis pushes an `invalidate` message

## Key Gotchas
- Requires RESP3 protocol and real Redis (fakereds doesn't support this).
- Client must handle invalidation messages in a separate listener.
