import { useState } from "react";
import { API } from "../services/api";  // Make sure to adjust this import to your API service location

export default function ManualReport() {
  const [userId, setUserId] = useState<number>(0);
  const [location, setLocation] = useState<string>("");
  const [severity, setSeverity] = useState<string>("");
  const [description, setDescription] = useState<string>("");
  const [message, setMessage] = useState<string>("");

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    try {
      const response = await API.post("/manual-report/submit_report", {
        user_id: userId,
        location,
        severity,
        description,
      });

      if (response.status === 200) {
        setMessage("Report submitted successfully!");
      } else {
        setMessage("Failed to submit the report.");
      }
    } catch (error) {
      setMessage("Error submitting the report.");
    }
  };

  return (
    <div className="container">
      <h1 className="text-3xl font-bold mb-4">📝 Submit a Manual Report</h1>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="flex flex-col">
          <label htmlFor="user_id" className="mb-1 text-lg font-medium">
            User ID
          </label>
          <input
            type="number"
            id="user_id"
            value={userId}
            onChange={(e) => setUserId(Number(e.target.value))}
            className="p-2 border border-gray-300 rounded"
            required
          />
        </div>

        <div className="flex flex-col">
          <label htmlFor="location" className="mb-1 text-lg font-medium">
            Location
          </label>
          <input
            type="text"
            id="location"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            className="p-2 border border-gray-300 rounded"
            required
          />
        </div>

        <div className="flex flex-col">
          <label htmlFor="severity" className="mb-1 text-lg font-medium">
            Severity
          </label>
          <input
            type="text"
            id="severity"
            value={severity}
            onChange={(e) => setSeverity(e.target.value)}
            className="p-2 border border-gray-300 rounded"
            required
          />
        </div>

        <div className="flex flex-col">
          <label htmlFor="description" className="mb-1 text-lg font-medium">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="p-2 border border-gray-300 rounded"
            rows={4}
            required
          />
        </div>

        <button
          type="submit"
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Submit Report
        </button>
      </form>

      {message && (
        <div className="mt-4 text-center">
          <p className="text-lg font-semibold">{message}</p>
        </div>
      )}
    </div>
  );
}
