// Inside Navbar component
import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="w-64 bg-gray-800 text-white">
      <ul>
        <li><Link to="/weather">Weather</Link></li>
        <li><Link to="/predictions">Predictions</Link></li>
        <li><Link to="/danger-zones">Danger Zones</Link></li>
        <li><Link to="/map">Map View</Link></li>
        <li><Link to="/agents">Agents</Link></li>
        <li><Link to="/manual-report">Submit Report</Link></li>  {/* Link to Manual Report */}
      </ul>
    </nav>
  );
}

export default Navbar;
