import { useEffect, useState } from "react";

export default function useSimulationStream() {
  const [data, setData] = useState([]);

  useEffect(() => {
    const ws = new WebSocket(import.meta.env.VITE_BACKEND_WS);

    ws.onmessage = (msg) => {
      const packet = JSON.parse(msg.data);
      setData((old) => [...old, packet]);
    };

    return () => ws.close();
  }, []);

  return data;
}
