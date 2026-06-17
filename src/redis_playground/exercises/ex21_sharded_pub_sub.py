"""Exercise 21: Sharded Pub/Sub — Redis 7.0+ sharded channel distribution."""

import threading
import time

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner


class Ex21ShardedPubSub(ExerciseRunner):
    def __init__(self):
        super().__init__("21-sharded-pub-sub", "Sharded Pub/Sub")

    def run(self, client: redis.Redis) -> dict:
        results = {}

        self.log.section("Step 1: SPUBLISH Without Subscribers")
        self.log.concept(
            "SPUBLISH sends to a sharded channel, returns subscriber count."
        )
        self.log.concept("Requires Redis 7.0+ — may not be available in fakeredis.")
        try:
            receivers = client.execute_command(
                "SPUBLISH", "orders:new", "Hello, sharded!"
            )
            self.log.command('SPUBLISH orders:new "Hello, sharded!"')
            self.log.output(f"Received by {receivers} subscriber(s)")
            results["spublish_no_sub"] = receivers
            sharded_available = True
        except redis.exceptions.ResponseError:
            self.log.warn("SPUBLISH not available — requires Redis 7.0+")
            self.log.concept(
                "Run with Docker `redis/redis-stack:latest` for sharded Pub/Sub support."
            )
            results["spublish_no_sub"] = 0
            sharded_available = False
            results["sharded_available"] = False
            self.log.separator()
            self.log.success(
                "Sharded Pub/Sub requires Redis 7.0+ — exercise complete (conceptual)"
            )
            return results

        results["sharded_available"] = True
        self.step_pause.pause()

        self.log.section("Step 2: SSUBSCRIBE — Listen on Sharded Channel")
        self.log.concept(
            "SSUBSCRIBE works like SUBSCRIBE but channels are shard-distributed."
        )
        pubsub = client.pubsub()
        pubsub.execute_command("SSUBSCRIBE", "orders:new")
        self.log.command("SSUBSCRIBE orders:new")

        received = []

        def listener():
            for msg in pubsub.listen():
                if msg.get("type") == "smessage":
                    received.append(msg.get("data", ""))

        t = threading.Thread(target=listener, daemon=True)
        t.start()
        time.sleep(0.1)

        client.execute_command("SPUBLISH", "orders:new", "Order #1 created")
        self.log.command('SPUBLISH orders:new "Order #1 created"')
        time.sleep(0.2)
        self.log.output(f"Received: {received}")
        results["message_count"] = len(received)
        pubsub.execute_command("SUNSUBSCRIBE", "orders:new")
        pubsub.close()

        self.log.section("Step 3: Sharded vs Classic — Side by Side")
        self.log.concept(
            "Classic PUBLISH reaches all nodes; SPUBLISH only targets one shard."
        )
        self.log.concept(
            "On a single-node Redis, both behave identically — the difference is in cluster mode."
        )

        # Classic Pub/Sub
        classic_pubsub = client.pubsub()
        classic_pubsub.subscribe("events:classic")
        classic_received = []

        def classic_listener():
            for msg in classic_pubsub.listen():
                if msg.get("type") == "message":
                    classic_received.append(msg.get("data", ""))

        t2 = threading.Thread(target=classic_listener, daemon=True)
        t2.start()
        time.sleep(0.1)
        client.publish("events:classic", "Broadcast message")
        time.sleep(0.2)
        results["classic_received"] = len(classic_received)
        classic_pubsub.unsubscribe("events:classic")
        classic_pubsub.close()

        self.log.command("SUBSCRIBE events:classic → PUBLISH events:classic")
        self.log.output(f"Classic received: {len(classic_received)} message(s)")

        # Sharded Pub/Sub (same pattern, different commands)
        sharded2 = client.pubsub()
        sharded2.execute_command("SSUBSCRIBE", "events:sharded")
        sharded_received = []

        def sharded_listener():
            for msg in sharded2.listen():
                if msg.get("type") == "smessage":
                    sharded_received.append(msg.get("data", ""))

        t3 = threading.Thread(target=sharded_listener, daemon=True)
        t3.start()
        time.sleep(0.1)
        client.execute_command("SPUBLISH", "events:sharded", "Sharded message")
        time.sleep(0.2)
        results["sharded_received"] = len(sharded_received)
        sharded2.execute_command("SUNSUBSCRIBE", "events:sharded")
        sharded2.close()

        self.log.command("SSUBSCRIBE events:sharded → SPUBLISH events:sharded")
        self.log.output(f"Sharded received: {len(sharded_received)} message(s)")
        self.log.concept(
            "Both patterns deliver messages — choose based on scale needs."
        )

        self.log.separator()
        self.log.success(
            f"Sharded Pub/Sub: available={sharded_available}, "
            f"msgs delivered={results['message_count']}, "
            f"classic={results['classic_received']}, sharded={results['sharded_received']}"
        )
        return results
