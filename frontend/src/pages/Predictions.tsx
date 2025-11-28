import { useEffect, useState } from "react";
import { API } from "../services/api";
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from "recharts";

export default function Predictions() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/predictions").then((res) => setData(res.data));
  }, []);

  return (
    <div>
      <h1 className="text-3xl font-bold">🔮 Flood Predictions</h1>

      <div className="mt-6 bg-white p-4 rounded shadow">
        <LineChart width={900} height={300} data={data}>
          <CartesianGrid />
          <XAxis dataKey="timestamp" />
          <YAxis />
          <Tooltip />
          <Line dataKey="risk_score" stroke="#FF5733" />
        </LineChart>
      </div>
    </div>
  );
}
