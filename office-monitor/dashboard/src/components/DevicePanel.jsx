import React, { useState } from "react";

const ROOM_LABELS = {
  drawing: "Drawing Room",
  work1: "Work Room 1",
  work2: "Work Room 2",
};

function timeAgo(iso, simNowIso) {
  const then = new Date(iso).getTime();
  const now = new Date(simNowIso).getTime();
  const diffMin = Math.round((now - then) / 60000);
  if (diffMin < 1) return "just now";
  if (diffMin < 60) return `${diffMin}m ago`;
  const hrs = Math.round(diffMin / 60);
  return `${hrs}h ago`;
}

export default function DevicePanel({ devicesByRoom, simTime }) {
  const [filter, setFilter] = useState("all");
  const rooms = filter === "all" ? Object.keys(ROOM_LABELS) : [filter];

  return (
    <div className="panel">
      <div className="panel-header">
        <h2>Live device status</h2>
        <div className="chip-row" role="tablist" aria-label="Filter by room">
          <button
            className={`chip ${filter === "all" ? "chip-active" : ""}`}
            onClick={() => setFilter("all")}
          >
            All rooms
          </button>
          {Object.entries(ROOM_LABELS).map(([id, label]) => (
            <button
              key={id}
              className={`chip ${filter === id ? "chip-active" : ""}`}
              onClick={() => setFilter(id)}
            >
              {label}
            </button>
          ))}
        </div>
      </div>

      {rooms.map((room) => (
        <div key={room} className="room-group">
          <div className="room-group-title">{ROOM_LABELS[room]}</div>
          <div className="device-grid">
            {(devicesByRoom[room] || []).map((d) => (
              <div key={d.id} className={`device-chip ${d.status ? "device-on" : ""}`}>
                <span className={`dot ${d.status ? "dot-on" : "dot-off"}`} />
                <span className="device-name">
                  {d.type === "fan" ? "Fan" : "Light"} {d.name.split(" ")[1]}
                </span>
                <span className="device-meta">
                  {d.status ? `${d.rated_watts}W` : "off"} · {timeAgo(d.last_changed, simTime)}
                </span>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
