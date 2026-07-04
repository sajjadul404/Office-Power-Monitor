"""
Turns instantaneous wattage readings into a running "today's estimated kWh"
figure, the way a real smart-meter would (Riemann-sum the power curve).

Kept separate from DeviceStore because it has its own piece of state (a
running total + last-sample time) that isn't really "device state" -- it's
derived/aggregated. Small class, but the separation keeps state.py focused
on one responsibility.
"""

from datetime import datetime


class UsageTracker:
    def __init__(self):
        self._wh_today = 0.0
        self._last_sample_time: datetime | None = None
        self._last_day = None

    def sample(self, sim_now: datetime, watts_now: float) -> None:
        if self._last_day is not None and sim_now.date() != self._last_day:
            self._wh_today = 0.0  # new simulated day -> reset the meter
        self._last_day = sim_now.date()

        if self._last_sample_time is not None:
            hours_elapsed = (sim_now - self._last_sample_time).total_seconds() / 3600
            if hours_elapsed > 0:
                self._wh_today += watts_now * hours_elapsed
        self._last_sample_time = sim_now

    @property
    def kwh_today(self) -> float:
        return round(self._wh_today / 1000, 2)
