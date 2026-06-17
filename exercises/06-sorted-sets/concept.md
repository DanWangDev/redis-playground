# Exercise 06: Sorted Sets

## What You'll Learn

- Add scored members with `ZADD`
- Retrieve by rank with `ZRANGE` and `ZREVRANGE`
- Get rank with `ZRANK` and `ZREVRANK`
- Get score with `ZSCORE`
- Count by score range with `ZCOUNT`
- Increment scores with `ZINCRBY`
- Remove members with `ZREM`

## Why This Matters

Sorted Sets are Redis's most versatile data structure. Each member has a score (a floating-point number), and members are always ordered by score. Use them for leaderboards, priority queues, rate limiting windows, time-series data, and any problem requiring ordered data with fast range queries.

## Core Concepts

### Leaderboard Pattern

```
ZADD game:leaderboard 9500 "alice" 8200 "bob" 10100 "dave"
ZREVRANGE game:leaderboard 0 2 WITHSCORES
# Returns: [("dave", 10100), ("alice", 9500), ("bob", 8200)]
ZRANK game:leaderboard "alice"  → 1 (zero-indexed, second place)
```

### Score Sorting Rules

- Members are ordered by score (low to high)
- Members with the same score are ordered lexicographically
- `ZREVRANGE` reverses the order (high score first)
- Scores are doubles (64-bit floating point)

### Use Cases

| Use Case | Commands |
|----------|----------|
| Game leaderboard | ZADD, ZREVRANGE, ZRANK |
| Priority queue | ZADD score=priority, ZPOPMIN |
| Rate limiting (sliding window) | ZADD + ZREMRANGEBYSCORE for cleanup |
| Time-series (sorted by timestamp) | ZADD score=timestamp, ZRANGEBYSCORE |
| Delayed job queue | ZADD score=execute_at_timestamp |

## What You'll Practice

1. Add players to a leaderboard with ZADD
2. Get top N players with ZREVRANGE
3. Check a player's rank with ZRANK and ZREVRANK
4. Get a player's score with ZSCORE
5. Increment scores with ZINCRBY
6. Count players within a score range with ZCOUNT
7. Remove players with ZREM

## Key Gotchas

- **Equal scores → lexicographic ordering**: Two members with score 100 won't have the same rank — they're ordered alphabetically.
- **ZRANK is zero-indexed**: The highest-ranked member (lowest score) has rank 0.
- **ZADD updates existing members**: Adding a member that already exists updates its score.
- **Large Sorted Sets**: Internal structure is a skip list + hash table. Operations are O(log N).
