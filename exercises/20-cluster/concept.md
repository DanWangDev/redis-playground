# Exercise 20: Redis Cluster

## What You'll Learn
- Understand hash slots (16384 slots) and key distribution
- Check which slot a key maps to with `CLUSTER KEYSLOT`
- Handle `MOVED` and `ASK` redirects
- Understand multi-key operation constraints
- Use hash tags `{key}` for co-location

## Why This Matters
Redis Cluster provides horizontal scaling beyond single-node memory capacity. Data is sharded across multiple nodes using hash slots. Each node owns a subset of slots, and clients are redirected to the correct node. This is the production architecture for large-scale Redis deployments.

## Core Concepts
- **16384 hash slots**: The entire keyspace is divided into 16384 slots
- **CRC16 hash**: `HASH_SLOT = CRC16(key) mod 16384`
- **MOVED redirect**: Permanent — "this slot is now owned by node X"
- **ASK redirect**: Temporary — "this slot is being migrated, ask node X"
- **Hash tags**: `user:{123}:name` — only the `{123}` part is hashed

## Key Gotchas
- Multi-key commands only work if ALL keys hash to the same slot.
- Use hash tags `{user:123}` to force keys to the same slot.
- Cross-slot transactions are NOT supported.
- Clients must handle MOVED/ASK errors (redis-py ClusterClient does this automatically).
- Cluster requires at least 3 master nodes for a minimal deployment.
