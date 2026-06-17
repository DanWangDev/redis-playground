# Exercise 07: Pub/Sub

## What You'll Learn

- Publish messages to channels with `PUBLISH`
- Subscribe to channels with `SUBSCRIBE` and receive messages in real time
- Use pattern-based subscriptions with `PSUBSCRIBE`
- Understand Pub/Sub message delivery semantics (fire-and-forget)

## Why This Matters

Redis Pub/Sub enables real-time messaging between application components. It's the foundation for chat systems, live notifications, service health monitoring, and event-driven architectures. Unlike message queues (covered in Exercise 08), Pub/Sub is fire-and-forget — messages are not persisted, and subscribers only receive messages published while they are actively subscribed.

## Core Concepts

### Publish-Subscribe Model

```
Publisher ──PUBLISH channel "hello"──→ Redis ──→ Subscriber 1 (subscribed to "channel")
                                              ──→ Subscriber 2 (subscribed to "channel")
                                              ✗  Subscriber 3 (not subscribed yet — misses message)
```

### Channel vs Pattern Subscription

- `SUBSCRIBE channel` — receive messages on a specific channel
- `PSUBSCRIBE notifications:*` — receive messages on any channel matching the pattern

### Delivery Semantics

- **Fire-and-forget**: Published messages go to all currently connected subscribers and are not stored.
- **No persistence**: If no subscriber is listening, the message is lost.
- **No acknowledgment**: Subscribers can't ACK/NACK messages. If a subscriber disconnects, it misses messages.

For reliable message delivery, use Redis Streams (Exercise 08).

## What You'll Practice

1. Publish a message to a channel with PUBLISH
2. Observe that PUBLISH returns the number of subscribers who received the message
3. Use PSUBSCRIBE with a pattern to match multiple channels
4. Understand that messages sent before subscription are lost

## Key Gotchas

- **Messages aren't persisted**: Pub/Sub is NOT a message queue. Use Streams for durable messaging.
- **SUBSCRIBE blocks the connection**: In redis-py, `pubsub.listen()` blocks and yields messages. Use a separate connection or thread for subscriptions.
- **Pattern subscriptions match any channel**: `PSUBSCRIBE *` subscribes to EVERYTHING — use carefully.
- **Unsubscribe before disconnecting**: Clean up subscriptions with `UNSUBSCRIBE` to avoid stale subscriber entries.
