# Exercise 22: SCAN — Cursor-Based Iteration

## What You'll Learn
- Iterate keys safely with `SCAN`
- Iterate hash fields with `HSCAN`
- Iterate set members with `SSCAN`
- Iterate sorted set members with `ZSCAN`
- Understand why SCAN is production-safe while KEYS is not

## Why This Matters

`KEYS *` (covered in Ex01) blocks the entire Redis server while scanning — on a database with millions of keys, this can cause seconds-long pauses. `SCAN` uses a cursor-based approach that returns small batches and never blocks. It's the only safe way to iterate keys in production.

## Core Concepts

### How SCAN Works

```
SCAN 0 COUNT 100
→ Returns: (next_cursor, [keys...])
SCAN next_cursor COUNT 100
→ Returns: (0, [keys...])  # cursor 0 means done
```

Each `SCAN` call returns a batch of keys and a cursor for the next batch. When the cursor returns `0`, iteration is complete. `COUNT` is a hint, not a guarantee — Redis may return fewer or more keys per batch.

### Variants

| Command | Iterates Over |
|---------|--------------|
| `SCAN` | All keys in the database |
| `HSCAN` | Fields in a hash |
| `SSCAN` | Members in a set |
| `ZSCAN` | Members + scores in a sorted set |

### SCAN Guarantees (and Lack Thereof)

- ✅ Non-blocking: Each call returns quickly
- ⚠️ May return duplicates: A key added during iteration may appear twice
- ⚠️ May miss keys: A key deleted during iteration may not appear
- ✅ Eventually consistent: The full iteration reflects approximately the state at start

## What You'll Practice

1. Seed many keys, then iterate with SCAN
2. Compare SCAN vs KEYS behavior
3. Iterate hash fields with HSCAN
4. Iterate set members with SSCAN
5. Iterate sorted set members with ZSCAN (with scores)

## Key Gotchas

- **COUNT is a hint**: Redis may return more or fewer keys than requested.
- **Duplicates possible**: If keys are added during iteration, they may appear twice.
- **Cursor is opaque**: Don't try to interpret cursor values — just pass them to the next call.
- **Database changes during scan**: Added keys may or may not appear; deleted keys may still appear.
