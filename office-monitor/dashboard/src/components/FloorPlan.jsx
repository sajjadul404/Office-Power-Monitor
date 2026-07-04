import React from "react";

const ROOM_ORDER = ["drawing", "work1", "work2"];
const ROOM_LABELS = {
  drawing: "Drawing Room",
  work1: "Work Room 1",
  work2: "Work Room 2",
};

// Local (within-room) layout for a room's 2 fans + 3 lights, in a 260x190 box.
const FAN_SLOTS = [
  { x: 75, y: 55 },
  { x: 185, y: 55 },
];
const LIGHT_SLOTS = [
  { x: 55, y: 145 },
  { x: 130, y: 145 },
  { x: 205, y: 145 },
];

function FanIcon({ x, y, on }) {
  return (
    <g transform={`translate(${x}, ${y})`}>
      <circle r="20" fill="none" stroke="var(--border)" strokeWidth="1.5" />
      <g className={on ? "fan-blades spin" : "fan-blades"}>
        {[0, 120, 240].map((deg) => (
          <ellipse
            key={deg}
            cx="0"
            cy="-9"
            rx="5"
            ry="11"
            fill={on ? "var(--accent-on)" : "var(--accent-off)"}
            transform={`rotate(${deg})`}
            opacity={on ? 0.95 : 0.55}
          />
        ))}
        <circle r="3.5" fill={on ? "var(--accent-on)" : "var(--accent-off)"} />
      </g>
    </g>
  );
}

function LightIcon({ x, y, on }) {
  return (
    <g transform={`translate(${x}, ${y})`}>
      {on && <circle r="18" fill="var(--accent-warn)" opacity="0.18" className="light-halo" />}
      <circle
        r="9"
        fill={on ? "var(--accent-warn)" : "var(--panel-alt)"}
        stroke={on ? "var(--accent-warn)" : "var(--border)"}
        strokeWidth="1.5"
      />
    </g>
  );
}

export default function FloorPlan({ devicesByRoom }) {
  return (
    <div className="floorplan-card">
      <div className="card-eyebrow">Office layout — top view</div>
      <svg viewBox="0 0 820 230" className="floorplan-svg" role="img" aria-label="Live office floor plan">
        {ROOM_ORDER.map((room, i) => {
          const devices = devicesByRoom[room] || [];
          const fans = devices.filter((d) => d.type === "fan");
          const lights = devices.filter((d) => d.type === "light");
          const offsetX = i * 273 + 10;
          const roomOn = devices.some((d) => d.status);

          return (
            <g key={room} transform={`translate(${offsetX}, 10)`}>
              <rect
                width="260"
                height="200"
                rx="10"
                fill="var(--panel)"
                stroke={roomOn ? "var(--accent-on)" : "var(--border)"}
                strokeWidth={roomOn ? 1.5 : 1}
              />
              <text x="16" y="24" className="room-label">
                {ROOM_LABELS[room]}
              </text>
              {fans.map((d, idx) => (
                <FanIcon key={d.id} x={FAN_SLOTS[idx].x} y={FAN_SLOTS[idx].y} on={d.status} />
              ))}
              {lights.map((d, idx) => (
                <LightIcon key={d.id} x={LIGHT_SLOTS[idx].x} y={LIGHT_SLOTS[idx].y} on={d.status} />
              ))}
            </g>
          );
        })}
      </svg>
      <div className="floorplan-legend">
        <span><i className="dot dot-on" /> device on</span>
        <span><i className="dot dot-off" /> device off</span>
      </div>
    </div>
  );
}
