"""
Single source of truth for device state.

Both the WebSocket broadcaster (dashboard) and the REST endpoints (bot +
dashboard initial load) read from this one object. This is the literal
implementation of the spec's architecture requirement:

    [Simulated Device Layer] -> [Backend API] -> [Web UI] && [Discord Bot]

Trade-off: this is a process-local in-memory store, not Redis/Postgres.
That's the right call for a hackathon demo (zero setup, trivially fast),
but it means state resets on restart and won't scale past one backend
process. If this were going to production, swap DeviceStore's internals
for a Redis hash (state) + Postgres (history/alerts audit trail) without
touching main.py's routes.
"""

import asyncio
from datetime import datetime, timedelta

from .models import Device, build_initial_devices, ROOM_LABELS


class DeviceStore:
    def __init__(self):
        self._devices: dict[str, Device] = {
            d.id: d for d in build_initial_devices()
        }
        # Tracks the timestamp a room's devices most recently became "all ON"
        # continuously, used for the >2h-continuous-on alert.
        self._room_all_on_since: dict[str, datetime | None] = {
            r: None for r in ROOM_LABELS
        }
        self._lock = asyncio.Lock()

    # ---- reads (no lock needed for dict snapshots in asyncio single-thread) ----

    def all_devices(self) -> list[dict]:
        return [d.to_dict() for d in self._devices.values()]

    def devices_in_room(self, room: str) -> list[dict]:
        return [d.to_dict() for d in self._devices.values() if d.room == room]

    def get(self, device_id: str) -> Device | None:
        return self._devices.get(device_id)

    def total_power_now(self) -> float:
        return sum(d.rated_watts for d in self._devices.values() if d.status)

    def power_by_room(self) -> dict[str, float]:
        totals = {r: 0.0 for r in ROOM_LABELS}
        for d in self._devices.values():
            if d.status:
                totals[d.room] += d.rated_watts
        return totals

    def room_all_on_since(self, room: str) -> datetime | None:
        return self._room_all_on_since.get(room)

    # ---- writes ----

    async def set_status(self, device_id: str, status: bool, at: datetime) -> Device:
        async with self._lock:
            d = self._devices[device_id]
            if d.status != status:
                d.status = status
                d.last_changed = at.isoformat(timespec="seconds")
            self._recompute_room_all_on(at)
            return d

    def _recompute_room_all_on(self, at: datetime) -> None:
        """Track, per room, how long every device in it has been ON back-to-back."""
        by_room: dict[str, list[Device]] = {r: [] for r in ROOM_LABELS}
        for d in self._devices.values():
            by_room[d.room].append(d)

        for room, devs in by_room.items():
            all_on = all(d.status for d in devs) and len(devs) > 0
            if all_on and self._room_all_on_since[room] is None:
                self._room_all_on_since[room] = at
            elif not all_on:
                self._room_all_on_since[room] = None
