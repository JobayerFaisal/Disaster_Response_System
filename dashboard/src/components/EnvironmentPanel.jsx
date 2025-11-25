import Panel from "./Panel";

export default function EnvironmentPanel({ data }) {
  return (
    <Panel title="Environment Summary">
      {!data?.weather && "Waiting..."}
      {data?.weather && (
        <div>
          <div>Rainfall: {data.weather.rainfall_mm} mm</div>
          <div>Humidity: {data.weather.humidity}%</div>
          <div>Wind: {data.weather.wind_kmh} km/h</div>
          <div className="font-bold">Alert: {data.weather.alert_level}</div>
        </div>
      )}
    </Panel>
  );
}
