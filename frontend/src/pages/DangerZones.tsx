import { useEffect, useState } from "react";
import { API } from "../services/api";

export default function DangerZones() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/danger-zones").then((res) => setData(res.data));
  }, []);

  return (
    <div>
      <h1 className="text-3xl font-bold">⚠ Danger Zone Reports</h1>

      <table className="mt-6 w-full bg-white shadow rounded">
        <thead>
          <tr className="border-b bg-gray-200 text-left">
            <th className="p-3">Zone</th>
            <th className="p-3">Severity</th>
            <th className="p-3">Affected Area (km²)</th>
            <th className="p-3">Risk Score</th>
            <th className="p-3">Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item: any) => (
            <tr key={item.id} className="border-b hover:bg-gray-50">
              <td className="p-3">{item.zone_id}</td>
              <td className="p-3">{item.severity_level}</td>
              <td className="p-3">{item.affected_area_km2}</td>
              <td className="p-3">{item.risk_score}</td>
              <td className="p-3">{item.timestamp}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
