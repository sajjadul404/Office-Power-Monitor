"""
Discord bot -- the boss's "quick-access remote control" for the office.

Talks ONLY to the backend's REST API (never touches the simulator directly),
which is what guarantees it always reflects the same reality as the web
dashboard: same source of truth, two read-only clients.

Run with:  python bot.py
Requires .env (see .env.example) with:
  DISCORD_BOT_TOKEN=...
  BACKEND_URL=http://localhost:8000
  ALERT_CHANNEL_ID=123456789012345678   (optional, enables proactive alerts)
  ANTHROPIC_API_KEY=...                  (optional, enables LLM-humanized replies)
"""

import asyncio
import os

import discord
from discord.ext import commands, tasks
import httpx
from dotenv import load_dotenv

from responder import (
    ROOM_LABELS,
    template_status,
    template_room,
    template_usage,
    template_alert,
    humanize,
)

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
ALERT_CHANNEL_ID = os.getenv("ALERT_CHANNEL_ID")
ALERT_POLL_SECONDS = 15

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

http_client = httpx.AsyncClient(base_url=BACKEND_URL, timeout=5.0)
_seen_alert_ids: set[str] = set()


async def fetch(path: str) -> dict | None:
    try:
        r = await http_client.get(path)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[bot] backend request failed ({path}): {e}")
        return None


@bot.event
async def on_ready():
    print(f"[bot] logged in as {bot.user}")
    if ALERT_CHANNEL_ID:
        alert_poller.start()
    else:
        print("[bot] ALERT_CHANNEL_ID not set -- proactive alerts disabled.")


@bot.command(name="status")
async def status_cmd(ctx):
    data = await fetch("/api/devices")
    if not data:
        await ctx.send("Couldn't reach the office backend just now — try again in a moment.")
        return
    msg = template_status(data["devices"])
    await ctx.send(humanize(msg, context="This is a !status summary for the whole office."))


@bot.command(name="room")
async def room_cmd(ctx, room_id: str = None):
    if room_id is None or room_id.lower() not in ROOM_LABELS:
        await ctx.send(f"Usage: `!room <name>` — valid names: {', '.join(ROOM_LABELS)}")
        return
    room_id = room_id.lower()
    data = await fetch(f"/api/rooms/{room_id}")
    if not data:
        await ctx.send("Couldn't reach the office backend just now — try again in a moment.")
        return
    msg = template_room(room_id, ROOM_LABELS[room_id], data["devices"])
    await ctx.send(humanize(msg, context=f"This is a !room {room_id} status check."))


@bot.command(name="usage")
async def usage_cmd(ctx):
    data = await fetch("/api/usage")
    if not data:
        await ctx.send("Couldn't reach the office backend just now — try again in a moment.")
        return
    msg = template_usage(data["power_total_w"], data["kwh_today"])
    await ctx.send(humanize(msg, context="This is a !usage power summary."))


@bot.command(name="help")
async def help_cmd(ctx):
    await ctx.send(
        "**Office Pulse bot commands**\n"
        "`!status` — quick summary of every room\n"
        "`!room <drawing|work1|work2>` — status of one room\n"
        "`!usage` — current power draw + today's estimated kWh"
    )


@tasks.loop(seconds=ALERT_POLL_SECONDS)
async def alert_poller():
    """Bonus: proactively posts NEW alerts to a designated channel."""
    data = await fetch("/api/alerts")
    if not data:
        return
    channel = bot.get_channel(int(ALERT_CHANNEL_ID))
    if channel is None:
        return

    current_ids = {a["id"] for a in data["alerts"]}
    for alert in data["alerts"]:
        if alert["id"] not in _seen_alert_ids:
            _seen_alert_ids.add(alert["id"])
            await channel.send(humanize(template_alert(alert), context="Proactive alert."))

    # Alerts that cleared can fire again later (e.g. it happens the next
    # evening too) -- drop resolved ones instead of remembering forever.
    _seen_alert_ids.intersection_update(current_ids)


if __name__ == "__main__":
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        raise SystemExit("DISCORD_BOT_TOKEN is not set. Copy .env.example to .env and fill it in.")
    bot.run(token)
