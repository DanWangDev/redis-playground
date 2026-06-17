# Exercise 01: Basic Commands

## What You'll Learn

- Connect to Redis and verify the connection with `PING`
- Store and retrieve string values with `SET` and `GET`
- Delete keys with `DEL`
- Check key existence with `EXISTS`
- Set key expiration with `EXPIRE` and inspect TTL with `TTL`
- Understand that `KEYS *` is O(N) — a debugging tool, not for production use
- Inspect key type with `TYPE`

## Why This Matters

These are the fundamental CRUD operations of Redis. Every other exercise builds on `SET`, `GET`, `DEL`, `EXISTS`, and `EXPIRE`. Understanding the key lifecycle — creation, mutation, expiration, deletion — is essential before tackling data structures like hashes, lists, and streams.

## Core Concepts

### The Redis Key Space

Redis is a key-value store. Every piece of data is stored under a key. Keys are binary-safe strings (but we use human-readable strings in practice). The key space is flat — there are no "tables" or "collections" like in a relational database. Convention uses colon-separated namespaces: `user:1`, `article:42:title`, `session:abc123`.

### Key Lifecycle

```
SET user:1 "Alice"     →  Key exists, value is "Alice"
EXPIRE user:1 3600     →  Key exists, TTL counts down from 3600 seconds
TTL user:1             →  Returns remaining seconds (e.g., 3587)
DEL user:1             →  Key deleted immediately
TTL user:1             →  Returns -2 (key does not exist)
```

### TTL Return Values

| TTL Value | Meaning |
|-----------|---------|
| Positive integer | Key exists and will expire in N seconds |
| `-1` | Key exists but has no expiry (persistent) |
| `-2` | Key does not exist |

### KEYS is O(N)

`KEYS pattern` scans the ENTIRE keyspace. In a database with millions of keys, this blocks the Redis server. Use `SCAN` for production (covered in a later exercise). `KEYS` is fine for learning and debugging.

## What You'll Practice

1. Connect to Redis and send a `PING` (should return `PONG`)
2. Set a key with `SET name "Alice"` and retrieve it with `GET name`
3. Set multiple keys and verify them with `EXISTS`
4. Set a key with expiration and watch it count down with `TTL`
5. Delete a key and verify it's gone (`TTL` returns `-2`)
6. List all keys with `KEYS *` and inspect types with `TYPE`

## Key Gotchas

- **KEYS blocks the server**: `KEYS` is a synchronous O(N) scan. Never use it in production code. Use `SCAN` instead.
- **TTL returns -1 vs -2**: `-1` means "no expiry set" (the key is persistent). `-2` means "key doesn't exist." Don't confuse them.
- **EXPIRE overwrites**: Calling `EXPIRE` on a key that already has a TTL resets the timer to the new value.
- **SET overwrites expiry**: `SET` without `EX`/`PX` removes any existing TTL — the key becomes persistent. Use `SET key value EX 3600` to set with expiry in one command.
- **DEL is silent**: `DEL` returns the number of keys deleted (0 or 1 for a single key). It doesn't error if the key doesn't exist.
