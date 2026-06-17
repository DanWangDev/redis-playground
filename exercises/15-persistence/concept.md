# Exercise 15: Persistence

## What You'll Learn
- Inspect persistence config with `CONFIG GET`
- Understand RDB snapshots: `save` trigger, `BGSAVE`
- Understand AOF: `appendonly`, `appendfsync` modes
- Check persistence stats with `INFO persistence`

## Why This Matters
Redis is an in-memory database, but data can survive restarts through RDB snapshots and AOF logs. Understanding persistence trade-offs is critical for production: RDB is compact but may lose recent data; AOF is durable but larger and slower to restart.

## Core Concepts
- **RDB**: Point-in-time snapshots. `save 900 1` means "save if 1 key changed in 900s". `BGSAVE` triggers manual snapshot.
- **AOF**: Append-only log of every write command. `appendfsync` modes: `always` (safest), `everysec` (default), `no`.
- **Mixed mode**: RDB + AOF together gives fast restarts + durability.

## Key Gotchas
- RDB snapshots are forked — child process writes, parent continues serving. Memory doubles during save.
- AOF files grow unboundedly — use `BGREWRITEAOF` to compact.
- `appendfsync always` is safest but slowest — every write waits for disk flush.
