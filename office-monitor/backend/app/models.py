"""
Data model for a single monitored device (fan or light).

Design notes:
- Kept as a plain dict-friendly dataclass (not a DB row) because the whole
  point of this deliverable is "simulated in-memory state" -- swapping this
  for a real ORM model later is a drop-in change, not a rewrite.
- `rated_watts` is the *nameplate* draw when ON. Real current sensing would
  replace this with a measured value; here it doubles as the simulated
  measurement, which is explicitly allowed by the problem statement.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime


@dataclass
class Device:
    id: str                 # e.g. "work1-fan-1"
    name: str                # e.g. "Fan 1"
    type: str                # "fan" | "light"
    room: str                # "drawing" | "work1" | "work2"
    status: bool              # True = ON
    rated_watts: float         # nameplate draw when ON
    last_changed: str          # ISO-8601 timestamp (simulated clock)

    def to_dict(self) -> dict:
        return asdict(self)


ROOM_LABELS = {
    "drawing": "Drawing Room",
    "work1": "Work Room 1",
    "work2": "Work Room 2",
}

# Realistic nameplate wattages, per the problem statement's example values.
FAN_WATTS = 60.0
LIGHT_WATTS = 15.0


def build_initial_devices() -> list[Device]:
    """Construct the fixed 15-device office layout (3 rooms x [2 fans, 3 lights])."""
    devices: list[Device] = []
    now_iso = datetime.now().isoformat(timespec="seconds")

    for room_id in ("drawing", "work1", "work2"):
        for i in range(1, 3):  # 2 fans
            devices.append(
                Device(
                    id=f"{room_id}-fan-{i}",
                    name=f"Fan {i}",
                    type="fan",
                    room=room_id,
                    status=False,
                    rated_watts=FAN_WATTS,
                    last_changed=now_iso,
                )
            )
        for i in range(1, 4):  # 3 lights
            devices.append(
                Device(
                    id=f"{room_id}-light-{i}",
                    name=f"Light {i}",
                    type="light",
                    room=room_id,
                    status=False,
                    rated_watts=LIGHT_WATTS,
                    last_changed=now_iso,
                )
            )
    return devices
