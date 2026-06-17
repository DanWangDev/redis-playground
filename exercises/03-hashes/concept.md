# Exercise 03: Hashes

## What You'll Learn

- Store objects as field-value pairs with `HSET`
- Retrieve fields with `HGET`, `HGETALL`, `HMGET`
- Atomic field increments with `HINCRBY`
- Delete fields with `HDEL`
- Inspect hash structure with `HEXISTS`, `HLEN`, `HKEYS`, `HVALS`

## Why This Matters

Redis Hashes are the primary way to store objects (user profiles, product catalogs, session data). Unlike storing JSON as a string, hashes allow atomic operations on individual fields — you can increment a counter field without reading the entire object. They are memory-efficient: small hashes (under ~512 fields) use a compact ziplist encoding that saves significant memory.

## Core Concepts

### Object-as-Hash Pattern

```
HSET user:1 name "Alice" email "alice@example.com" age 28 plan "pro"
```

This is the Redis equivalent of:
```sql
INSERT INTO users (id, name, email, age, plan)
VALUES (1, 'Alice', 'alice@example.com', 28, 'pro');
```

But unlike SQL, you can atomically `HINCRBY user:1 age 1` without a read-then-write race condition.

### Memory Efficiency

Small hashes (few fields, small values) use a ziplist encoding internally — ~5-10x less memory than storing the same data as separate string keys. This changes to a hash table encoding when the hash grows large (controlled by `hash-max-ziplist-entries` and `hash-max-ziplist-value`).

## What You'll Practice

1. Create user profiles with `HSET` using `mapping` parameter
2. Retrieve individual fields with `HGET` and multiple fields with `HMGET`
3. Fetch the entire hash with `HGETALL`
4. Increment numeric fields atomically with `HINCRBY`
5. Delete fields with `HDEL` and verify removal
6. Check field existence with `HEXISTS` and count fields with `HLEN`

## Key Gotchas

- **HGETALL is O(N)**: It returns all fields and values. On a hash with millions of fields, this is expensive. Use `HSCAN` for large hashes.
- **HINCRBY on non-numeric**: Errors if the field contains non-numeric data.
- **HSET overwrites**: Setting an existing field silently overwrites its value.
- **Deleted fields disappear**: `HGET` on a deleted field returns `None`. `HEXISTS` returns 0. The hash itself is deleted when the last field is removed.
