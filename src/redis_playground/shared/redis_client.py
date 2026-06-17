"""Shared Redis connection management.

Provides create_client() for both local (fakeredis) and remote (real Redis)
modes. Mirrors the dual-mode pattern from flink-playground's --local flag.
"""

import os
import redis


def create_client(local: bool = False) -> redis.Redis:
    """Create a Redis client.

    Args:
        local: If True, use fakeredis (in-memory, no Docker needed).
               If False, connect to real Redis via environment variables.

    Returns:
        A Redis client instance with decode_responses=True.
    """
    if local:
        import fakeredis

        return fakeredis.FakeRedis(decode_responses=True)

    return redis.Redis(
        host=os.environ.get("REDIS_HOST", "localhost"),
        port=int(os.environ.get("REDIS_PORT", "6379")),
        password=os.environ.get("REDIS_PASSWORD", "playground"),
        decode_responses=True,
    )
