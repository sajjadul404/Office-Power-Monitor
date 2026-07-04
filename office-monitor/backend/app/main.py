"""
The one backend. Both the React dashboard and the Discord bot talk only to
this process -- the dashboard over REST (initial load) + WebSocket (live
updates), the bot over REST only (it doesn't need push updates, it answers
on-demand commands and polls /api/alerts separately for the proactive-post
bonus).

Run with:  uvicorn app.main:app --reload --port 8000
"""

import asyncio
from datetime import datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .state import DeviceStore
from .simulator import SimClock, run_simulator, SIMULATION_SPEED
from .alerts import compute_alerts
from .usage import UsageTracker
from .models import ROOM_LABELS

app = FastAPI(title="Office Device Monitor API")

# Dashboard dev server runs on a different origin (localhost:5173) than the
# API (localhost:8000) -- CORS has to be explicitly opened for that.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten to the real dashboard origin in production
    allow_methods=["*"],
    allow_headers=["*"],
)

store = DeviceStore()
clock = SimClock()
usage = UsageTracker()


class ConnectionManager:
    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        if ws in self.active:
            self.active.remove(ws)

    async def broadcast(self, payload: dict):
        dead = []
        for ws in self.active:
            try:
                await ws.send_json(payload)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws)


manager = ConnectionManager()


def _snapshot(sim_now: datetime) -> dict:
    return {
        "type": "snapshot",
        "sim_time": sim_now.isoformat(timespec="seconds"),
        "devices": store.all_devices(),
        "power_total_w": store.total_power_now(),
        "power_by_room": store.power_by_room(),
        "kwh_today": usage.kwh_today,
        "alerts": compute_alerts(store, sim_now),
    }


async def _on_tick(sim_now: datetime):
    usage.sample(sim_now, store.total_power_now())
    await manager.broadcast(_snapshot(sim_now))


@app.on_event("startup")
async def start_simulator():
    asyncio.create_task(run_simulator(store, clock, _on_tick))


# ---------------------------------------------------------------- REST ----

@app.get("/api/health")
def health():
    return {"status": "ok", "simulation_speed": SIMULATION_SPEED}


@app.get("/api/devices")
def get_devices():
    return {"devices": store.all_devices(), "sim_time": clock.now().isoformat(timespec="seconds")}


@app.get("/api/rooms/{room_id}")
def get_room(room_id: str):
    if room_id not in ROOM_LABELS:
        raise HTTPException(status_code=404, detail=f"Unknown room '{room_id}'. Valid: {list(ROOM_LABELS)}")
    devices = store.devices_in_room(room_id)
    return {
        "room": room_id,
        "room_label": ROOM_LABELS[room_id],
        "devices": devices,
        "power_w": sum(d["rated_watts"] for d in devices if d["status"]),
    }


@app.get("/api/usage")
def get_usage():
    return {
        "power_total_w": store.total_power_now(),
        "power_by_room": store.power_by_room(),
        "kwh_today": usage.kwh_today,
        "sim_time": clock.now().isoformat(timespec="seconds"),
    }


@app.get("/api/alerts")
def get_alerts():
    sim_now = clock.now()
    return {"alerts": compute_alerts(store, sim_now), "sim_time": sim_now.isoformat(timespec="seconds")}


# ------------------------------------------------------------ WEBSOCKET ---

@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # send an immediate snapshot so the dashboard isn't blank until next tick
        await websocket.send_json(_snapshot(clock.now()))
        while True:
            await websocket.receive_text()  # we don't expect client messages; just keep alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)
