"""Abstract base class for all Redis exercises.

Mirrors flink-playground's ExerciseRunner.java. Each exercise extends this,
implements run(client) -> list, and is registered in main.py's EXERCISE_REGISTRY.
"""

from abc import ABC, abstractmethod
from typing import Any

import redis

from .console import Console
from .step_pause import StepPause


class ExerciseRunner(ABC):
    """Base class for all exercises.

    Subclasses implement run(client) which returns a list of collected
    results. This list is used by tests for deterministic assertions
    (mirrors flink-playground's CollectingSink pattern).
    """

    def __init__(self, exercise_id: str, title: str):
        self.exercise_id = exercise_id
        self.title = title
        self.log = Console.for_module(exercise_id)
        self.step_pause = StepPause(enabled=False)

    def set_step_pause(self, step: StepPause) -> None:
        self.step_pause = step

    @abstractmethod
    def run(self, client: redis.Redis) -> list[Any]:
        """Execute the exercise.

        Args:
            client: A Redis client (real or fakeredis).

        Returns:
            A list of collected results for test assertions.
            Each step's output is appended to this list.
        """
        ...

    def execute(self, client: redis.Redis) -> list[Any]:
        """Run the exercise with header/summary logging.

        Args:
            client: A Redis client (real or fakeredis).

        Returns:
            The list of collected results from run().
        """
        self.log.header(f"Exercise {self.exercise_id}: {self.title}")
        client.flushdb()
        results = self.run(client)
        self.log.summary(f"Exercise {self.exercise_id} completed — {len(results)} results")
        return results
