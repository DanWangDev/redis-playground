# Exercise 13: Bitmaps & HyperLogLog

## What You'll Learn
- Set/get individual bits with `SETBIT` / `GETBIT`
- Count set bits with `BITCOUNT`
- Perform bitwise operations with `BITOP`
- Estimate unique counts with `PFADD` / `PFCOUNT`
- Merge HyperLogLog structures with `PFMERGE`

## Why This Matters
Bitmaps provide compact boolean storage — track 1 million daily active users in 125KB. HyperLogLog provides probabilistic unique counting with ~0.81% error using only 12KB per key, regardless of cardinality. Together they power analytics dashboards, A/B test tracking, and unique visitor counting.

## Core Concepts
- **Bitmap**: Each bit represents a boolean (e.g., "user logged in on day N")
- **BITCOUNT**: O(N) byte scan — efficient for small ranges
- **HyperLogLog**: Probabilistic counter, ~0.81% standard error, 12KB fixed size
- **PFMERGE**: Combine multiple HLL counters without data loss

## Key Gotchas
- HLL is probabilistic — PFCOUNT has ~0.81% error, not exact.
- BITCOUNT is O(N) — use sub-ranges for incremental counting on large bitmaps.
- You can't retrieve individual HLL elements — it's a counter, not a set.
