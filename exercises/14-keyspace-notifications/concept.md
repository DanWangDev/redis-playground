# Exercise 14: Keyspace Notifications

## What You'll Learn
- Enable keyspace events with `CONFIG SET notify-keyspace-events`
- Subscribe to key events with `PSUBSCRIBE __keyspace@*`
- Detect key creation, deletion, expiration
- Understand fire-and-forget delivery guarantees

## Why This Matters
Keyspace notifications allow your application to react to data changes in real time — cache invalidation, session expiry cleanup, audit logging.

## Core Concepts
- `notify-keyspace-events` config string: K=keyspace, E=keyevent, g=generic, x=expired
- Delivered via Pub/Sub channels `__keyspace@0__:*` and `__keyevent@0__:*`

## Key Gotchas
- Notifications are fire-and-forget — if subscriber is down, events are lost.
- `notify-keyspace-events` is disabled by default.
- High event volume can saturate the Pub/Sub channel.
