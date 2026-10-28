#!/usr/bin/env python3
"""time_guard.py — wall-clock budget guard for experiment runs.

Use as a context manager OR as a periodic poll inside training loops. Halts at
80% of budget by default and saves whatever partial results are available, so
the pipeline never silently overshoots a compute red line.

Usage A — context manager:

    from time_guard import TimeGuard

    with TimeGuard(budget_minutes=30, partial_save_path="results/v1/partial.json") as guard:
        for epoch in range(EPOCHS):
            ... train ...
            guard.checkpoint({"epoch": epoch, "loss": loss})  # saved on early exit
            if guard.should_stop():
                print(f"Time guard tripped at epoch {epoch}; halting cleanly.")
                break

Usage B — pilot extrapolation (mandatory at start of every script per RESTRICTS.yaml):

    from time_guard import pilot_estimate

    estimate = pilot_estimate(
        pilot_fn=lambda: run_one_step(small_dataset),  # something that runs ≤5 min
        scaling_factor=len(full_dataset) / len(small_dataset) * num_epochs,
    )
    print(f"TIME_ESTIMATE: full run will take ~{estimate.minutes:.1f} min "
          f"(pilot took {estimate.pilot_seconds:.1f} s, scaling {estimate.scaling}×)")
    if estimate.minutes > BUDGET_PER_RUN_MINUTES:
        sys.exit("Time estimate exceeds budget; downscale before scaling up.")

Usage C — CLI poll (for shell scripts):

    python time_guard.py --start <epoch_seconds> --budget-minutes 30
    # exit code 0 if within 80% budget, 1 if past
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import sys
import time
from pathlib import Path
from typing import Any, Callable, Optional


# ─── Pilot estimate ───────────────────────────────────────────────────────────

@dataclasses.dataclass
class PilotEstimate:
    pilot_seconds: float
    scaling: float
    minutes: float          # estimated full run time, in minutes


def pilot_estimate(pilot_fn: Callable[[], Any], scaling_factor: float) -> PilotEstimate:
    """Run `pilot_fn` once, time it, and extrapolate.

    `scaling_factor` should be the multiplier from the pilot's workload to the
    full workload (e.g. (full_examples × full_epochs) / (pilot_examples × pilot_epochs)).
    """
    if scaling_factor <= 0:
        raise ValueError("scaling_factor must be > 0")
    t0 = time.monotonic()
    pilot_fn()
    pilot_seconds = time.monotonic() - t0
    return PilotEstimate(
        pilot_seconds=pilot_seconds,
        scaling=scaling_factor,
        minutes=(pilot_seconds * scaling_factor) / 60.0,
    )


# ─── TimeGuard context manager ───────────────────────────────────────────────

class TimeGuard:
    """Wall-clock budget guard.

    Trips at `stop_fraction * budget_minutes`. The default 0.8 leaves headroom
    for cleanup/save before any external process kills us.
    """

    def __init__(
        self,
        budget_minutes: float,
        partial_save_path: Optional[str | Path] = None,
        stop_fraction: float = 0.8,
        clock: Callable[[], float] = time.monotonic,
    ):
        if budget_minutes <= 0:
            raise ValueError("budget_minutes must be > 0")
        if not (0 < stop_fraction <= 1):
            raise ValueError("stop_fraction must be in (0, 1]")
        self.budget_seconds = budget_minutes * 60.0
        self.stop_at_seconds = self.budget_seconds * stop_fraction
        self.partial_save_path = Path(partial_save_path) if partial_save_path else None
        self._clock = clock
        self._start: Optional[float] = None
        self._latest_checkpoint: Optional[dict] = None

    def __enter__(self) -> "TimeGuard":
        self._start = self._clock()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        # Always try to save the latest checkpoint, even on exception.
        if self.partial_save_path and self._latest_checkpoint is not None:
            try:
                self.partial_save_path.parent.mkdir(parents=True, exist_ok=True)
                with self.partial_save_path.open("w", encoding="utf-8") as f:
                    json.dump(
                        {
                            "elapsed_seconds": self.elapsed_seconds(),
                            "budget_seconds": self.budget_seconds,
                            "checkpoint": self._latest_checkpoint,
                            "exited_normally": exc_type is None,
                        },
                        f,
                        indent=2,
                        default=str,
                    )
            except OSError as e:
                print(f"  (time_guard: failed to save partial: {e})", file=sys.stderr)

    def elapsed_seconds(self) -> float:
        if self._start is None:
            return 0.0
        return self._clock() - self._start

    def should_stop(self) -> bool:
        return self.elapsed_seconds() >= self.stop_at_seconds

    def remaining_seconds(self) -> float:
        return max(0.0, self.budget_seconds - self.elapsed_seconds())

    def checkpoint(self, state: dict) -> None:
        """Record the latest known-good state. Saved on exit."""
        self._latest_checkpoint = state


# ─── CLI mode ─────────────────────────────────────────────────────────────────

def _cli() -> int:
    parser = argparse.ArgumentParser(description="Poll a wall-clock budget from a shell.")
    parser.add_argument("--start", type=float, required=True,
                        help="start time as POSIX epoch seconds")
    parser.add_argument("--budget-minutes", type=float, required=True)
    parser.add_argument("--stop-fraction", type=float, default=0.8)
    args = parser.parse_args()

    elapsed = time.time() - args.start
    stop_at = args.budget_minutes * 60.0 * args.stop_fraction
    remaining = max(0.0, args.budget_minutes * 60.0 - elapsed)
    print(json.dumps({
        "elapsed_seconds": round(elapsed, 1),
        "budget_seconds": round(args.budget_minutes * 60.0, 1),
        "stop_at_seconds": round(stop_at, 1),
        "remaining_seconds": round(remaining, 1),
        "should_stop": elapsed >= stop_at,
    }))
    return 1 if elapsed >= stop_at else 0


if __name__ == "__main__":
    raise SystemExit(_cli())
