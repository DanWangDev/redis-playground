# Exercise 08: Streams

## What You'll Learn

- Append entries to a stream with `XADD`
- Read entries with `XREAD` (non-consumer-group)
- Create consumer groups with `XGROUP CREATE`
- Read as a consumer group with `XREADGROUP`
- Acknowledge messages with `XACK`
- Inspect pending entries with `XPENDING`
- Query by range with `XRANGE`

## Why This Matters

Redis Streams are the durable, reliable alternative to Pub/Sub. They provide an append-only log with consumer groups for fan-out message delivery, message acknowledgment (ACK), and pending message inspection. This is the foundation for event sourcing, reliable task queues, and microservice communication.

## Core Concepts

### Stream as an Append-Only Log

```
XADD events * type "page_view" user "alice"
XADD events * type "purchase" user "bob" amount 49.99
```

The `*` tells Redis to auto-generate the entry ID (a timestamp-sequence pair like `1680000000000-0`).

### Consumer Groups

```
XGROUP CREATE events mygroup $ MKSTREAM

# Consumer 1 reads new messages
XREADGROUP GROUP mygroup consumer-1 COUNT 2 STREAMS events >

# After processing, acknowledge
XACK events mygroup 1680000000000-0
```

- `>` means "give me messages never delivered to any consumer in this group"
- `0` or a specific ID means "give me my pending messages"
- Consumer groups enable multiple independent applications to read the same stream

### Pending Entries List (PEL)

Messages delivered to a consumer but not yet acknowledged are "pending." `XPENDING` shows the pending status. If a consumer crashes, another consumer can claim and process its pending messages.

## What You'll Practice

1. Add entries to a stream with XADD (auto-generated IDs)
2. Read entries with XREAD from a starting point
3. Create a consumer group with XGROUP CREATE
4. Read as consumer group with XREADGROUP
5. Acknowledge messages with XACK
6. Check pending entries with XPENDING

## Key Gotchas

- **XREAD is not consumer-group-aware**: Use XREADGROUP for reliable delivery.
- **Unacknowledged messages live forever**: If you never ACK, messages stay in the PEL indefinitely.
- **Consumer groups require explicit creation**: `XGROUP CREATE` fails if the group already exists (use `MKSTREAM` to create the stream if needed).
- **Stream trimming**: Streams grow unboundedly. Use `MAXLEN` with XADD or `XTRIM` to cap them.
