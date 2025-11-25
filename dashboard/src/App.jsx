import { useEffect, useState } from "react";

const API_BASE_URL = "http://localhost:8000"; // ⬅️ change to your backend URL

export default function App() {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        setError("");
        const res = await fetch(`${API_BASE_URL}/api/flood/summary`);
        if (!res.ok) {
          throw new Error(`HTTP ${res.status}`);
        }
        const data = await res.json();
        setStatus(data);
      } catch (err) {
        setError(err.message || "Failed to load data");
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, []);

  return (
    <div style={{ fontFamily: "system-ui, sans-serif", padding: "2rem" }}>
      <h1 style={{ fontSize: "2.5rem", marginBottom: "0.5rem" }}>
        Flood Dashboard
      </h1>
      <p style={{ marginBottom: "1.5rem", color: "#555" }}>
        Live overview of flood risk in Bangladesh (demo layout).
      </p>

      {loading && <p>Loading latest flood data…</p>}
      {error && (
        <p style={{ color: "red" }}>
          Failed to load data: {error}
        </p>
      )}

      {status && (
        <>
          <section
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
              gap: "1rem",
              marginBottom: "2rem",
            }}
          >
            <div
              style={{
                border: "1px solid #ddd",
                borderRadius: "0.75rem",
                padding: "1rem",
              }}
            >
              <h2>Current Alert Level</h2>
              <p style={{ fontSize: "1.5rem", fontWeight: "bold" }}>
                {status.alert_level}
              </p>
            </div>

            <div
              style={{
                border: "1px solid #ddd",
                borderRadius: "0.75rem",
                padding: "1rem",
              }}
            >
              <h2>High-Risk Districts</h2>
              <ul>
                {status.high_risk_areas.map((area) => (
                  <li key={area}>{area}</li>
                ))}
              </ul>
            </div>

            <div
              style={{
                border: "1px solid #ddd",
                borderRadius: "0.75rem",
                padding: "1rem",
              }}
            >
              <h2>Last Updated</h2>
              <p>{status.last_updated}</p>
            </div>
          </section>

          <section>
            <h2>Details</h2>
            <pre
              style={{
                background: "#f9f9f9",
                padding: "1rem",
                borderRadius: "0.75rem",
                overflowX: "auto",
              }}
            >
              {JSON.stringify(status, null, 2)}
            </pre>
          </section>
        </>
      )}
    </div>
  );
}
