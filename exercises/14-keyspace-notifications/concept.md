# Exercise 14: Keyspace Notifications

## What You'll Learn
- Enable keyspace events with `CONFIG SET notify-keyspace-events`
- Subscribe to key events with `PSUBSCRIBE __keyspace@*` / `__keyevent@*`
- Detect key creation, deletion, expiration
- Understand delivery guarantees: fire-and-forget

## Why This Matters
Keyspace notifications allow your application to react to data changes in real time — cache invalidation, session expiry cleanup, audit logging. Combined with key expiry, they enable TTL-based workflows without polling.

## Core Concepts
- `notify-keyspace-events` config string: K=keyspace, E=keyevent, g=generic, $=string, l=list, s=set, h=hash, z=sorted set, x=expired, e=evicted
- `Kx` enables expired key notifications — used for TTL-based callbacks
- Delivered via Pub/Sub channels

## Key Gotchas
- Notifications are fire-and-forget — if subscriber is down, events are lost.
- High event volume can saturate the Pub/Sub channel.
- `notify-keyspace-events` is disabled by default — must be explicitly configured.
