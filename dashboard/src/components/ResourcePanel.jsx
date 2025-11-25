import Panel from "./Panel";

export default function ResourcePanel({ data }) {
  return (
    <Panel title="Resource Allocation">
      {!data?.resource_plan && "Waiting..."}
      {data?.resource_plan && (
        <pre className="text-sm">
          {JSON.stringify(data.resource_plan, null, 2)}
        </pre>
      )}
    </Panel>
  );
}
