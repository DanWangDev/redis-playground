"""Redis-specific assertion helpers.

Mirrors flink-playground's StreamAssertions.java — convenience wrappers
around Redis commands for clear, readable test assertions.
"""

import redis


def assert_key_exists(client: redis.Redis, key: str) -> None:
    """Assert that a key exists in Redis."""
    assert client.exists(key), f"Key '{key}' should exist but does not"


def assert_key_not_exists(client: redis.Redis, key: str) -> None:
    """Assert that a key does not exist in Redis."""
    assert not client.exists(key), f"Key '{key}' should not exist but does"


def assert_ttl_in_range(
    client: redis.Redis, key: str, min_seconds: int, max_seconds: int
) -> None:
    """Assert that a key's TTL is within the given range."""
    ttl = client.ttl(key)
    assert min_seconds <= ttl <= max_seconds, (
        f"Key '{key}' TTL ({ttl}) not in range [{min_seconds}, {max_seconds}]"
    )


def assert_ttl_positive(client: redis.Redis, key: str) -> None:
    """Assert that a key has a positive TTL (has an expiry set)."""
    ttl = client.ttl(key)
    assert ttl > 0, f"Key '{key}' should have positive TTL but got {ttl}"


def assert_type(client: redis.Redis, key: str, expected_type: str) -> None:
    """Assert that a key is of the expected Redis type."""
    actual = client.type(key)
    assert actual == expected_type, (
        f"Key '{key}' type should be '{expected_type}' but is '{actual}'"
    )


def assert_value_equal(client: redis.Redis, key: str, expected: str) -> None:
    """Assert that a string key has the expected value."""
    actual = client.get(key)
    assert actual == expected, (
        f"Key '{key}' value should be '{expected}' but is '{actual}'"
    )


def assert_hash_field(client: redis.Redis, key: str, field: str, expected: str) -> None:
    """Assert that a hash field has the expected value."""
    actual = client.hget(key, field)
    assert actual == expected, (
        f"Hash '{key}' field '{field}' should be '{expected}' but is '{actual}'"
    )


def assert_list_length(client: redis.Redis, key: str, expected: int) -> None:
    """Assert that a list has the expected length."""
    actual = client.llen(key)
    assert actual == expected, (
        f"List '{key}' length should be {expected} but is {actual}"
    )


def assert_set_member(client: redis.Redis, key: str, member: str) -> None:
    """Assert that a member exists in a set."""
    assert client.sismember(key, member), f"Set '{key}' should contain '{member}'"


def assert_set_size(client: redis.Redis, key: str, expected: int) -> None:
    """Assert that a set has the expected cardinality."""
    actual = client.scard(key)
    assert actual == expected, (
        f"Set '{key}' cardinality should be {expected} but is {actual}"
    )


def assert_sorted_set_rank(
    client: redis.Redis, key: str, member: str, expected_rank: int
) -> None:
    """Assert that a member has the expected rank in a sorted set (0-indexed)."""
    actual = client.zrank(key, member)
    assert actual == expected_rank, (
        f"Sorted set '{key}' member '{member}' rank should be {expected_rank} but is {actual}"
    )


def assert_sorted_set_score(
    client: redis.Redis, key: str, member: str, expected_score: float
) -> None:
    """Assert that a member has the expected score in a sorted set."""
    actual = client.zscore(key, member)
    assert actual == expected_score, (
        f"Sorted set '{key}' member '{member}' score should be {expected_score} but is {actual}"
    )
