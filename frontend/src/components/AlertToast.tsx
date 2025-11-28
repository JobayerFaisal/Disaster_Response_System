import { useEffect, useState } from "react";
import { alertSocket } from "../services/websocket";

interface AlertData {
  message: string;
  severity: string;
  timestamp: string;
}

export default function AlertToast() {
  const [alert, setAlert] = useState<AlertData | null>(null);

  useEffect(() => {
    alertSocket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data && data.message) {
          setAlert(data);

          // hide after 5 seconds
          setTimeout(() => setAlert(null), 5000);
        }
      } catch (e) {
        console.error("Invalid alert format:", e);
      }
    };
  }, []);

  if (!alert) return null;

  return (
    <div className="fixed top-4 right-4 bg-red-600 text-white px-4 py-3 rounded shadow z-50">
      <p className="font-bold">{alert.message}</p>
      <small className="opacity-80 text-sm">
        Severity: {alert.severity} | {alert.timestamp}
      </small>
    </div>
  );
}

