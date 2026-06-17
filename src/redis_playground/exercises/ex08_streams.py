"""Exercise 08: Streams — append-only log, consumer groups, ACK."""

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner


class Ex08Streams(ExerciseRunner):
    def __init__(self):
        super().__init__("08-streams", "Streams")

    def run(self, client: redis.Redis) -> list:
        results = []

        self.log.section("Step 1: XADD — Append to a Stream")
        self.log.concept("XADD adds entries. Use * for auto-generated IDs.")
        client.delete("events")
        id1 = client.xadd(
            "events", {"type": "page_view", "user": "alice", "page": "/home"}
        )
        id2 = client.xadd(
            "events", {"type": "purchase", "user": "bob", "amount": "49.99"}
        )
        self.log.command(
            "XADD events * type page_view ... → XADD events * type purchase ..."
        )
        self.log.output(f"IDs: {id1}, {id2}")
        stream_len = client.xlen("events")
        self.log.output(f"XLEN → {stream_len}")
        results.extend([id1, id2, stream_len])

        self.log.section("Step 2: XREAD — Read Entries")
        entries = client.xread({"events": "0"}, count=2)
        self.log.command("XREAD COUNT 2 STREAMS events 0")
        for _, msgs in entries:
            for msg_id, fields in msgs:
                self.log.output(f"  [{msg_id}] {fields}")
        results.append(len(entries[0][1]) if entries else 0)

        self.log.section("Step 3: XRANGE — Query by Range")
        range_entries = client.xrange("events", "-", "+", count=5)
        self.log.command("XRANGE events - + COUNT 5")
        self.log.output(f"Found {len(range_entries)} entries")
        results.append(len(range_entries))

        self.log.section("Step 4: Consumer Group")
        try:
            client.xgroup_destroy("events", "mygroup")
        except Exception:
            pass
        client.xgroup_create("events", "mygroup", "0", mkstream=False)
        self.log.command("XGROUP CREATE events mygroup 0")
        results.append("mygroup")

        self.log.section("Step 5: XREADGROUP")
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

        self.log.section("Step 6: XACK and XPENDING")
        if msg_ids:
            acked = client.xack("events", "mygroup", *msg_ids)
            self.log.command(f"XACK events mygroup → {acked}")
            pending = client.xpending("events", "mygroup")
            if isinstance(pending, dict):
                pending_count = pending.get("pending", 0)
            else:
                pending_count = int(pending)
            self.log.command(f"XPENDING → {pending_count}")
            results.extend([acked, pending_count])
        else:
            results.extend([0, 0])

        self.log.separator()
        self.log.success(
            f"Streams: {results[2]} entries, delivered={results[6]}, pending={results[8]}"
        )
        return results
