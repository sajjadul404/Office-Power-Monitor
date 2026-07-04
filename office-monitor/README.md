# Office Pulse

A live office electrical-monitoring system: a shared FastAPI backend feeds
both a real-time React dashboard and a Discord bot from one source of
truth, over a simulated 15-device office (3 rooms × 2 fans + 3 lights).

Built for the "Lights, Fans, Discord" hackathon problem statement.

## A discrepancy worth flagging

The problem statement says "15 devices total" in the room breakdown but
"18 devices" in several other places, and the floor-plan image's own
summary lists "6 fans + 9 lights = 18" (6+9 is 15, not 18). This project
implements the physically consistent number: **15 devices** (3 rooms ×
[2 fans + 3 lights]). Worth a quick check with the organizers if their
grading script hardcodes 18 anywhere.

## Architecture

```
[Simulated Device Layer] -> [Backend: FastAPI] -> [Web Dashboard (React)]
                                                 -> [Discord Bot]
```

One backend process is the single source of truth. The dashboard subscribes
over WebSocket for live pushes; the bot polls the same REST API on demand
(commands) and every 15s (alert check). Neither client ever talks to the
other — see `diagrams/system-diagram.svg` for the full picture.

| Piece | Stack | Why |
|---|---|---|
| Backend | FastAPI + asyncio | Native async WebSocket support, minimal boilerplate for a hackathon timeline |
| Dashboard | React (Vite) | Component reuse across floor plan / panels; fast dev server |
| Bot | discord.py | Standard, well-documented Discord bot library for Python |
| State | In-memory (Python dict) | Zero setup; documented trade-off in `backend/app/state.py` on what would change for production |

## Repo layout

```
backend/     FastAPI app: device model, simulator, alerts, REST + WebSocket
dashboard/   React (Vite) live dashboard
bot/         discord.py bot (!status, !room, !usage, proactive alerts)
diagrams/    system-diagram.svg + circuit/ (Wokwi files + pin-mapping docs)
preview/     standalone dashboard-preview.html (mock data, no setup needed)
```

## Running it

### 1. Backend

```bash
cd backend
python3 -m venv venv && source venv/bin/activate   # or your preferred env tool
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Check it's alive: `curl http://localhost:8000/api/health`

**Demo speed vs. real time**: `backend/app/simulator.py` has
`SIMULATION_SPEED = 300` (1 real second = 5 simulated minutes), so a full
office day cycles in ~4.8 real minutes and both alert types (after-hours,
continuous-2h) reliably fire during a short demo/video. Set it to `1` for
an actual real-time deployment.

### 2. Dashboard

```bash
cd dashboard
npm install
npm run dev
```

Open the printed localhost URL (default `http://localhost:5173`). It
connects to the backend at `ws://localhost:8000/ws` by default — override
with a `.env` file (`VITE_API_BASE`, `VITE_WS_URL`) if you deploy the
backend elsewhere.

**Don't want to run the backend first?** Open `preview/dashboard-preview.html`
directly in a browser — it's a self-contained mock of the exact same visual
design with fake data, useful for a quick visual check or as a fallback if
the live backend isn't reachable during a demo.

### 3. Discord bot

```bash
cd bot
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env: DISCORD_BOT_TOKEN, BACKEND_URL, optionally ALERT_CHANNEL_ID
python3 bot.py
```

Commands: `!status`, `!room <drawing|work1|work2>`, `!usage`, `!help`.

Set `ALERT_CHANNEL_ID` (right-click a channel in Discord → Copy Channel ID,
with Developer Mode on) to enable proactive alert posts. Set
`ANTHROPIC_API_KEY` to have replies rewritten through an LLM for a warmer
tone — the bot works fine without it using built-in friendly templates.

## Diagrams

- `diagrams/system-diagram.svg` — full data-flow diagram (device layer →
  backend → dashboard + bot → user), hand-drawn SVG per the "no Mermaid"
  requirement.
- `diagrams/circuit/` — Wokwi-importable circuit (`diagram.json` +
  `sketch.ino`) for one representative room, plus a README with pin-mapping
  tables and the electrical reasoning for how this would actually be wired
  with mains-isolating relays and real current sensors.

## Testing / validation approach

- `backend/app/*.py` are pure-Python logic (state, simulator, alerts,
  usage) with no FastAPI dependency at import time, so the simulation and
  alert rules were smoke-tested directly with asyncio before wiring up the
  HTTP layer — see the inline comments in `simulator.py` for the trade-offs
  that testing surfaced (tick granularity vs. the scripted-scenario window).
- Recommended next step before submission: an end-to-end pass with the
  backend, dashboard, and bot all running together, confirming the alert
  that fires on the dashboard also reaches Discord within one poll cycle
  (≤15s).

## Known limitations / honest trade-offs

- State is in-memory and resets on backend restart — fine for a demo,
  documented in `state.py` as the first thing to swap for a real deployment
  (Redis for live state, Postgres for an alerts audit trail).
- The Wokwi circuit simulates the switched load directly with an LED/motor
  rather than including an actual relay part, because I wasn't fully
  confident the relay-module part type would import cleanly — the
  `circuit/README.md` documents the real relay-based wiring in prose/table
  form instead of risking a broken import.
- Per-device current sensing doesn't scale cleanly past a few devices with
  a single microcontroller; `circuit/README.md` discusses the trade-off
  and a couple of more practical alternatives (I/O expanders, per-room
  clamp sensors, or Tasmota smart plugs).
