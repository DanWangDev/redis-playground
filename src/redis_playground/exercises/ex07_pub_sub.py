"""Exercise 07: Pub/Sub — real-time messaging with channels and patterns."""

import threading
import time

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner


class Ex07PubSub(ExerciseRunner):
    def __init__(self):
        super().__init__("07-pub-sub", "Pub/Sub")

    def run(self, client: redis.Redis) -> list:
        results = []

        # ── Step 1: PUBLISH without subscribers ────────────────
        self.log.section("Step 1: PUBLISH — Send a Message")
        self.log.concept(
            "PUBLISH returns the number of subscribers that received the message."
        )
        receivers = client.publish("chat:general", "Hello, Redis!")
        self.log.command('PUBLISH chat:general "Hello, Redis!"')
        self.log.output(f"Received by {receivers} subscriber(s)")
        self.log.concept("0 subscribers = message lost. Pub/Sub is fire-and-forget.")
        results.append(receivers)

        # ── Step 2: SUBSCRIBE and receive ──────────────────────
        self.log.section("Step 2: SUBSCRIBE — Listen for Messages")
        self.log.concept(
            "SUBSCRIBE registers interest in a channel. Messages arrive in a listener loop."
        )

        pubsub = client.pubsub()
        pubsub.subscribe("chat:general")
        self.log.command("SUBSCRIBE chat:general")

        received_messages = []

        def listener():
            for message in pubsub.listen():
                if message["type"] == "message":
                    received_messages.append(message["data"])

        t = threading.Thread(target=listener, daemon=True)
        t.start()
        time.sleep(0.1)

        client.publish("chat:general", "Hello, subscribers!")
        self.log.command('PUBLISH chat:general "Hello, subscribers!"')
        time.sleep(0.2)
        self.log.output(f"Subscriber received: {received_messages}")
        results.append(len(received_messages))
        pubsub.unsubscribe("chat:general")
        pubsub.close()
        self.step_pause.pause()

        # ── Step 3: Pattern subscriptions ─────────────────────
        self.log.section("Step 3: PSUBSCRIBE — Pattern Matching")
        self.log.concept("PSUBSCRIBE 'notifications:*' matches email and sms channels.")

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

        t2 = threading.Thread(target=listener2, daemon=True)
        t2.start()
        time.sleep(0.1)

        client.publish("notifications:email", "You have new mail!")
        client.publish("notifications:sms", "Package delivered!")
        client.publish("chat:general", "Won't match notifications:*")
        self.log.command(
            "PUBLISH notifications:email → notifications:sms → chat:general"
        )
        time.sleep(0.2)
        self.log.output(f"Pattern matches received: {len(pattern_messages)}")
        for msg in pattern_messages:
            self.log.output(f"  [{msg['channel']}] {msg['data']}")
        results.append(len(pattern_messages))
        pubsub2.punsubscribe("notifications:*")
        pubsub2.close()

        self.log.separator()
        self.log.success(
            f"Pub/Sub: no-subscribers={results[0]}, received={results[1]}, patterns={results[2]}"
        )
        return results
