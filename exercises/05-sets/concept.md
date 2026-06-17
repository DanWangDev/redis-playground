# Exercise 05: Sets

## What You'll Learn

- Store unique members with `SADD`
- Test membership with `SISMEMBER`
- Remove members with `SREM`
- Set operations: `SINTER` (intersection), `SUNION` (union), `SDIFF` (difference)
- Get all members with `SMEMBERS`
- Count members with `SCARD`
- Get random member with `SRANDMEMBER`

## Why This Matters

Redis Sets are unordered collections of unique strings. They power tagging systems, friend lists, unique visitor tracking, and any problem requiring membership testing or set arithmetic. Operations like `SINTER` (common friends), `SUNION` (all interests), and `SDIFF` (missing tags) are O(N) where N is the smallest set — making them very fast.

## Core Concepts

### Set Arithmetic

```
SADD user:1:tags "redis" "python" "docker"
SADD user:2:tags "redis" "java" "docker"

SINTER user:1:tags user:2:tags  → {"redis", "docker"}  # common tags
SUNION user:1:tags user:2:tags  → {"redis", "python", "docker", "java"}  # all tags
SDIFF user:1:tags user:2:tags   → {"python"}  # tags user:1 has that user:2 doesn't
```

### Use Cases

- **Tagging**: Article tags, product categories, user interests
- **Membership**: "Is user X in the admin set?"
- **Uniqueness**: Track unique IPs, unique daily visitors
- **Random element**: `SRANDMEMBER` for random item selection (A/B testing, raffles)

### Performance

All set operations run in O(N) where N is the cardinality of the smallest set. `SADD`, `SREM`, `SISMEMBER` are O(1).

## What You'll Practice

1. Add members to sets with SADD
2. Check membership with SISMEMBER
3. Compute intersections (common elements) between sets
4. Compute unions (all elements) between sets
5. Compute differences (A has but B doesn't)
6. Count members with SCARD and pick random with SRANDMEMBER

## Key Gotchas

- **SMEMBERS is O(N)**: On a set with millions of members, it returns all of them. Use `SSCAN` for large sets.
- **No ordering**: Sets are unordered. Need ordering? Use Sorted Sets (Exercise 06).
- **Duplicates silently dropped**: `SADD set "a" "a"` adds "a" only once.
- **SINTER with empty sets**: Intersection with an empty set always returns empty.
