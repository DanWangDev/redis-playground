# Exercise 25: RedisTimeSeries

## What You'll Learn
- Create time-series with `TS.CREATE`
- Add data points with `TS.ADD`
- Query ranges with `TS.RANGE`
- Multi-series queries with `TS.MRANGE`
- Aggregation: `TS.RANGE` with `AGGREGATION avg`

## Why This Matters

RedisTimeSeries is the dedicated time-series module in Redis Stack. Unlike sorted sets (which can simulate time-series), RedisTimeSeries provides automatic downsampling, retention policies, and optimized storage — critical for IoT sensors, monitoring dashboards, and financial tick data.

## Core Concepts
- **TS.CREATE**: Defines a time-series key with optional retention period
- **TS.ADD**: Appends a data point (timestamp, value) — auto-sorted by time
- **TS.RANGE**: Queries a range with optional aggregation (avg, min, max, sum, count)

## What You'll Practice
1. Create a time-series with TS.CREATE
2. Add data points with TS.ADD
3. Query a range with TS.RANGE
4. Filter by time with FROM/TO

## Key Gotchas
- Timestamps are Unix epoch in milliseconds
- TS.CREATE with RETENTION auto-deletes old data
- Requires Redis Stack (not plain Redis OSS)
