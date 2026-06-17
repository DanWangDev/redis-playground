# Exercise 10: Pipelining

## What You'll Learn
- Batch commands with `pipeline(transaction=False)` to reduce round-trips
- Measure performance difference: pipelined vs sequential
- Understand pipelining is NOT atomic (different from MULTI/EXEC)

## Why This Matters
Pipelining reduces network round-trip time from N×RTT to 1×RTT. For bulk inserts, cache warming, and batch operations, it provides 5-100x throughput improvement without the overhead of transactions.

## Core Concepts

### Pipelining vs Transactions

| Feature | Pipelining | MULTI/EXEC |
|---------|-----------|------------|
| Atomic? | No | Yes |
| Reduces RTT? | Yes | Yes |
| Interleavable? | Yes | No |
| Use case | Bulk inserts, cache warm | Account transfers |

## What You'll Practice
1. Execute commands sequentially, measure latency
2. Execute same commands via pipeline, compare speedup
3. Demonstrate non-atomic interleaving
4. Use pipeline for batch reads

## Key Gotchas
- **Not atomic**: Other clients' commands can execute between your pipelined commands.
- **Pipeline replies must be consumed**: Read all replies from `.execute()`.
- **Don't pipeline dependent reads**: If command 2 depends on command 1's result, pipelining won't work.
- **Batch into chunks**: Very large pipelines (~10k+ commands) consume client memory.
