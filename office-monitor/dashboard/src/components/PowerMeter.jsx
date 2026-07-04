import React from "react";

const ROOM_LABELS = {
  drawing: "Drawing Room",
  work1: "Work Room 1",
  work2: "Work Room 2",
};

export default function PowerMeter({ totalW, byRoom, kwhToday }) {
  const maxRoom = Math.max(1, ...Object.values(byRoom));

  return (
    <div className="panel">
      <div className="panel-header">
        <h2>Power consumption</h2>
      </div>

      <div className="power-total">
        <span className="power-total-value">{totalW.toFixed(0)}</span>
        <span className="power-total-unit">W right now</span>
      </div>
      <div className="power-kwh">Est. usage today: <strong>{kwhToday} kWh</strong></div>

      <div className="power-bars">
        {Object.entries(ROOM_LABELS).map(([id, label]) => {
          const value = byRoom[id] || 0;
          const pct = Math.round((value / maxRoom) * 100);
          return (
            <div key={id} className="power-bar-row">
              <span className="power-bar-label">{label}</span>
              <div className="power-bar-track">
                <div className="power-bar-fill" style={{ width: `${pct}%` }} />
              </div>
              <span className="power-bar-value">{value.toFixed(0)}W</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
