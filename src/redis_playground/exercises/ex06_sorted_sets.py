"""Exercise 06: Sorted Sets.

Redis's most versatile data structure — leaderboards, rankings,
priority queues with ZADD, ZRANGE, ZRANK, ZSCORE, ZINCRBY, ZCOUNT.
"""

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner
from redis_playground.shared.data_factory import seed_leaderboard


class Ex06SortedSets(ExerciseRunner):
    def __init__(self):
        super().__init__("06-sorted-sets", "Sorted Sets")

    def run(self, client: redis.Redis) -> list:
        results = []

        # ── Step 1: Create a leaderboard ───────────────────────
        self.log.section("Step 1: ZADD — Build a Leaderboard")
        self.log.concept(
            "Each member has a score. Members are always ordered by score."
        )
        self.log.concept("ZADD with a dict maps member → score in one command.")

        key = seed_leaderboard(client)
        self.log.command(f"ZADD {key} (10 players with scores)")
        size = client.zcard(key)
        self.log.output(f"Leaderboard size: {size}")
        results.append(size)

        # ── Step 2: Top N with ZREVRANGE ──────────────────────
        self.log.section("Step 2: ZREVRANGE — Top Players")
        self.log.concept(
            "ZREVRANGE returns members in reverse order (highest score first)."
        )
        self.log.concept("WITHSCORES includes scores in the response.")

        top3 = client.zrevrange(key, 0, 2, withscores=True)
        self.log.command(f"ZREVRANGE {key} 0 2 WITHSCORES")
        self.log.table(
            ["Rank", "Player", "Score"],
            [[str(i + 1), name, str(score)] for i, (name, score) in enumerate(top3)],
        )
        results.append(top3)

        # ── Step 3: Rank and reverse rank ─────────────────────
        self.log.section("Step 3: ZRANK — Find a Player's Position")
        self.log.concept("ZRANK returns 0-indexed position (lowest score = rank 0).")
        self.log.concept("ZREVRANK returns 0-indexed position from highest score.")

        rank = client.zrank(key, "player:eve")
        rev_rank = client.zrevrank(key, "player:eve")
        score = client.zscore(key, "player:eve")
        self.log.command(f"ZRANK {key} player:eve")
        self.log.output(f"→ Rank {rank} (0-indexed from bottom), Score: {score}")
        self.log.command(f"ZREVRANK {key} player:eve")
        self.log.output(f"→ Reverse rank {rev_rank} (0-indexed from top)")
        results.extend([rank, rev_rank, score])

        # ── Step 4: Increment scores ──────────────────────────
        self.log.section("Step 4: ZINCRBY — Update Scores")
        self.log.concept("ZINCRBY atomically increments a member's score.")
        self.log.concept(
            "If the member doesn't exist, it's added with the increment as its score."
        )

        new_score = client.zincrby(key, 500, "player:eve")
        self.log.command(f"ZINCRBY {key} 500 player:eve")
        self.log.output(f"player:eve score is now: {new_score}")
        results.append(new_score)

        new_rank = client.zrank(key, "player:eve")
        self.log.output(f"New rank: {new_rank} (moved up after score increase)")
        results.append(new_rank)

        # ── Step 5: Count by score range ──────────────────────
        self.log.section("Step 5: ZCOUNT — Count by Score Range")
        self.log.concept(
            "ZCOUNT returns the count of members with scores in a given range."
        )

        mid_tier = client.zcount(key, 8000, 9000)
        self.log.command(f"ZCOUNT {key} 8000 9000")
        self.log.output(f"Players with scores 8000-9000: {mid_tier}")
        results.append(mid_tier)

        elite = client.zcount(key, 9000, float("inf"))
        self.log.command(f"ZCOUNT {key} 9000 +inf")
        self.log.output(f"Elite players (9000+): {elite}")
        results.append(elite)

        # ── Step 6: Remove a player ────────────────────────────
        self.log.section("Step 6: ZREM — Remove Members")
        self.log.concept(
            "ZREM removes one or more members and returns the count removed."
        )

        removed = client.zrem(key, "player:jack")
        self.log.command(f"ZREM {key} player:jack")
        self.log.output(f"Removed {removed} member(s)")

        exists = client.zscore(key, "player:jack")
        self.log.command(f"ZSCORE {key} player:jack")
        self.log.output(f"Score: {exists} (None = gone)")
        results.extend([removed, exists])

        # ── Summary ─────────────────────────────────────────────
        self.log.separator()
        self.log.success(
            f"Sorted set operations: leaderboard size={results[0]}, "
            f"top player={results[1][0][0]}:{results[1][0][1]}, "
            f"eve rank={results[2]}→{results[6]} after +500, "
            f"mid-tier count={results[7]}, elite={results[8]}"
        )
        return results
