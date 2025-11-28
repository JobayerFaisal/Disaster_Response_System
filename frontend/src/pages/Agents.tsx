import { useEffect, useState } from "react";
import { API } from "../services/api";

export default function Agents() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    API.get("/agents/logs").then((res) => setLogs(res.data));
  }, []);

  return (
    <div>
      <h1 className="text-3xl font-bold">🧠 Agent Logs</h1>

      <table className="mt-6 w-full bg-white shadow rounded">
        <thead>
          <tr className="bg-gray-200">
            <th className="p-3">Agent</th>
            <th className="p-3">Status</th>
            <th className="p-3">Message</th>
            <th className="p-3">Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {logs.map((log: any) => (
            <tr key={log.id}>
              <td className="p-3">{log.agent_name}</td>
              <td className="p-3">{log.status}</td>
              <td className="p-3">{log.message}</td>
              <td className="p-3">{log.timestamp}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
