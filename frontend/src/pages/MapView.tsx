import { MapContainer, TileLayer, Circle } from "react-leaflet";
import { useEffect, useState } from "react";
import { API } from "../services/api";
import "leaflet/dist/leaflet.css";


export default function MapView() {
  const [zones, setZones] = useState([]);

  useEffect(() => {
    API.get("/zones").then((res) => setZones(res.data));
  }, []);

  return (
    <div>
      <h1 className="text-3xl font-bold">🛰 Map View</h1>

      <MapContainer
        center={[23.8103, 90.4125]}
        zoom={10}
        style={{ height: "500px", width: "100%", marginTop: "20px" }}
      >
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

        {zones.map((zone: any) => (
          <Circle
            key={zone.id}
            center={[zone.center_lat, zone.center_lon]}
            radius={zone.radius_km * 1000}
            color="red"
          />
        ))}
      </MapContainer>
    </div>
  );
}
