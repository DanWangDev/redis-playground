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

Redis Sets are unordered collections of unique strings. They power tagging systems, friend lists, unique visitor tracking, and any problem requiring membership testing or set arithmetic. Operations like `SINTER` (common friends), `SUNION` (all interests), and `SDIFF` (missing tags) are O(N) where N is the smallest set.

## Core Concepts

### Set Arithmetic

```
SADD user:1:tags "redis" "python" "docker"
SADD user:2:tags "redis" "java" "docker"

SINTER user:1:tags user:2:tags  → {"redis", "docker"}  # common tags
SUNION user:1:tags user:2:tags  → {"redis", "python", "docker", "java"}  # all tags
SDIFF user:1:tags user:2:tags   → {"python"}  # tags user:1 has but user:2 doesn't
```

## What You'll Practice

1. Add members to sets with SADD
2. Check membership with SISMEMBER
3. Compute intersections (common elements) between sets
4. Compute unions (all elements) between sets
5. Compute differences (A has but B doesn't)
6. Count members with SCARD and pick random with SRANDMEMBER
7. Remove members with SREM

## Key Gotchas

- **SMEMBERS is O(N)**: On a set with millions of members, use `SSCAN`.
- **No ordering**: Sets are unordered. Need ordering? Use Sorted Sets (Ex06).
- **Duplicates silently dropped**: `SADD set "a" "a"` adds "a" only once.
- **SINTER with empty sets**: Intersection with an empty set always returns empty.
