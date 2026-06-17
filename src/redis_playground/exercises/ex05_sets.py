"""Exercise 05: Sets.

Explore Redis set operations: SADD, SISMEMBER, SREM,
SINTER, SUNION, SDIFF, SMEMBERS, SCARD, SRANDMEMBER.
"""

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner
from redis_playground.shared.data_factory import seed_article_tags


class Ex05Sets(ExerciseRunner):
    def __init__(self):
        super().__init__("05-sets", "Sets")

    def run(self, client: redis.Redis) -> list:
        results = []

        # ── Step 1: Add members and test membership ────────────
        self.log.section("Step 1: SADD and SISMEMBER")
        self.log.concept("Sets store unique members. Adding a duplicate is a no-op.")
        self.log.concept("SISMEMBER is O(1) — instant membership check regardless of set size.")

        added = client.sadd("tags:redis", "nosql", "cache", "in-memory", "key-value")
        self.log.command('SADD tags:redis "nosql" "cache" "in-memory" "key-value"')
        self.log.output(f"Added {added} members")

        # Add a duplicate — should be silently ignored
        added2 = client.sadd("tags:redis", "cache")
        self.log.command('SADD tags:redis "cache"')
        self.log.output(f"Added {added2} member(s) (duplicate ignored)")

        is_member = client.sismember("tags:redis", "cache")
        not_member = client.sismember("tags:redis", "sql")
        self.log.command("SISMEMBER tags:redis cache")
        self.log.output(f"→ {is_member}")
        self.log.command("SISMEMBER tags:redis sql")
        self.log.output(f"→ {not_member}")
        results.extend([added, added2, is_member, not_member])

        # ── Step 2: Set arithmetic ─────────────────────────────
        self.log.section("Step 2: Set Arithmetic — SINTER, SUNION, SDIFF")
        self.log.concept("SINTER finds common members across sets — like 'friends in common'.")
        self.log.concept("SUNION combines all members from all sets — like 'all interests'.")
        self.log.concept("SDIFF finds members in set A that are NOT in set B — like 'missing tags'.")

        seed_article_tags(client)
        self.log.command("Seeded article tags for 4 articles")

        # Intersection: tags common to article:1 and article:2
        common = client.sinter("article:1:tags", "article:2:tags")
        self.log.command("SINTER article:1:tags article:2:tags")
        self.log.output(f"Common tags: {common}")
        results.append(common)

        # Union: all distinct tags across article:1 and article:3
        all_tags = client.sunion("article:1:tags", "article:3:tags")
        self.log.command("SUNION article:1:tags article:3:tags")
        self.log.output(f"All tags: {all_tags}")
        results.append(all_tags)

        # Difference: tags in article:4 that article:1 doesn't have
        diff = client.sdiff("article:4:tags", "article:1:tags")
        self.log.command("SDIFF article:4:tags article:1:tags")
        self.log.output(f"Tags only in article:4: {diff}")
        results.append(diff)

        # ── Step 3: Metadata and random member ─────────────────
        self.log.section("Step 3: SCARD, SMEMBERS, SRANDMEMBER")
        self.log.concept("SCARD returns the cardinality (size) of a set — O(1).")
        self.log.concept("SRANDMEMBER returns a random member without removing it.")

        size = client.scard("article:1:tags")
        self.log.command("SCARD article:1:tags")
        self.log.output(f"→ {size} tags")
        results.append(size)

        random_tag = client.srandmember("article:1:tags", 2)
        self.log.command("SRANDMEMBER article:1:tags 2")
        self.log.output(f"Random tags: {random_tag}")
        results.append(random_tag)

        # ── Step 4: Remove members ─────────────────────────────
        self.log.section("Step 4: SREM — Remove Members")
        self.log.concept("SREM removes one or more members from a set.")
        self.log.concept("Returns the count of actually removed members.")

        removed = client.srem("tags:redis", "cache")
        self.log.command("SREM tags:redis cache")
        self.log.output(f"Removed {removed} member(s)")

        still_there = client.sismember("tags:redis", "cache")
        self.log.command("SISMEMBER tags:redis cache")
        self.log.output(f"→ {still_there}")
        results.extend([removed, still_there])

        # ── Summary ─────────────────────────────────────────────
        self.log.separator()
        self.log.success(
            f"Set operations: SADD={results[0]}, dup={results[1]}, "
            f"ISMEMBER={results[2]}, NOT_MEMBER={results[3]}, "
            f"SINTER={results[4]}, SUNION size={len(results[5])}, "
            f"SDIFF={results[6]}, SCARD={results[7]}, "
            f"SREM={results[9]}"
        )
        return results
