import React from "react";

export default function AlertsPanel({ alerts }) {
  return (
    <div className="panel">
      <div className="panel-header">
        <h2>Active alerts</h2>
        {alerts.length > 0 && <span className="alert-count">{alerts.length}</span>}
      </div>

      {alerts.length === 0 ? (
        <div className="alerts-empty">No anomalies right now — everything checks out.</div>
      ) : (
        <ul className="alerts-list">
          {alerts.map((a) => (
            <li key={a.id} className={`alert-item alert-${a.severity}`}>
              <div className="alert-message">{a.message}</div>
              <div className="alert-timestamp">
                {new Date(a.timestamp).toLocaleString([], {
                  hour: "2-digit",
                  minute: "2-digit",
                  month: "short",
                  day: "numeric",
                })}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
