# Exercise 02: Strings

## What You'll Learn

- Atomic counter operations with `INCR`, `DECR`, `INCRBY`
- Bulk operations with `MSET` and `MGET`
- String slicing with `GETRANGE` and `SETRANGE`
- Atomic set-if-not-exists with `SETNX`
- String metadata: `STRLEN`, `APPEND`

## Why This Matters

Redis strings are not just for text — they handle counters, cache values, serialized JSON, and binary data. The atomic increment operations (`INCR`/`DECR`) are the foundation for rate limiters, view counters, and inventory systems. `MSET`/`MGET` batch multiple operations into a single round-trip, critical for performance.

## Core Concepts

### Counters Are Atomic

Unlike `GET` → increment → `SET` in application code, `INCR` is a single atomic operation. If two clients call `INCR views` simultaneously, Redis guarantees the counter increments by 2 — no lost updates.

### Bulk Operations Reduce RTT

```
# Without batching: 3 round-trips
SET user:1:name "Alice"
SET user:1:email "alice@example.com"
SET user:1:plan "pro"

# With MSET: 1 round-trip
MSET user:1:name "Alice" user:1:email "alice@example.com" user:1:plan "pro"
```

Each round-trip adds ~0.5-2ms of network latency. `MSET`/`MGET` eliminate this overhead.

### SETNX for Distributed Locks (Preview)

`SETNX key value` sets the key only if it doesn't exist. This is the primitive behind distributed locks (covered in detail in Exercise 18).

### String as Binary Blob

Redis strings are binary-safe — up to 512 MB. You can store JSON, MessagePack, or serialized protobuf. `GETRANGE` and `SETRANGE` allow random access within the value.

## What You'll Practice

1. Create counters with `INCR` and observe atomic increment behavior
2. Decrement counters with `DECR` and `DECRBY`
3. Set multiple keys atomically with `MSET` and retrieve with `MGET`
4. Slice strings with `GETRANGE` and modify substrings with `SETRANGE`
5. Use `SETNX` for conditional set — fails if key already exists
6. Check string length with `STRLEN` and append with `APPEND`

## Key Gotchas

- **INCR on non-integer**: `INCR` on a key holding "hello" returns an error. Use `TYPE` to check first.
- **INCR creates keys**: `INCR` on a non-existent key creates it with value 0, then increments to 1.
- **GETRANGE is inclusive**: `GETRANGE key 0 4` returns characters 0 through 4 (5 characters total).
- **SETNX is "set if not exists"**: It returns 0 (didn't set) if the key already exists — no error.
- **String max size**: 512 MB. Don't store large blobs in Redis — use object storage (S3, GCS) and store URLs in Redis.
