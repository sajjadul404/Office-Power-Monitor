"""
Dependency-free smoke tests for the parts of the backend that don't need
FastAPI running -- state, alerts, and usage math. Run with:

    cd backend && python3 tests/test_logic.py

(Kept as plain asserts + a runner rather than pytest to avoid adding a test
framework dependency just for a hackathon submission -- swap for pytest
happily if the project grows.)
"""

import sys
import os
import asyncio
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.state import DeviceStore
from app.alerts import compute_alerts
from app.usage import UsageTracker
from app.models import ROOM_LABELS


def test_initial_device_count():
    store = DeviceStore()
    devices = store.all_devices()
    assert len(devices) == 15, f"expected 15 devices, got {len(devices)}"
    fans = [d for d in devices if d["type"] == "fan"]
    lights = [d for d in devices if d["type"] == "light"]
    assert len(fans) == 6, f"expected 6 fans, got {len(fans)}"
    assert len(lights) == 9, f"expected 9 lights, got {len(lights)}"
    print("PASS: test_initial_device_count")


def test_all_devices_off_initially():
    store = DeviceStore()
    assert store.total_power_now() == 0.0
    print("PASS: test_all_devices_off_initially")


def test_power_updates_on_status_change():
    async def run():
        store = DeviceStore()
        now = datetime.now()
        await store.set_status("drawing-fan-1", True, now)
        assert store.total_power_now() == 60.0
        await store.set_status("drawing-light-1", True, now)
        assert store.total_power_now() == 75.0
    asyncio.run(run())
    print("PASS: test_power_updates_on_status_change")


def test_after_hours_alert_fires():
    async def run():
        store = DeviceStore()
        off_hours = datetime.now().replace(hour=22, minute=0, second=0, microsecond=0)
        await store.set_status("work1-light-1", True, off_hours)
        alerts = compute_alerts(store, off_hours)
        ids = [a["id"] for a in alerts]
        assert "after-hours:work1-light-1" in ids
    asyncio.run(run())
    print("PASS: test_after_hours_alert_fires")


def test_no_after_hours_alert_during_office_hours():
    async def run():
        store = DeviceStore()
        during_hours = datetime.now().replace(hour=11, minute=0, second=0, microsecond=0)
        await store.set_status("work1-light-1", True, during_hours)
        alerts = compute_alerts(store, during_hours)
        assert not any(a["id"].startswith("after-hours:") for a in alerts)
    asyncio.run(run())
    print("PASS: test_no_after_hours_alert_during_office_hours")


def test_continuous_on_alert_after_2_hours():
    async def run():
        store = DeviceStore()
        t0 = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        room_devices = [d for d in store.all_devices() if d["room"] == "drawing"]
        for d in room_devices:
            await store.set_status(d["id"], True, t0)

        just_under = t0 + timedelta(hours=1, minutes=59)
        alerts_under = compute_alerts(store, just_under)
        assert not any(a["id"] == "continuous:drawing" for a in alerts_under)

        just_over = t0 + timedelta(hours=2, minutes=1)
        alerts_over = compute_alerts(store, just_over)
        assert any(a["id"] == "continuous:drawing" for a in alerts_over)
    asyncio.run(run())
    print("PASS: test_continuous_on_alert_after_2_hours")


def test_continuous_alert_resets_when_one_device_turns_off():
    async def run():
        store = DeviceStore()
        t0 = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        room_devices = [d for d in store.all_devices() if d["room"] == "drawing"]
        for d in room_devices:
            await store.set_status(d["id"], True, t0)

        mid = t0 + timedelta(hours=1)
        await store.set_status(room_devices[0]["id"], False, mid)  # one device drops off

        later = t0 + timedelta(hours=2, minutes=30)
        alerts = compute_alerts(store, later)
        assert not any(a["id"] == "continuous:drawing" for a in alerts), (
            "alert should reset once the room is no longer ALL on"
        )
    asyncio.run(run())
    print("PASS: test_continuous_alert_resets_when_one_device_turns_off")


def test_usage_tracker_integrates_power_over_time():
    tracker = UsageTracker()
    t0 = datetime.now()
    tracker.sample(t0, 1000.0)  # 1000W
    t1 = t0 + timedelta(hours=1)
    tracker.sample(t1, 1000.0)  # still 1000W, 1 hour later
    assert abs(tracker.kwh_today - 1.0) < 0.01, f"expected ~1.0 kWh, got {tracker.kwh_today}"
    print("PASS: test_usage_tracker_integrates_power_over_time")


if __name__ == "__main__":
    test_initial_device_count()
    test_all_devices_off_initially()
    test_power_updates_on_status_change()
    test_after_hours_alert_fires()
    test_no_after_hours_alert_during_office_hours()
    test_continuous_on_alert_after_2_hours()
    test_continuous_alert_resets_when_one_device_turns_off()
    test_usage_tracker_integrates_power_over_time()
    print("\nAll tests passed.")
