import { useEffect, useState } from "react";
import { API } from "../services/api";
import Card from "../components/Card";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

export default function Weather() {
  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    API.get("/weather/latest").then((res) => {
      setData([res.data]);
    });
  }, []);

  return (
    <div>
      <h1 className="text-3xl font-bold">🌧 Real-Time Weather</h1>

      {data.length > 0 && (
        <>
          <div className="grid grid-cols-3 gap-4 mt-6">
            <Card title="Temperature" value={data[0].temperature + "°C"} />
            <Card title="Humidity" value={data[0].humidity + "%"} />
            <Card title="Wind" value={data[0].wind_speed + " m/s"} />
          </div>

          <div className="mt-10 p-4 bg-white rounded shadow">
            <LineChart width={800} height={300} data={data}>
              <CartesianGrid />
              <XAxis dataKey="timestamp" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="temperature" stroke="#1E90FF" />
            </LineChart>
          </div>
        </>
      )}
    </div>
  );
}
