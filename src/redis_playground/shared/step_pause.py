"""Interactive step-by-step mode for exercises.

Mirrors flink-playground's StepPause.java. When enabled, pauses between
each step so the learner can read output and press Enter to continue.
"""

import os


class StepPause:
    """Controls interactive step-by-step execution."""

    def __init__(self, enabled: bool = False):
        self.enabled = enabled and not os.environ.get("NO_PAUSE")

    def pause(self, description: str = "") -> None:
        """Pause and wait for Enter if step mode is enabled."""
        if not self.enabled:
            return
        prompt = "  [Enter] to continue"
        if description:
            prompt = f"  {description} — [Enter] to continue"
        input(prompt)

    def enable(self) -> None:
        self.enabled = True

    def disable(self) -> None:
        self.enabled = False
