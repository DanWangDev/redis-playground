# Exercise 21: Sharded Pub/Sub

## What You'll Learn
- Subscribe to sharded channels with `SSUBSCRIBE`
- Publish to sharded channels with `SPUBLISH`
- Unsubscribe with `SUNSUBSCRIBE`
- Understand the difference between sharded and classic Pub/Sub
- Know when to use each pattern

## Why This Matters

Classic Pub/Sub (Exercise 07) broadcasts every message to **every cluster node**, regardless of whether any subscriber exists on that node. This wastes bandwidth and CPU at scale. Redis 7.0 introduced **Sharded Pub/Sub** where channels are distributed across cluster shards — a message published to `orders:new` only goes to the shard that owns that channel. This is the production Pub/Sub pattern for Redis Cluster deployments.

## Core Concepts

### Classic vs Sharded Pub/Sub

| Feature | Classic (Ex07) | Sharded (Ex21) |
|---------|---------------|----------------|
| Subscribe | `SUBSCRIBE` | `SSUBSCRIBE` |
| Publish | `PUBLISH` | `SPUBLISH` |
| Unsubscribe | `UNSUBSCRIBE` | `SUNSUBSCRIBE` |
| Pattern subscribe | `PSUBSCRIBE` | Not supported |
| Channel distribution | Broadcast to ALL nodes | Hashed to one shard |
| Use case | Cross-cluster notifications | High-throughput messaging |

### How Sharding Works

Redis hashes the channel name to a hash slot (same CRC16 as key hashing). The message only goes to the node that owns that slot. This means:

```
SPUBLISH orders:new "Order #123 created"
→ CRC16("orders:new") mod 16384 = slot 9273
→ Only the node owning slot 9273 processes the message
→ Only subscribers ON THAT NODE receive it
```

Contrast with classic `PUBLISH` where every node broadcasts to its local subscribers.

### When to Use Sharded Pub/Sub

- **✅ Cluster deployments** — reduces cross-node traffic
- **✅ High-throughput messaging** — millions of messages/sec
- **✅ Channel-per-entity patterns** — one channel per user/session
- **❌ Pattern subscriptions needed** — sharded doesn't support `PSUBSCRIBE`
- **❌ Single-node deployments** — no benefit without sharding

## What You'll Practice

1. Subscribe to a sharded channel with SSUBSCRIBE
2. Publish messages with SPUBLISH
3. Observe that SPUBLISH returns the subscriber count (like PUBLISH)
4. Unsubscribe with SUNSUBSCRIBE
5. Compare with classic Pub/Sub side-by-side

## Key Gotchas

- **No pattern subscriptions**: Sharded Pub/Sub doesn't support `PSUBSCRIBE`. Use classic Pub/Sub for patterns.
- **Cluster-only benefit**: On a single-node Redis, sharded Pub/Sub behaves identically to classic.
- **Client library support**: Ensure your Redis client supports `SSUBSCRIBE` (redis-py 4.5+).
- **Same connection semantics**: Like classic Pub/Sub, SSUBSCRIBE blocks the connection — use a separate thread.
- **Requires Redis 7.0+**: Older Redis versions don't have sharded Pub/Sub commands.
