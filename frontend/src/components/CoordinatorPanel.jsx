import Panel from "./Panel";

export default function CoordinatorPanel({ data }) {
  return (
    <Panel title="Coordinator Decision">
      {!data?.coordinator && "Waiting..."}
      {data?.coordinator && (
        <pre className="text-sm">
          {JSON.stringify(data.coordinator, null, 2)}
        </pre>
      )}
    </Panel>
  );
}
