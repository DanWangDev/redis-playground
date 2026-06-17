# Exercise 09: Transactions

## What You'll Learn
- Queue commands atomically with `MULTI` / `EXEC`
- Cancel a transaction with `DISCARD`
- Implement optimistic locking with `WATCH`
- Understand the no-rollback limitation

## Why This Matters
Redis Transactions guarantee atomic command batches — no other client interleaves. Critical for operations like money transfers. `WATCH` enables optimistic concurrency control: if a watched key changes, the transaction aborts and you retry.

## Core Concepts
- **MULTI/EXEC**: Commands between them are queued, then executed atomically
- **DISCARD**: Aborts the transaction — queued commands are never executed
- **WATCH**: Monitors keys; if any change before EXEC, transaction aborts
- **No rollback**: If one command fails, others still execute

## Key Gotchas
- No rollback: a runtime error inside MULTI doesn't undo earlier commands.
- WATCH is connection-scoped, cleared by EXEC/DISCARD/disconnect.
- EXEC returns None (or raises WatchError in redis-py) when aborted.
- Reads inside MULTI are deferred — values come back in the EXEC result array.
