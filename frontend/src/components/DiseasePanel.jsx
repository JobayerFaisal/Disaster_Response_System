import Panel from "./Panel";

export default function DiseasePanel({ data }) {
  return (
    <Panel title="Disease Risk">
      {!data?.disease_risk && "Waiting..."}
      {data?.disease_risk && (
        <pre className="text-sm">
          {JSON.stringify(data.disease_risk, null, 2)}
        </pre>
      )}
    </Panel>
  );
}
