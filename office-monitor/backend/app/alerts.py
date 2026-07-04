"""
Computes the "Active Alerts" the dashboard and bot both need. Pure function
over current store state + sim time -- no hidden state here, which makes it
trivial to unit test (see backend/tests).

Each alert has a stable `id` so callers (the Discord proactive-poster) can
diff against the previous tick and only announce *new* alerts, not repeat
the same one every poll.
"""

from datetime import datetime, timedelta

from .state import DeviceStore
from .models import ROOM_LABELS

CONTINUOUS_ON_THRESHOLD = timedelta(hours=2)
OFFICE_START_HOUR = 9
OFFICE_END_HOUR = 17


def compute_alerts(store: DeviceStore, sim_now: datetime) -> list[dict]:
    alerts: list[dict] = []
    office_hours = OFFICE_START_HOUR <= sim_now.hour < OFFICE_END_HOUR

    if not office_hours:
        for d in store.all_devices():
            if d["status"]:
                alerts.append(
                    {
                        "id": f"after-hours:{d['id']}",
                        "severity": "warning",
                        "room": d["room"],
                        "room_label": ROOM_LABELS[d["room"]],
                        "message": (
                            f"{d['name']} in {ROOM_LABELS[d['room']]} is ON "
                            f"outside office hours (9AM-5PM)."
                        ),
                        "timestamp": sim_now.isoformat(timespec="seconds"),
                    }
                )

    for room in ROOM_LABELS:
        since = store.room_all_on_since(room)
        if since is not None and (sim_now - since) >= CONTINUOUS_ON_THRESHOLD:
            alerts.append(
                {
                    "id": f"continuous:{room}",
                    "severity": "critical",
                    "room": room,
                    "room_label": ROOM_LABELS[room],
                    "message": (
                        f"All devices in {ROOM_LABELS[room]} have been ON "
                        f"continuously for over 2 hours (since "
                        f"{since.strftime('%I:%M %p')})."
                    ),
                    "timestamp": sim_now.isoformat(timespec="seconds"),
                }
            )

    return alerts
