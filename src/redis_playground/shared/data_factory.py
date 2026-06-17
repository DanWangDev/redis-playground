"""Test data factories for Redis exercises.

Mirrors flink-playground's DataSources.java. Provides reusable functions
to seed sample data (users, scores, locations, etc.) into Redis.
"""

import redis

# ── User profiles (for Hash exercises) ──────────────────────────

SAMPLE_USERS = {
    "user:1": {
        "name": "Alice",
        "email": "alice@example.com",
        "age": "28",
        "plan": "pro",
    },
    "user:2": {"name": "Bob", "email": "bob@example.com", "age": "35", "plan": "basic"},
    "user:3": {
        "name": "Carol",
        "email": "carol@example.com",
        "age": "22",
        "plan": "pro",
    },
    "user:4": {
        "name": "Dave",
        "email": "dave@example.com",
        "age": "41",
        "plan": "enterprise",
    },
    "user:5": {"name": "Eve", "email": "eve@example.com", "age": "30", "plan": "basic"},
}


def seed_users(client: redis.Redis) -> list[str]:
    """Seed user profiles as Redis hashes. Returns list of user keys."""
    for uid, data in SAMPLE_USERS.items():
        client.hset(uid, mapping=data)
    return list(SAMPLE_USERS.keys())


# ── Game scores (for Sorted Set / leaderboard exercises) ────────

SAMPLE_SCORES = {
    "player:alice": 9500,
    "player:bob": 8200,
    "player:carol": 7800,
    "player:dave": 10100,
    "player:eve": 6700,
    "player:frank": 8900,
    "player:grace": 7200,
    "player:henry": 9300,
    "player:iris": 8500,
    "player:jack": 6100,
}


def seed_leaderboard(client: redis.Redis) -> str:
    """Seed game scores as a sorted set. Returns the leaderboard key."""
    key = "game:leaderboard"
    client.zadd(key, SAMPLE_SCORES)
    return key


# ── Store locations (for Geospatial exercises) ──────────────────

SAMPLE_LOCATIONS = {
    "store:downtown": (-122.4194, 37.7749),
    "store:mission": (-122.4184, 37.7599),
    "store:soma": (-122.3982, 37.7810),
    "store:marina": (-122.4368, 37.8035),
    "store:castro": (-122.4349, 37.7609),
    "store:sunset": (-122.4946, 37.7558),
    "store:richmond": (-122.4786, 37.7778),
}


def seed_locations(client: redis.Redis) -> str:
    """Seed store locations as geospatial data. Returns the geo key."""
    key = "stores:locations"
    for store, (lon, lat) in SAMPLE_LOCATIONS.items():
        client.geoadd(key, (lon, lat, store))
    return key


# ── Article tags (for Set exercises) ────────────────────────────


def seed_article_tags(client: redis.Redis) -> list[str]:
    """Seed article tags as Redis sets. Returns list of article keys."""
    tags = {
        "article:1:tags": ["redis", "database", "nosql", "caching"],
        "article:2:tags": ["python", "programming", "redis"],
        "article:3:tags": ["database", "sql", "postgresql"],
        "article:4:tags": ["redis", "caching", "performance"],
    }
    for key, tag_list in tags.items():
        client.sadd(key, *tag_list)
    return list(tags.keys())
