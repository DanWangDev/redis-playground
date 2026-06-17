# Exercise 09: Transactions

## What You'll Learn

- Batch commands atomically with `MULTI` / `EXEC`
- Discard a transaction with `DISCARD`
- Implement optimistic locking with `WATCH` / `UNWATCH`
- Understand the limitations: no rollback on error

## Why This Matters

Redis Transactions guarantee that a batch of commands executes atomically — no other client's commands interleave. This is critical for operations like transferring money between accounts, where you must deduct from one account and credit another as a single atomic unit. The `WATCH` command enables optimistic concurrency control — checking that a key hasn't changed before executing a transaction.

## Core Concepts

### MULTI/EXEC Atomicity

```
MULTI
SET account:a 50
SET account:b 150
EXEC
```

All commands between MULTI and EXEC are queued and executed atomically as a batch. No other client can see the intermediate state.

### Optimistic Locking with WATCH

```
WATCH account:a
val = GET account:a
MULTI
SET account:a (val - 10)
EXEC
```

If `account:a` is modified by another client between `WATCH` and `EXEC`, the transaction ABORTS and `EXEC` returns `None`. The client retries the entire operation.

### Errors in Transactions

- **Syntax error before EXEC**: Redis rejects the entire transaction (EXEC returns an error).
- **Runtime error during EXEC**: Redis executes the transaction anyway, but the failing command errors. Other commands succeed. **There is no rollback.**

## What You'll Practice

1. Queue commands with MULTI and execute atomically with EXEC
2. Cancel a transaction with DISCARD
3. Watch a key with WATCH, modify it from another connection, and observe EXEC abort
4. Retry pattern: watch, get, compute, multi, exec — loop on abort

## Key Gotchas

- **No rollback**: If one command in a transaction fails, the others still execute. This is intentional for performance.
- **WATCH is connection-scoped**: WATCH is tied to the connection, not the transaction. `EXEC`, `DISCARD`, or connection close clears the watch.
- **EXEC returns None on abort**: Not an exception — `EXEC` returns `None` when a WATCHed key was modified.
- **Reads inside MULTI are deferred**: `GET` inside MULTI doesn't return the value immediately — it queues the command. The value comes back in the `EXEC` result array.
