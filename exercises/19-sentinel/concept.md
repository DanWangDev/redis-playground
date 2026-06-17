# Exercise 19: Redis Sentinel

## What You'll Learn
- Understand Sentinel architecture: monitoring, failover, discovery
- Query master address with `SENTINEL get-master-addr-by-name`
- Discover replicas with `SENTINEL replicas`
- Configure a Sentinel-aware Redis client

## Why This Matters
Redis Sentinel provides high availability without sharding. Multiple Sentinel processes monitor Redis instances, agree on failures via quorum, and automatically promote a replica to master. Clients use Sentinel for discovery — they ask Sentinel for the current master address rather than connecting to a fixed IP.

## Core Concepts
- **Sentinel**: A separate process (`redis-sentinel`) that monitors Redis instances
- **Quorum**: Number of Sentinels that must agree a master is down before failover
- **Failover**: Sentinel promotes a replica to master and reconfigures other replicas
- **Discovery**: Clients query Sentinel for current master (`SENTINEL get-master-addr-by-name`)

## Key Gotchas
- Sentinel provides HA but NOT sharding. For horizontal scaling, use Redis Cluster (Ex20).
- Clients must be sentinel-aware to follow failovers (redis-py: `Sentinel` class).
- Quorum vs majority: quorum detects failure, majority elects the leader Sentinel.
- Minimum 3 Sentinel instances for a reliable deployment.
