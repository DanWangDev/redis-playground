"""pytest fixtures for Redis Playground tests.

Provides two layers:
- fake_redis: fakeredis fixture for fast unit tests (no Docker)
- real_redis: real Redis fixture for integration tests (Docker required)

Mirrors flink-playground's MiniClusterTestBase.
"""

import pytest


@pytest.fixture
def fake_redis():
    """Fast in-memory Redis for unit tests — no Docker needed.

    Uses fakeredis which implements the Redis protocol in pure Python.
    The [lua] extra enables Lua scripting support.
    """
    import fakeredis

    server = fakeredis.FakeServer()
    client = fakeredis.FakeRedis(server=server, decode_responses=True)
    yield client
    client.flushall()


@pytest.fixture
def real_redis():
    """Real Redis client for integration tests — requires Docker.

    Set REDIS_HOST, REDIS_PORT, REDIS_PASSWORD env vars or use defaults
    that match the docker-compose.yml configuration.
    """
    import os
    import redis

    client = redis.Redis(
        host=os.environ.get("REDIS_HOST", "localhost"),
        port=int(os.environ.get("REDIS_PORT", "6379")),
        password=os.environ.get("REDIS_PASSWORD", "playground"),
        decode_responses=True,
    )
    yield client
    client.flushdb()
