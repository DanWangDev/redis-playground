# Exercise 15: Persistence

## What You'll Learn
- Inspect persistence config with `CONFIG GET`
- Understand RDB snapshots and AOF logs
- Check persistence stats with `INFO persistence`

## Why This Matters
Redis is in-memory, but data survives restarts through RDB snapshots and AOF logs. Understanding persistence trade-offs is critical for production.

## Core Concepts
- **RDB**: Point-in-time snapshots triggered by save directives
- **AOF**: Append-only log of every write, with configurable fsync
- **Mixed mode**: RDB + AOF for fast restarts + durability

## Key Gotchas
- RDB snapshots fork — memory doubles during save.
- AOF files grow unboundedly — use BGREWRITEAOF.
- CONFIG commands require real Redis (not fakereds).
