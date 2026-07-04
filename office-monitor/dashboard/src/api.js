import { useEffect, useRef, useState } from "react";

// Override with VITE_API_BASE / VITE_WS_URL env vars for non-local deployments.
export const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";
const WS_URL = import.meta.env.VITE_WS_URL || "ws://localhost:8000/ws";

/**
 * Subscribes to the backend's single WebSocket feed. This is the *only*
 * data source the dashboard needs for live updates -- the whole panel,
 * power meter, and alerts all update from one snapshot message, which is
 * what keeps them guaranteed-in-sync with each other and with the bot
 * (which reads the same backend over REST).
 *
 * Reconnects with backoff if the backend restarts or the connection drops,
 * since a hackathon demo backend restarting mid-demo shouldn't require a
 * manual page refresh to recover.
 */
export function useLiveData() {
  const [data, setData] = useState(null);
  const [connected, setConnected] = useState(false);
  const retryDelay = useRef(1000);

  useEffect(() => {
    let ws;
    let cancelled = false;
    let reconnectTimer;

    function connect() {
      ws = new WebSocket(WS_URL);

      ws.onopen = () => {
        if (cancelled) return;
        setConnected(true);
        retryDelay.current = 1000;
      };

      ws.onmessage = (event) => {
        if (cancelled) return;
        try {
          const payload = JSON.parse(event.data);
          setData(payload);
        } catch (err) {
          console.error("Bad WS payload", err);
        }
      };

      ws.onclose = () => {
        if (cancelled) return;
        setConnected(false);
        reconnectTimer = setTimeout(connect, retryDelay.current);
        retryDelay.current = Math.min(retryDelay.current * 1.5, 10000);
      };

      ws.onerror = () => ws.close();
    }

    connect();

    return () => {
      cancelled = true;
      clearTimeout(reconnectTimer);
      ws?.close();
    };
  }, []);

  return { data, connected };
}
