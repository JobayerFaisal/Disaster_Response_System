import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import AlertToast from "./components/AlertToast";

import Weather from "./pages/Weather";
import Predictions from "./pages/Predictions";
import DangerZones from "./pages/DangerZones";
import Agents from "./pages/Agents";
import MapView from "./pages/MapView";
import ManualReport from "./pages/ManualReport";  // <-- Import the new page

export default function App() {
  return (
    <BrowserRouter>
      <AlertToast />
      <div className="flex">
        <Navbar />
        <main className="ml-64 p-8 w-full bg-gray-100 min-h-screen">
          <Routes>
            <Route path="/weather" element={<Weather />} />
            <Route path="/predictions" element={<Predictions />} />
            <Route path="/danger-zones" element={<DangerZones />} />
            <Route path="/map" element={<MapView />} />
            <Route path="/agents" element={<Agents />} />
            <Route path="/manual-report" element={<ManualReport />} />  {/* <-- New route */}
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
