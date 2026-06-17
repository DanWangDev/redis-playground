# Exercise 07: Pub/Sub

## What You'll Learn
- Publish messages to channels with `PUBLISH`
- Subscribe to channels with `SUBSCRIBE`
- Use pattern-based subscriptions with `PSUBSCRIBE`
- Understand fire-and-forget delivery semantics

## Why This Matters
Redis Pub/Sub enables real-time messaging between application components — chat systems, live notifications, service health monitoring. Unlike Streams (Ex08), Pub/Sub is fire-and-forget: messages aren't persisted, and subscribers only receive messages published while they are actively subscribed.

## Core Concepts
- **PUBLISH** sends a message to a channel, returns subscriber count
- **SUBSCRIBE** registers interest in a specific channel
- **PSUBSCRIBE** subscribes to channels matching a glob pattern (e.g., `notifications:*`)
- **No persistence**: If no subscriber is listening, the message is lost

## Key Gotchas
- Messages aren't persisted — Pub/Sub is NOT a message queue. Use Streams for durability.
- SUBSCRIBE blocks the connection — use a separate PubSub object and listener thread.
- Pattern subscriptions match ALL matching channels — `PSUBSCRIBE *` subscribes to everything.
