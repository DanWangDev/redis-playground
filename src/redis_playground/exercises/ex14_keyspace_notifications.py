"""Exercise 14: Keyspace Notifications — real-time key event monitoring."""

import threading
import time

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner


class Ex14KeyspaceNotifications(ExerciseRunner):
    def __init__(self):
        super().__init__("14-keyspace-notifications", "Keyspace Notifications")

    def run(self, client: redis.Redis) -> dict:
        results = {}

        self.log.section("Step 1: Enable Keyspace Notifications")
        try:
            client.config_set("notify-keyspace-events", "Kgx")
            self.log.command('CONFIG SET notify-keyspace-events "Kgx"')
            self.log.success("K=keyspace, g=generic, x=expired events enabled")
        except Exception:
            self.log.warn("CONFIG SET not available (fakeredis) — skipping")
        results["config_set"] = True

        self.log.section("Step 2: Subscribe to Keyspace Events")
        self.log.concept(
            "PSUBSCRIBE __keyspace@0__:* monitors all key events in database 0."
        )
        pubsub = client.pubsub()
        pubsub.psubscribe("__keyspace@0__:*")
        self.log.command("PSUBSCRIBE __keyspace@0__:*")
        events = []
        stop = threading.Event()

        def listener():
            try:
                for msg in pubsub.listen():
                    if stop.is_set():
                        break
                    if msg["type"] == "pmessage":
                        events.append({"channel": msg["channel"], "data": msg["data"]})
            except Exception:
                pass

        t = threading.Thread(target=listener, daemon=True)
        t.start()
        time.sleep(0.1)

        self.log.section("Step 3: Trigger Events")
        client.set("notify:key1", "value1")
        client.set("notify:key2", "value2")
        client.delete("notify:key2")
        self.log.command("SET notify:key1 → SET notify:key2 → DEL notify:key2")
        time.sleep(0.3)
        self.log.output(f"Captured {len(events)} event(s)")
        for e in events[:5]:
            self.log.output(f"  [{e['channel']}] {e['data']}")
        results["event_count"] = len(events)
        stop.set()
        pubsub.close()
        t.join(timeout=1.0)

        self.log.separator()
        self.log.success(f"Keyspace notifications: {len(events)} events captured")
        return results
