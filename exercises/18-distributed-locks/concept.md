# Exercise 18: Distributed Locks

## What You'll Learn
- Acquire a lock with `SET NX PX` (atomic set-if-not-exists with TTL)
- Release safely with a Lua script (verify token before delete)
- Understand the Redlock algorithm for multi-node Redis
- Use fencing tokens to prevent lock-starvation issues

## Why This Matters
Distributed locks coordinate access to shared resources across multiple processes/servers. Redis provides simple but powerful lock primitives. However, distributed locking is surprisingly subtle — clock skew, process pauses, and network partitions can all break naive lock implementations.

## Core Concepts
- **SET NX PX**: Atomic "set if not exists with expiry" — the foundation of Redis locks
- **Lock token**: A random UUID identifies the lock owner; prevents accidentally releasing someone else's lock
- **Safe release**: Lua script checks token before deleting
- **Redlock**: Acquire lock on N independent Redis nodes (N/2+1 required) for fault tolerance

## Key Gotchas
- Never release a lock without verifying the token — use a Lua script.
- Always set a TTL — prevent deadlocks if the lock holder crashes.
- Redlock is controversial (Martin Kleppmann's critique) — understand the limitations.
- Clock skew between nodes can cause Redlock to grant locks to two holders.
