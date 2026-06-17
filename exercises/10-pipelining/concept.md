# Exercise 10: Pipelining

## What You'll Learn

- Batch commands with `pipeline(transaction=False)` to reduce round-trips
- Measure the performance difference between pipelined and non-pipelined commands
- Understand the difference between pipelining and MULTI/EXEC transactions

## Why This Matters

Pipelining is a pure performance optimization. Instead of sending one command and waiting for its reply, you send multiple commands at once and read the replies as a batch. This reduces network round-trip time (RTT) from N × RTT to 1 × RTT. For bulk inserts, cache warming, and batch operations, pipelining can provide 5-100x throughput improvement.

## Core Concepts

### Pipelining vs Transactions

| Feature | Pipelining | MULTI/EXEC |
|---------|-----------|------------|
| Atomic? | ❌ No | ✅ Yes |
| Reduces RTT? | ✅ Yes | ✅ Yes |
| Commands interleavable? | ✅ Yes (other clients can interleave) | ❌ No (atomic isolation) |
| Use case | Bulk inserts, cache warm | Account transfers, inventory |

### How Pipelining Works

```
# Without pipelining (3 RTTs)
client.set("key1", "val1")   # Send → wait → reply
client.set("key2", "val2")   # Send → wait → reply
client.set("key3", "val3")   # Send → wait → reply

# With pipelining (1 RTT)
pipe = client.pipeline(transaction=False)
pipe.set("key1", "val1")
pipe.set("key2", "val2")
pipe.set("key3", "val3")
pipe.execute()               # Send all → wait → get all replies
```

### When to Pipeline

- **✅ Bulk data loading**: Insert thousands of keys
- **✅ Cache warming**: Pre-populate cache on startup
- **✅ Batch reads**: MGET handles simple cases, pipeline handles complex ones
- **❌ Atomic operations**: Use MULTI/EXEC or Lua scripts instead
- **❌ Sequential dependencies**: If command 2 depends on command 1's result, don't pipeline them

## What You'll Practice

1. Execute commands one at a time and measure latency
2. Execute the same commands via a pipeline and compare the speedup
3. Verify that pipelined commands are NOT atomic (other commands can interleave)
4. Use pipeline for bulk data insertion

## Key Gotchas

- **Not atomic**: Other clients' commands can execute between your pipelined commands.
- **Pipeline replies must be read**: You must consume all replies from `.execute()` or use `.reset()`.
- **redis-py pipelines buffer in memory**: Very large pipelines can consume memory. Batch into chunks of ~1000 commands.
- **Don't pipeline dependent reads**: If you need the result of GET to decide the next SET, pipelining won't work.
