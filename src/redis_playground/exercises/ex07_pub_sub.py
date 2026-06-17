"""Exercise 07: Pub/Sub.

Explore Redis Pub/Sub: PUBLISH, SUBSCRIBE, PSUBSCRIBE (pattern matching),
and fire-and-forget message delivery semantics.
"""

import threading
import time

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner


class Ex07PubSub(ExerciseRunner):
    def __init__(self):
        super().__init__("07-pub-sub", "Pub/Sub")

    def run(self, client: redis.Redis) -> list:
        results = []

        # ── Step 1: Basic PUBLISH ───────────────────────────────
        self.log.section("Step 1: PUBLISH — Send a Message")
        self.log.concept(
            "PUBLISH sends a message to a channel and returns the number of subscribers."
        )
        self.log.concept("If no one is subscribed, it returns 0 — the message is lost.")

        receivers = client.publish("chat:general", "Hello, Redis!")
        self.log.command('PUBLISH chat:general "Hello, Redis!"')
        self.log.output(f"Received by {receivers} subscriber(s)")
        self.log.concept("0 subscribers = message lost. Pub/Sub is fire-and-forget.")
        results.append(receivers)

        # ── Step 2: Subscribe and receive ──────────────────────
        self.log.section("Step 2: SUBSCRIBE — Listen for Messages")
        self.log.concept(
            "SUBSCRIBE registers interest in a channel. Messages arrive in a listener loop."
        )
        self.log.concept(
            "In redis-py, we use a separate PubSub object and a listener thread."
        )

        # Create a pubsub connection and subscribe in a thread
        pubsub = client.pubsub()
        pubsub.subscribe("chat:general")
        self.log.command("SUBSCRIBE chat:general")

        # Use a list to collect received messages from the listener thread
        received_messages = []

        def listener():
            for message in pubsub.listen():
                if message["type"] == "message":
                    received_messages.append(message["data"])

        listener_thread = threading.Thread(target=listener, daemon=True)
        listener_thread.start()

        # Give the subscriber time to connect
        time.sleep(0.1)

        # Publish a message — this one should be received
        client.publish("chat:general", "Hello, subscribers!")
        self.log.command('PUBLISH chat:general "Hello, subscribers!"')

        time.sleep(0.2)  # Allow message to arrive
        self.log.output(f"Subscriber received: {received_messages}")
        results.append(len(received_messages))

        # Clean up
        pubsub.unsubscribe("chat:general")
        pubsub.close()
        self.step_pause.pause()

        # ── Step 3: Pattern subscriptions ─────────────────────
        self.log.section("Step 3: PSUBSCRIBE — Pattern Matching")
        self.log.concept("PSUBSCRIBE subscribes to channels matching a glob pattern.")
        self.log.concept(
            "Example: 'notifications:*' matches 'notifications:email' and 'notifications:sms'."
        )

        pubsub2 = client.pubsub()
        pubsub2.psubscribe("notifications:*")
        self.log.command("PSUBSCRIBE notifications:*")

        pattern_messages = []

        def listener2():
            for message in pubsub2.listen():
                if message["type"] == "pmessage":
                    pattern_messages.append(
                        {"channel": message["channel"], "data": message["data"]}
                    )

        t = threading.Thread(target=listener2, daemon=True)
        t.start()
        time.sleep(0.1)

        client.publish("notifications:email", "You have new mail!")
        client.publish("notifications:sms", "Package delivered!")
        client.publish("chat:general", "This won't match the pattern")
        self.log.command('PUBLISH notifications:email "You have new mail!"')
        self.log.command('PUBLISH notifications:sms "Package delivered!"')
        self.log.command('PUBLISH chat:general "This won\'t match the pattern"')

        time.sleep(0.2)
        self.log.output(f"Pattern matches received: {len(pattern_messages)}")
        for msg in pattern_messages:
            self.log.output(f"  [{msg['channel']}] {msg['data']}")
        results.append(len(pattern_messages))

        pubsub2.punsubscribe("notifications:*")
        pubsub2.close()

        # ── Summary ─────────────────────────────────────────────
        self.log.separator()
        self.log.success(
            f"Pub/Sub: no-subscribers={results[0]}, "
            f"messages received={results[1]}, "
            f"pattern matches={results[2]}"
        )
        return results
