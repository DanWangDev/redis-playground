"""Exercise 08: Streams.

Explore Redis Streams: append-only log with consumer groups,
message acknowledgment, and pending entry inspection.
XADD, XREAD, XGROUP CREATE, XREADGROUP, XACK, XPENDING, XRANGE.
"""

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner


class Ex08Streams(ExerciseRunner):
    def __init__(self):
        super().__init__("08-streams", "Streams")

    def run(self, client: redis.Redis) -> list:
        results = []

        # ── Step 1: XADD — Append to stream ────────────────────
        self.log.section("Step 1: XADD — Append to a Stream")
        self.log.concept(
            "XADD adds an entry to a stream. Use * for auto-generated IDs."
        )
        self.log.concept("Each entry is a set of field-value pairs (like a mini-hash).")

        client.delete("events")  # Clean start

        id1 = client.xadd(
            "events", {"type": "page_view", "user": "alice", "page": "/home"}
        )
        self.log.command('XADD events * type "page_view" user "alice" page "/home"')
        self.log.output(f"Entry ID: {id1}")

        id2 = client.xadd(
            "events", {"type": "purchase", "user": "bob", "amount": "49.99"}
        )
        self.log.command('XADD events * type "purchase" user "bob" amount "49.99"')
        self.log.output(f"Entry ID: {id2}")

        stream_len = client.xlen("events")
        self.log.command("XLEN events")
        self.log.output(f"Stream length: {stream_len}")
        results.extend([id1, id2, stream_len])

        # ── Step 2: XREAD — Read from stream ───────────────────
        self.log.section("Step 2: XREAD — Read Entries")
        self.log.concept(
            "XREAD reads entries from one or more streams starting at a given ID."
        )
        self.log.concept(
            "Use '0' to read from the beginning, or '$' for new entries only."
        )

        entries = client.xread({"events": "0"}, count=2)
        self.log.command("XREAD COUNT 2 STREAMS events 0")
        for stream_name, msgs in entries:
            for msg_id, fields in msgs:
                self.log.output(f"  [{msg_id}] {fields}")
        results.append(len(entries[0][1]) if entries else 0)

        # ── Step 3: XRANGE — Query by range ────────────────────
        self.log.section("Step 3: XRANGE — Query by Range")
        range_entries = client.xrange("events", "-", "+", count=5)
        self.log.command("XRANGE events - + COUNT 5")
        for msg_id, fields in range_entries:
            self.log.output(f"  [{msg_id}] type={fields.get('type')}")
        results.append(len(range_entries))

        # ── Step 4: Consumer group ─────────────────────────────
        self.log.section("Step 4: XGROUP CREATE — Consumer Group")
        self.log.concept(
            "Consumer groups enable fan-out: multiple apps can read the same stream independently."
        )
        self.log.concept("Each consumer in a group gets its own subset of messages.")

        # Create consumer group (destroy first if exists)
        try:
            client.xgroup_destroy("events", "mygroup")
        except Exception:
            pass
        client.xgroup_create("events", "mygroup", "0", mkstream=False)
        self.log.command("XGROUP CREATE events mygroup 0")
        self.log.success("Consumer group 'mygroup' created")
        results.append("mygroup")

        # ── Step 5: XREADGROUP — Read as consumer ──────────────
        self.log.section("Step 5: XREADGROUP — Read as Consumer Group")
        self.log.concept("XREADGROUP reads messages assigned to a consumer in a group.")
        self.log.concept(
            "Use '>' to get new (never-delivered) messages. Use '0' for pending messages."
        )

        group_msgs = client.xreadgroup(
            "mygroup", "consumer-1", {"events": ">"}, count=2
        )
        self.log.command("XREADGROUP GROUP mygroup consumer-1 COUNT 2 STREAMS events >")
        msg_ids = []
        for _, msgs in group_msgs:
            for msg_id, fields in msgs:
                self.log.output(f"  [{msg_id}] {fields}")
                msg_ids.append(msg_id)
        results.append(len(msg_ids))

        self.step_pause.pause()

        # ── Step 6: XACK — Acknowledge messages ────────────────
        self.log.section("Step 6: XACK — Acknowledge Messages")
        self.log.concept("XACK removes messages from the pending entries list (PEL).")
        self.log.concept(
            "Without ACK, messages stay pending forever and are redelivered to other consumers."
        )

        if msg_ids:
            acked = client.xack("events", "mygroup", *msg_ids)
            self.log.command(f"XACK events mygroup {msg_ids}")
            self.log.output(f"Acknowledged {acked} message(s)")
            results.append(acked)

            # Check pending — should be 0 after ACK
            pending_raw = client.xpending("events", "mygroup")
            self.log.command("XPENDING events mygroup")
            # xpending returns dict in redis-py 5.x, int in some fakeredis versions
            if isinstance(pending_raw, dict):
                pending_count = pending_raw.get("pending", 0)
            else:
                pending_count = int(pending_raw)
            self.log.output(f"Pending: {pending_count}")
            results.append(pending_count)
        else:
            results.extend([0, 0])

        # ── Summary ─────────────────────────────────────────────
        self.log.separator()
        self.log.success(
            f"Streams: {results[2]} entries, group='{results[5]}', "
            f"xread={results[3]}, xrange={results[4]}, "
            f"delivered={results[6]}, acked={results[7]}, pending={results[8]}"
        )
        return results
