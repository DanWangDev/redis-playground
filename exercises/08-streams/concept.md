# Exercise 08: Streams

## What You'll Learn
- Append entries with `XADD`
- Read entries with `XREAD` and `XRANGE`
- Create consumer groups with `XGROUP CREATE`
- Read as consumer group with `XREADGROUP`
- Acknowledge messages with `XACK`
- Inspect pending entries with `XPENDING`

## Why This Matters
Redis Streams are the durable, reliable alternative to Pub/Sub. They provide an append-only log with consumer groups for fan-out message delivery, message acknowledgment, and pending message inspection — the foundation for event sourcing and reliable task queues.

## Core Concepts
- **XADD** appends entries (field-value pairs) to a stream, auto-generating IDs
- **XREAD** reads from a starting ID (0 = beginning, $ = new only)
- **Consumer groups** enable multiple apps to read the same stream independently
- **XACK** removes messages from the Pending Entries List (PEL)
- **Unacknowledged messages** stay in the PEL forever and can be reclaimed

## Key Gotchas
- XREAD is NOT consumer-group-aware — use XREADGROUP for reliable delivery.
- Unacknowledged messages live forever in the PEL.
- Streams grow unboundedly — use MAXLEN or XTRIM to cap them.
