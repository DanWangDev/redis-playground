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
