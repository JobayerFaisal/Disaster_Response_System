import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="w-64 h-screen bg-gray-900 text-white p-5 fixed">
      <h1 className="text-2xl font-bold mb-5">🌎 Disaster AI</h1>

      <ul className="space-y-4">
        <li><Link to="/weather">🌧 Weather</Link></li>
        <li><Link to="/predictions">🔮 Predictions</Link></li>
        <li><Link to="/danger-zones">⚠ Danger Zones</Link></li>
        <li><Link to="/map">🛰 Map</Link></li>
        <li><Link to="/agents">🧠 Agent Logs</Link></li>
      </ul>
    </nav>
  );
}
