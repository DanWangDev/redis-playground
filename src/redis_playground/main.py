"""CLI entry point for Redis Playground.

Usage:
    python -m redis_playground.main --exercise 01 --local --step
    python -m redis_playground.main --exercise 01 --local --no-step
    python -m redis_playground.main --exercise 01   # real Redis (Docker)

Mirrors flink-playground's Main.java with EXERCISE_REGISTRY and
reflection-based exercise loading.
"""

import argparse
import sys
import importlib

from redis_playground.shared.step_pause import StepPause
from redis_playground.shared.redis_client import create_client
from redis_playground.shared.console import Console


EXERCISE_REGISTRY = {
    "01": ("redis_playground.exercises.ex01_basic_commands", "Ex01BasicCommands"),
    "02": ("redis_playground.exercises.ex02_strings", "Ex02Strings"),
    "03": ("redis_playground.exercises.ex03_hashes", "Ex03Hashes"),
    "04": ("redis_playground.exercises.ex04_lists", "Ex04Lists"),
    "05": ("redis_playground.exercises.ex05_sets", "Ex05Sets"),
    "06": ("redis_playground.exercises.ex06_sorted_sets", "Ex06SortedSets"),
    "07": ("redis_playground.exercises.ex07_pub_sub", "Ex07PubSub"),
    "08": ("redis_playground.exercises.ex08_streams", "Ex08Streams"),
    "09": ("redis_playground.exercises.ex09_transactions", "Ex09Transactions"),
    "10": ("redis_playground.exercises.ex10_pipelining", "Ex10Pipelining"),
    "11": ("redis_playground.exercises.ex11_lua_scripting", "Ex11LuaScripting"),
    "12": ("redis_playground.exercises.ex12_geospatial", "Ex12Geospatial"),
    "13": ("redis_playground.exercises.ex13_bitmaps_hll", "Ex13BitmapsHLL"),
    "14": (
        "redis_playground.exercises.ex14_keyspace_notifications",
        "Ex14KeyspaceNotifications",
    ),
    "15": ("redis_playground.exercises.ex15_persistence", "Ex15Persistence"),
    "16": (
        "redis_playground.exercises.ex16_client_side_caching",
        "Ex16ClientSideCaching",
    ),
    "17": ("redis_playground.exercises.ex17_rate_limiting", "Ex17RateLimiting"),
    "18": ("redis_playground.exercises.ex18_distributed_locks", "Ex18DistributedLocks"),
    "19": ("redis_playground.exercises.ex19_sentinel", "Ex19Sentinel"),
    "20": ("redis_playground.exercises.ex20_cluster", "Ex20Cluster"),
    "21": ("redis_playground.exercises.ex21_sharded_pub_sub", "Ex21ShardedPubSub"),
}

main_log = Console.for_module("main")


def load_exercise(exercise_id: str):
    """Load an exercise class by its numbered ID."""
    if exercise_id not in EXERCISE_REGISTRY:
        available = ", ".join(sorted(EXERCISE_REGISTRY.keys()))
        main_log.error(f"Exercise '{exercise_id}' not found. Available: {available}")
        sys.exit(1)

    module_path, class_name = EXERCISE_REGISTRY[exercise_id]
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


def main():
    parser = argparse.ArgumentParser(
        description="Redis Playground — hands-on Redis learning exercises"
    )
    parser.add_argument(
        "--exercise",
        "-e",
        type=str,
        required=True,
        help="Exercise number (e.g., '01', '02')",
    )
    parser.add_argument(
        "--local",
        "-l",
        action="store_true",
        help="Use fakeredis (in-memory, no Docker needed)",
    )
    parser.add_argument(
        "--step",
        "-s",
        action="store_true",
        help="Enable interactive step-by-step mode",
    )
    parser.add_argument(
        "--no-step",
        action="store_true",
        help="Disable step mode (for automated runs)",
    )
    args = parser.parse_args()

    exercise_id = args.exercise.zfill(2)

    step = StepPause(enabled=args.step and not args.no_step)
    client = create_client(local=args.local)

    exercise_cls = load_exercise(exercise_id)
    runner = exercise_cls()
    runner.set_step_pause(step)

    try:
        results = runner.execute(client)
        main_log.success(
            f"Exercise {exercise_id} completed with {len(results)} result(s)"
        )
    except Exception as e:
        main_log.error(f"Exercise {exercise_id} failed: {e}")
        raise


if __name__ == "__main__":
    main()
