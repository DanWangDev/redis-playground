"""Exercise 05: Sets — membership, set arithmetic, random sampling."""

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner
from redis_playground.shared.data_factory import seed_article_tags


class Ex05Sets(ExerciseRunner):
    def __init__(self):
        super().__init__("05-sets", "Sets")

    def run(self, client: redis.Redis) -> list:
        results = []

        # ── Step 1: SADD and SISMEMBER ─────────────────────────
        self.log.section("Step 1: SADD and SISMEMBER")
        self.log.concept("Sets store unique members. Adding a duplicate is a no-op.")
        self.log.concept(
            "SISMEMBER is O(1) — instant membership check regardless of set size."
        )

        added = client.sadd("tags:redis", "nosql", "cache", "in-memory", "key-value")
        self.log.command('SADD tags:redis "nosql" "cache" "in-memory" "key-value"')
        self.log.output(f"Added {added} members")

        added2 = client.sadd("tags:redis", "cache")  # duplicate — silently ignored
        self.log.command('SADD tags:redis "cache" (duplicate)')
        self.log.output(f"Added {added2} member(s) — duplicate ignored")

        is_member = client.sismember("tags:redis", "cache")
        not_member = client.sismember("tags:redis", "sql")
        self.log.command("SISMEMBER tags:redis cache → SISMEMBER tags:redis sql")
        self.log.output(f"cache={is_member}, sql={not_member}")
        results.extend([added, added2, is_member, not_member])

        # ── Step 2: Set arithmetic ─────────────────────────────
        self.log.section("Step 2: Set Arithmetic — SINTER, SUNION, SDIFF")
        self.log.concept(
            "SINTER finds common members. SUNION combines. SDIFF finds what's exclusive to set A."
        )

        seed_article_tags(client)
        self.log.command("Seeded article tags for 4 articles")

        common = client.sinter("article:1:tags", "article:2:tags")
        self.log.command("SINTER article:1:tags article:2:tags")
        self.log.output(f"Common tags: {common}")
        results.append(common)

        all_tags = client.sunion("article:1:tags", "article:3:tags")
        self.log.command("SUNION article:1:tags article:3:tags")
        self.log.output(f"All distinct tags: {sorted(all_tags)}")
        results.append(all_tags)

        diff = client.sdiff("article:4:tags", "article:1:tags")
        self.log.command("SDIFF article:4:tags article:1:tags")
        self.log.output(f"Only in article:4: {diff}")
        results.append(diff)

        # ── Step 3: SCARD, SRANDMEMBER ─────────────────────────
        self.log.section("Step 3: SCARD, SRANDMEMBER")
        size = client.scard("article:1:tags")
        self.log.command("SCARD article:1:tags")
        self.log.output(f"→ {size} tags")
        results.append(size)

        random_tags = client.srandmember("article:1:tags", 2)
        self.log.command("SRANDMEMBER article:1:tags 2")
        self.log.output(f"Random: {random_tags}")
        results.append(random_tags)

        # ── Step 4: SREM ───────────────────────────────────────
        self.log.section("Step 4: SREM — Remove Members")
        removed = client.srem("tags:redis", "cache")
        still_there = client.sismember("tags:redis", "cache")
        self.log.command("SREM tags:redis cache")
        self.log.output(f"Removed {removed}, exists now: {still_there}")
        results.extend([removed, still_there])

        self.log.separator()
        self.log.success(
            f"Set ops: SADD={results[0]}, SINTER={results[4]}, "
            f"SUNION size={len(results[5])}, SDIFF={results[6]}, SCARD={results[7]}"
        )
        return results
