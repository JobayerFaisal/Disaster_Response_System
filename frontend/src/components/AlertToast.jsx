import React, { useEffect, useState } from "react";
import { alertSocket } from "../services/websocket";

export default function AlertToast() {
  const [alert, setAlert] = useState<any>(null);

  useEffect(() => {
    alertSocket.onmessage = (event) => {
      if (event.data !== "{}") {
        setAlert(JSON.parse(event.data));
      }
    };
  }, []);

  if (!alert) return null;

  return (
    <div className="fixed top-4 right-4 bg-red-600 text-white px-4 py-3 rounded shadow">
      <p>{alert.message}</p>
      <small className="opacity-80">
        Severity: {alert.severity} | {alert.timestamp}
      </small>
    </div>
  );
}
