"""
Drives fake-but-plausible device activity so the dashboard/bot always have
something live to show, without any real hardware.

Two things worth calling out (trade-off, documented rather than hidden):

1. SIMULATION_SPEED (see .env / config below): the "clock" used for
   office-hours / continuous-on logic can run faster than real time. At
   speed=1 it's real wall-clock time, which is correct for an actual
   deployment but means alert conditions could take hours to occur --
   useless for a live demo or video. At speed=300 (default), 1 real second
   = 5 simulated minutes, so a full day cycles in ~4.8 real minutes and
   both alert types (after-hours, continuous-2h) reliably fire during a
   short demo. Flip SIMULATION_SPEED=1 in .env for a real deployment.

2. The "Work Room 2 left on" scenario is intentionally scripted (not pure
   random noise) so it reproduces the exact situation the problem
   statement's bonus example describes -- this makes the proactive Discord
   alert demonstrable on demand instead of hoping randomness cooperates
   during a recording.
"""

import asyncio
import random
from datetime import datetime, timedelta

from .state import DeviceStore
from .models import ROOM_LABELS

REAL_TICK_SECONDS = 2          # how often the simulator steps, in real seconds
SIMULATION_SPEED = 300         # simulated seconds per real second (300 = 5 sim-min/tick... see below)
OFFICE_START_HOUR = 9
OFFICE_END_HOUR = 17

# The room used for the "forgot to turn it off" demo scenario.
SCRIPTED_FORGOTTEN_ROOM = "work2"


class SimClock:
    """Wall-clock time scaled by SIMULATION_SPEED, starting at a fixed sim time."""

    def __init__(self, speed: int = SIMULATION_SPEED, start_hour: int = 8):
        self._speed = speed
        self._real_start = datetime.now()
        today = datetime.now().replace(
            hour=start_hour, minute=0, second=0, microsecond=0
        )
        self._sim_start = today

    def now(self) -> datetime:
        elapsed_real = (datetime.now() - self._real_start).total_seconds()
        return self._sim_start + timedelta(seconds=elapsed_real * self._speed)

    @property
    def speed(self) -> int:
        return self._speed


def _is_office_hours(sim_time: datetime) -> bool:
    return OFFICE_START_HOUR <= sim_time.hour < OFFICE_END_HOUR


async def run_simulator(store: DeviceStore, clock: SimClock, on_tick):
    """
    Background task: mutates `store` forever, calling `on_tick()` (async)
    after every step so the caller can broadcast the new snapshot.
    """
    forgotten_triggered_for_day = None  # tracks sim date already scripted today

    while True:
        sim_now = clock.now()
        office_hours = _is_office_hours(sim_now)

        for device in list(store._devices.values()):  # snapshot iteration
            # --- scripted scenario: Work Room 2 "forgot to switch off" ---
            if device.room == SCRIPTED_FORGOTTEN_ROOM:
                just_closed = sim_now.hour == OFFICE_END_HOUR and sim_now.minute < 20
                if just_closed and forgotten_triggered_for_day != sim_now.date():
                    await store.set_status(device.id, True, sim_now)
                    continue
                if not office_hours and sim_now.hour >= OFFICE_END_HOUR:
                    # stays on deliberately until next office-hours window
                    continue

            # --- normal random-walk behaviour for everything else ---
            target_on_probability = 0.55 if office_hours else 0.03
            transition_chance = 0.18  # how "twitchy" the simulation is per tick
            if random.random() < transition_chance:
                new_status = random.random() < target_on_probability
                if new_status != device.status:
                    await store.set_status(device.id, new_status, sim_now)

        if sim_now.hour == OFFICE_END_HOUR and sim_now.minute < 20:
            forgotten_triggered_for_day = sim_now.date()
        if office_hours:
            forgotten_triggered_for_day = None  # re-arm for the next evening

        await on_tick(sim_now)
        await asyncio.sleep(REAL_TICK_SECONDS)
