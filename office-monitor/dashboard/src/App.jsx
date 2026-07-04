import React, { useMemo } from "react";
import { useLiveData } from "./api.js";
import FloorPlan from "./components/FloorPlan.jsx";
import DevicePanel from "./components/DevicePanel.jsx";
import PowerMeter from "./components/PowerMeter.jsx";
import AlertsPanel from "./components/AlertsPanel.jsx";

export default function App() {
  const { data, connected } = useLiveData();

  const devicesByRoom = useMemo(() => {
    const grouped = { drawing: [], work1: [], work2: [] };
    (data?.devices || []).forEach((d) => grouped[d.room]?.push(d));
    return grouped;
  }, [data]);

  return (
    <div className="app">
      <header className="app-header">
        <div>
          <div className="app-eyebrow">Office Pulse</div>
          <h1>Live device &amp; power monitor</h1>
        </div>
        <div className="header-right">
          <span className={`status-pill ${connected ? "status-live" : "status-down"}`}>
            <i className="status-dot" /> {connected ? "Live" : "Reconnecting…"}
          </span>
          {data && (
            <span className="sim-clock">
              {new Date(data.sim_time).toLocaleString([], {
                weekday: "short",
                hour: "2-digit",
                minute: "2-digit",
              })}
            </span>
          )}
        </div>
      </header>

      {!data ? (
        <div className="loading-state">Connecting to backend…</div>
      ) : (
        <main className="app-grid">
          <div className="col-main">
            <FloorPlan devicesByRoom={devicesByRoom} />
            <DevicePanel devicesByRoom={devicesByRoom} simTime={data.sim_time} />
          </div>
          <div className="col-side">
            <PowerMeter
              totalW={data.power_total_w}
              byRoom={data.power_by_room}
              kwhToday={data.kwh_today}
            />
            <AlertsPanel alerts={data.alerts} />
          </div>
        </main>
      )}

      <footer className="app-footer">
        Simulated data · office hours 9AM–5PM · clock runs at accelerated demo speed
      </footer>
    </div>
  );
}
