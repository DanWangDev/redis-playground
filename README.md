# Redis Playground

[中文版本](README.zh-CN.md) | [English](README.md)

Hands-on Redis learning playground with 26 progressive exercises. Each exercise includes a runnable Python class, unit tests, and bilingual concept documentation (English + Chinese).

## Quick Start

```bash
# Install dependencies
pip install -e ".[dev]"

# Run an exercise (fakeredis — no Docker needed)
python -m redis_playground.main --exercise 01 --local

# Interactive step-by-step mode
python -m redis_playground.main --exercise 01 --local --step

# With real Redis (Docker)
docker compose up -d --wait
python -m redis_playground.main --exercise 01
```

Open RedisInsight at http://localhost:8001 to explore data visually.

## Tech Stack

![Python](https://img.shields.io/badge/Python_3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![Redis](https://img.shields.io/badge/Redis_Stack-FF4438?style=flat-square&logo=redis&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)
![Ruff](https://img.shields.io/badge/Ruff-FCC21B?style=flat-square&logo=ruff&logoColor=black)

Dual-mode execution via [fakeredis](https://github.com/cunla/fakeredis-py) (in-memory, no Docker) or real Redis Stack. Terminal UI with [Rich](https://github.com/Textualize/rich). Bilingual concept docs in English and 中文. 26 exercises with unit and integration tests.

## Exercise Map

| # | Topic | What You'll Learn |
|---|-------|-------------------|
| 01 | Basic Commands | PING, SET, GET, DEL, EXISTS, EXPIRE, TTL, KEYS, TYPE |
| 02 | Strings | INCR/DECR, MSET/MGET, GETRANGE/SETRANGE, SETNX, APPEND |
| 03 | Hashes | HSET/HGET/HGETALL, HINCRBY, HDEL, HEXISTS, HKEYS/HVALS |
| 04 | Lists | LPUSH/RPOP (queue), LPUSH/LPOP (stack), LRANGE, LTRIM |
| 05 | Sets | SADD, SINTER/SUNION/SDIFF, SISMEMBER, SCARD |
| 06 | Sorted Sets | ZADD, ZRANGE/ZREVRANGE, ZRANK, ZSCORE, ZINCRBY |
| 07 | Pub/Sub | PUBLISH, SUBSCRIBE, PSUBSCRIBE, fire-and-forget semantics |
| 08 | Streams | XADD, XREAD, XGROUP, XREADGROUP, XACK, XPENDING |
| 09 | Transactions | MULTI/EXEC, DISCARD, WATCH (optimistic locking) |
| 10 | Pipelining | pipeline(), RTT reduction, non-atomic interleaving |
| 11 | Lua Scripting | EVAL, EVALSHA, SCRIPT LOAD, atomic server-side scripts |
| 12 | Geospatial | GEOADD, GEORADIUS, GEODIST, location-based queries |
| 13 | Bitmaps & HLL | SETBIT, BITCOUNT, PFADD, probabilistic counting |
| 14 | Keyspace Notifications | notify-keyspace-events, PSUBSCRIBE `__keyspace@*` |
| 15 | Persistence | RDB snapshots, AOF, BGSAVE, durability trade-offs |
| 16 | Client-Side Caching | CLIENT TRACKING, RESP3 push, cache invalidation |
| 17 | Rate Limiting | Token bucket, sliding window, fixed window patterns |
| 18 | Distributed Locks | SET NX PX, Redlock algorithm, fencing tokens |
| 19 | Sentinel | Sentinel monitoring, automatic failover, master election |
| 20 | Cluster | Hash slots, MOVED/ASK redirect, resharding |
| 21 | Sharded Pub/Sub | SSUBSCRIBE, SPUBLISH, sharded channel distribution |
| 22 | SCAN | SCAN, HSCAN, SSCAN, ZSCAN — cursor-based iteration |
| 23 | RedisJSON | JSON.SET, JSON.GET, JSON.NUMINCRBY, JSON.ARRAPPEND |
| 24 | RediSearch | FT.CREATE, FT.SEARCH — full-text search with filters |
| 25 | RedisTimeSeries | TS.CREATE, TS.ADD, TS.RANGE with aggregation |
| 26 | FUNCTION | FUNCTION LOAD, FCALL — durable Redis 7 server-side functions |

## CLI Reference

```
python -m redis_playground.main --exercise NN [--local] [--step|--no-step]
```

| Flag | Description |
|------|-------------|
| `--exercise NN` | Exercise number (01–26) |
| `--local` | Use fakeredis (in-memory, no Docker) |
| `--step` | Interactive step-by-step mode |
| `--no-step` | Run without pauses (CI/automation) |

## Development

```bash
make install-dev    # Install with dev dependencies
make test           # Run unit tests (fakeredis)
make lint           # Ruff check
make fmt            # Ruff format
```

## Architecture

```
redis-playground/
├── exercises/                  # Bilingual concept docs per module
│   └── NN-topic/
│       ├── concept.md          # English
│       └── concept_cn.md       # 中文
├── src/redis_playground/
│   ├── main.py                 # CLI entry point
│   ├── shared/                 # ExerciseRunner ABC, console, fixtures
│   └── exercises/              # One class per exercise (ExNN...)
└── tests/
    ├── conftest.py              # fakeredis fixture
    ├── helpers/assertions.py    # Redis assertion helpers
    └── exercises/              # One test file per exercise
```

## Key Gotchas Summary

- **KEYS is O(N)**: Synchronous full keyspace scan — never in production. Use `SCAN`.
- **TTL returns -1 vs -2**: `-1` means persistent (no expiry set). `-2` means key doesn't exist.
- **Pub/Sub is fire-and-forget**: Messages published before subscription are lost. Use Streams for persistence.
- **MULTI/EXEC has no rollback**: If one command fails, others still execute.
- **Pipelining is NOT atomic**: Other clients' commands can interleave. Use MULTI/EXEC or Lua for atomicity.
