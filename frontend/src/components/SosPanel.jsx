import Panel from "./Panel";

export default function SosPanel({ data }) {
  return (
    <Panel title="SOS Triage">
      {!data?.triaged_sos && "Waiting..."}
      {data?.triaged_sos?.map((s, i) => (
        <div key={i} className="mb-2">
          <div>Source: {s.source}</div>
          <div>Location: {s.location}</div>
          <div className="font-bold text-red-400">Priority: {s.priority}</div>
        </div>
      ))}
    </Panel>
  );
}
