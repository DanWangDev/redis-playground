"""Exercise 06: Sorted Sets — leaderboards, rankings, score ranges."""

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner
from redis_playground.shared.data_factory import seed_leaderboard


class Ex06SortedSets(ExerciseRunner):
    def __init__(self):
        super().__init__("06-sorted-sets", "Sorted Sets")

    def run(self, client: redis.Redis) -> list:
        results = []

        self.log.section("Step 1: ZADD — Build a Leaderboard")
        self.log.concept(
            "Each member has a score. Members are always ordered by score."
        )
        key = seed_leaderboard(client)
        self.log.command(f"ZADD {key} (10 players)")
        size = client.zcard(key)
        self.log.output(f"Size: {size}")
        results.append(size)

        self.log.section("Step 2: ZREVRANGE — Top Players")
        top3 = client.zrevrange(key, 0, 2, withscores=True)
        self.log.command(f"ZREVRANGE {key} 0 2 WITHSCORES")
        for i, (name, score) in enumerate(top3):
            self.log.output(f"  #{i + 1}: {name} = {score}")
        results.append(top3)

        self.log.section("Step 3: ZRANK — Find Position")
        rank = client.zrank(key, "player:eve")
        rev_rank = client.zrevrank(key, "player:eve")
        score = client.zscore(key, "player:eve")
        self.log.command(f"ZRANK → {rank}, ZREVRANK → {rev_rank}, ZSCORE → {score}")
        results.extend([rank, rev_rank, score])

        self.log.section("Step 4: ZINCRBY — Update Score")
        new_score = client.zincrby(key, 500, "player:eve")
        self.log.command(f"ZINCRBY {key} 500 player:eve → {new_score}")
        new_rank = client.zrank(key, "player:eve")
        results.extend([new_score, new_rank])

        self.log.section("Step 5: ZCOUNT — Count by Score Range")
        mid_tier = client.zcount(key, 8000, 9000)
        elite = client.zcount(key, 9000, float("inf"))
        self.log.command(f"ZCOUNT {key} 8000 9000 → {mid_tier}, 9000 +inf → {elite}")
        results.extend([mid_tier, elite])

        self.log.section("Step 6: ZREM — Remove Member")
        removed = client.zrem(key, "player:jack")
        exists = client.zscore(key, "player:jack")
        self.log.command(f"ZREM {key} player:jack → removed={removed}, score={exists}")
        results.extend([removed, exists])

        self.log.separator()
        self.log.success(
            f"Sorted set ops: size={results[0]}, top={results[1][0][0]}, eve={results[4]}→{results[5]}"
        )
        return results
