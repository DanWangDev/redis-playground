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

Sorted Sets are Redis's most versatile data structure. Each member has a score (floating-point), and members are always ordered by score. Use them for leaderboards, priority queues, rate limiting windows, time-series data, and any problem requiring ordered data with fast range queries.

## Core Concepts

### Leaderboard Pattern

```
ZADD game:leaderboard 9500 "alice" 8200 "bob" 10100 "dave"
ZREVRANGE game:leaderboard 0 2 WITHSCORES
ZRANK game:leaderboard "alice"  → 1 (zero-indexed, second place)
```

## What You'll Practice

1. Create a leaderboard with ZADD
2. Get top N players with ZREVRANGE
3. Find player rank with ZRANK / ZREVRANK
4. Check a player's score with ZSCORE
5. Update scores with ZINCRBY
6. Count players in a score range with ZCOUNT
7. Remove players with ZREM

## Key Gotchas

- **Equal scores → lexicographic ordering**: Ties broken alphabetically.
- **ZRANK is zero-indexed**: Lowest score = rank 0.
- **ZADD updates existing**: Adding existing member updates its score.
