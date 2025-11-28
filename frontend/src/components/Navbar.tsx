import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="w-64 h-screen bg-gray-900 text-white p-5 fixed left-0 top-0">
      <h1 className="text-2xl font-bold mb-5">🌎 Disaster AI</h1>

      <ul className="space-y-4">
        <li><Link to="/weather" className="hover:text-blue-300">🌧 Weather</Link></li>
        <li><Link to="/predictions" className="hover:text-blue-300">🔮 Predictions</Link></li>
        <li><Link to="/danger-zones" className="hover:text-blue-300">⚠ Danger Zones</Link></li>
        <li><Link to="/map" className="hover:text-blue-300">🛰 Map</Link></li>
        <li><Link to="/agents" className="hover:text-blue-300">🧠 Agent Logs</Link></li>
      </ul>
    </nav>
  );
}
